/**
 * messaging.js
 *
 * Agent-to-agent messaging system for Diverga v9.0.
 * Provides direct messaging, broadcast, channels, progress reporting,
 * and checkpoint relay for pipeline coordination (I0→I1→I2→I3).
 *
 * Uses SQLite state store (better-sqlite3) for persistence.
 */

// ---------------------------------------------------------------------------
// createMessaging(store) -> messaging
// ---------------------------------------------------------------------------

export function createMessaging(store) {
  const db = store.db;

  // -------------------------------------------------------------------------
  // Create messaging tables (idempotent)
  // -------------------------------------------------------------------------

  db.exec(`
    CREATE TABLE IF NOT EXISTS msg_agents (
      agent_id TEXT PRIMARY KEY,
      role TEXT,
      model TEXT,
      capabilities TEXT,
      registered_at INTEGER
    );

    CREATE TABLE IF NOT EXISTS msg_messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      message_id TEXT UNIQUE NOT NULL,
      from_agent TEXT NOT NULL,
      to_agent TEXT NOT NULL,
      content TEXT,
      type TEXT DEFAULT 'message',
      priority TEXT DEFAULT 'normal',
      delivered INTEGER DEFAULT 0,
      acknowledged INTEGER DEFAULT 0,
      acknowledged_at TEXT,
      channel TEXT,
      timestamp INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS msg_channels (
      name TEXT PRIMARY KEY,
      members TEXT NOT NULL,
      status TEXT DEFAULT 'open',
      created_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS msg_progress (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      agent_id TEXT NOT NULL,
      stage TEXT,
      percent REAL,
      detail TEXT,
      message_id TEXT,
      timestamp INTEGER NOT NULL
    );
  `);

  // -------------------------------------------------------------------------
  // Prepared statements
  // -------------------------------------------------------------------------

  const stmts = {
    upsertAgent: db.prepare(`
      INSERT INTO msg_agents (agent_id, role, model, capabilities, registered_at)
      VALUES (@agent_id, @role, @model, @capabilities, @registered_at)
      ON CONFLICT(agent_id) DO UPDATE SET
        role = @role, model = @model, capabilities = @capabilities
    `),
    getAgent: db.prepare('SELECT * FROM msg_agents WHERE agent_id = ?'),
    listAgents: db.prepare('SELECT * FROM msg_agents ORDER BY registered_at ASC, rowid ASC'),
    deleteAgent: db.prepare('DELETE FROM msg_agents WHERE agent_id = ?'),

    insertMessage: db.prepare(`
      INSERT INTO msg_messages (message_id, from_agent, to_agent, content, type, priority, channel, timestamp)
      VALUES (@message_id, @from_agent, @to_agent, @content, @type, @priority, @channel, @timestamp)
    `),
    getMessage: db.prepare('SELECT * FROM msg_messages WHERE message_id = ?'),
    countMessages: db.prepare('SELECT COUNT(*) as cnt FROM msg_messages'),

    markDelivered: db.prepare('UPDATE msg_messages SET delivered = 1 WHERE id = ?'),
    markAcknowledged: db.prepare(
      'UPDATE msg_messages SET acknowledged = 1, acknowledged_at = ? WHERE message_id = ?'
    ),

    upsertChannel: db.prepare(`
      INSERT INTO msg_channels (name, members, status, created_at)
      VALUES (@name, @members, @status, @created_at)
      ON CONFLICT(name) DO UPDATE SET members = @members
    `),
    getChannel: db.prepare('SELECT * FROM msg_channels WHERE name = ?'),
    updateChannelMembers: db.prepare('UPDATE msg_channels SET members = ? WHERE name = ?'),
    updateChannelStatus: db.prepare('UPDATE msg_channels SET status = ? WHERE name = ?'),

    insertProgress: db.prepare(`
      INSERT INTO msg_progress (agent_id, stage, percent, detail, message_id, timestamp)
      VALUES (@agent_id, @stage, @percent, @detail, @message_id, @timestamp)
    `),
  };

  // -------------------------------------------------------------------------
  // Internal helpers
  // -------------------------------------------------------------------------

  function _nextMessageId() {
    const { cnt } = stmts.countMessages.get();
    return `msg_${String(cnt + 1).padStart(4, '0')}`;
  }

  function _parseContent(str) {
    if (str === null || str === undefined) return null;
    try {
      return JSON.parse(str);
    } catch {
      return str;
    }
  }

  function _rowToMessage(row) {
    return {
      messageId: row.message_id,
      from: row.from_agent,
      to: row.to_agent,
      content: _parseContent(row.content),
      type: row.type,
      priority: row.priority,
      timestamp: row.timestamp,
      delivered: row.delivered === 1,
      acknowledged: row.acknowledged === 1,
      acknowledgedAt: row.acknowledged_at,
    };
  }

  function _insertMessage(from, to, content, type, priority, channel) {
    const messageId = _nextMessageId();
    const timestamp = Date.now();
    const contentStr = JSON.stringify(content);

    stmts.insertMessage.run({
      message_id: messageId,
      from_agent: from,
      to_agent: to,
      content: contentStr,
      type: type || 'message',
      priority: priority || 'normal',
      channel: channel || null,
      timestamp,
    });

    return messageId;
  }

  // -------------------------------------------------------------------------
  // Agent registration
  // -------------------------------------------------------------------------

  function registerAgent(agentId, metadata = {}) {
    const caps = metadata.capabilities
      ? JSON.stringify(metadata.capabilities)
      : null;

    stmts.upsertAgent.run({
      agent_id: agentId,
      role: metadata.role || null,
      model: metadata.model || null,
      capabilities: caps,
      registered_at: Date.now(),
    });

    return {
      agentId,
      role: metadata.role || null,
      model: metadata.model || null,
      capabilities: metadata.capabilities || null,
    };
  }

  function listAgents() {
    const rows = stmts.listAgents.all();
    return rows.map(r => ({
      agentId: r.agent_id,
      role: r.role,
      model: r.model,
      capabilities: r.capabilities ? JSON.parse(r.capabilities) : null,
    }));
  }

  function getAgent(agentId) {
    const row = stmts.getAgent.get(agentId);
    if (!row) return null;
    return {
      agentId: row.agent_id,
      role: row.role,
      model: row.model,
      capabilities: row.capabilities ? JSON.parse(row.capabilities) : null,
    };
  }

  function unregisterAgent(agentId) {
    const result = stmts.deleteAgent.run(agentId);
    return result.changes > 0;
  }

  // -------------------------------------------------------------------------
  // Direct messaging
  // -------------------------------------------------------------------------

  function send(from, to, content, options = {}) {
    // Validate recipient exists (allow anonymous sender)
    const recipient = stmts.getAgent.get(to);
    if (!recipient) {
      throw new Error(`Agent "${to}" not found`);
    }

    return _insertMessage(from, to, content, options.type, options.priority);
  }

  // -------------------------------------------------------------------------
  // Mailbox
  // -------------------------------------------------------------------------

  function mailbox(agentId, options = {}) {
    const { includeRead = false, type } = options;

    let sql = 'SELECT * FROM msg_messages WHERE to_agent = ?';
    const params = [agentId];

    if (!includeRead) {
      sql += ' AND delivered = 0';
    }

    if (type) {
      sql += ' AND type = ?';
      params.push(type);
    }

    sql += ' ORDER BY timestamp ASC, id ASC';

    const rows = db.prepare(sql).all(...params);
    const messages = rows.map(_rowToMessage);

    // Mark undelivered messages in the result as delivered
    const undeliveredIds = rows.filter(r => r.delivered === 0).map(r => r.id);
    if (undeliveredIds.length > 0) {
      for (const id of undeliveredIds) {
        stmts.markDelivered.run(id);
      }
    }

    return messages;
  }

  function acknowledge(messageId) {
    const now = new Date().toISOString();
    const result = stmts.markAcknowledged.run(now, messageId);
    return result.changes > 0;
  }

  // -------------------------------------------------------------------------
  // Broadcast
  // -------------------------------------------------------------------------

  function broadcast(from, content, options = {}) {
    const { excludeSelf = true, type, roles } = options;

    let agents = listAgents();

    if (excludeSelf) {
      agents = agents.filter(a => a.agentId !== from);
    }

    if (roles && roles.length > 0) {
      agents = agents.filter(a => roles.includes(a.role));
    }

    const messageIds = [];
    for (const agent of agents) {
      const msgId = _insertMessage(from, agent.agentId, content, type);
      messageIds.push(msgId);
    }

    return messageIds;
  }

  // -------------------------------------------------------------------------
  // Channels
  // -------------------------------------------------------------------------

  function createChannel(name, members) {
    stmts.upsertChannel.run({
      name,
      members: JSON.stringify(members),
      status: 'open',
      created_at: Date.now(),
    });

    return { name, members };
  }

  function sendToChannel(channelName, from, content, options = {}) {
    const channelRow = stmts.getChannel.get(channelName);
    if (!channelRow) throw new Error(`Channel "${channelName}" not found`);

    const members = JSON.parse(channelRow.members);
    const messageIds = [];

    for (const member of members) {
      const msgId = _insertMessage(
        from, member, content, options.type, options.priority, channelName
      );
      messageIds.push(msgId);
    }

    return messageIds;
  }

  function getChannelMessages(channelName) {
    const rows = db.prepare(
      'SELECT * FROM msg_messages WHERE channel = ? ORDER BY timestamp ASC, id ASC'
    ).all(channelName);

    return rows.map(_rowToMessage);
  }

  function getChannel(channelName) {
    const row = stmts.getChannel.get(channelName);
    if (!row) return null;
    return {
      name: row.name,
      members: JSON.parse(row.members),
      status: row.status,
    };
  }

  function addChannelMember(channelName, agentId) {
    const row = stmts.getChannel.get(channelName);
    if (!row) throw new Error(`Channel "${channelName}" not found`);

    const members = JSON.parse(row.members);
    if (!members.includes(agentId)) {
      members.push(agentId);
      stmts.updateChannelMembers.run(JSON.stringify(members), channelName);
    }
  }

  function removeChannelMember(channelName, agentId) {
    const row = stmts.getChannel.get(channelName);
    if (!row) throw new Error(`Channel "${channelName}" not found`);

    const members = JSON.parse(row.members).filter(m => m !== agentId);
    stmts.updateChannelMembers.run(JSON.stringify(members), channelName);
  }

  function closeChannel(channelName) {
    stmts.updateChannelStatus.run('closed', channelName);
  }

  // -------------------------------------------------------------------------
  // Progress reporting
  // -------------------------------------------------------------------------

  function reportProgress(agentId, progressData) {
    const { stage, percent, detail } = progressData;

    // Find orchestrator to send progress message to
    const orchestrator = db.prepare(
      "SELECT agent_id FROM msg_agents WHERE role = 'orchestrator' LIMIT 1"
    ).get();

    let messageId = null;
    if (orchestrator) {
      messageId = _insertMessage(
        agentId, orchestrator.agent_id, progressData, 'progress', 'normal'
      );
    }

    // Store in progress table
    stmts.insertProgress.run({
      agent_id: agentId,
      stage: stage || null,
      percent,
      detail: detail || null,
      message_id: messageId,
      timestamp: Date.now(),
    });

    return messageId;
  }

  function getProgress(channelName) {
    const channelRow = stmts.getChannel.get(channelName);
    if (!channelRow) return [];

    const members = JSON.parse(channelRow.members);
    if (members.length === 0) return [];

    const placeholders = members.map(() => '?').join(',');
    const rows = db.prepare(
      `SELECT * FROM msg_progress WHERE agent_id IN (${placeholders}) ORDER BY id DESC`
    ).all(...members);

    // Latest progress per agent
    const latest = new Map();
    for (const row of rows) {
      if (!latest.has(row.agent_id)) {
        latest.set(row.agent_id, {
          agentId: row.agent_id,
          stage: row.stage,
          percent: row.percent,
          detail: row.detail,
          timestamp: row.timestamp,
        });
      }
    }

    return Array.from(latest.values());
  }

  // -------------------------------------------------------------------------
  // Checkpoint relay
  // -------------------------------------------------------------------------

  function relayCheckpoint(cpId, decision, from, targets) {
    const content = { checkpointId: cpId, decision };
    const messageIds = [];

    for (const target of targets) {
      const msgId = _insertMessage(from, target, content, 'checkpoint', 'high');
      messageIds.push(msgId);
    }

    return messageIds;
  }

  async function awaitCheckpoint(agentId, cpId, timeout) {
    const start = Date.now();

    while (Date.now() - start < timeout) {
      // Direct query without mailbox side effects
      const rows = db.prepare(
        `SELECT * FROM msg_messages
         WHERE to_agent = ? AND type = 'checkpoint' AND delivered = 0
         ORDER BY id ASC`
      ).all(agentId);

      for (const row of rows) {
        const content = _parseContent(row.content);
        if (content && content.checkpointId === cpId) {
          // Mark as delivered
          stmts.markDelivered.run(row.id);
          return content;
        }
      }

      await new Promise(r => setTimeout(r, 50));
    }

    return null;
  }

  // -------------------------------------------------------------------------
  // History query
  // -------------------------------------------------------------------------

  function history(filters = {}) {
    const { from, since, limit } = filters;

    let sql = 'SELECT * FROM msg_messages WHERE 1=1';
    const params = [];

    if (from) {
      sql += ' AND from_agent = ?';
      params.push(from);
    }

    if (since !== undefined && since !== null) {
      sql += ' AND timestamp > ?';
      params.push(since);
    }

    sql += ' ORDER BY timestamp ASC, id ASC';

    if (limit) {
      sql += ' LIMIT ?';
      params.push(limit);
    }

    const rows = db.prepare(sql).all(...params);
    return rows.map(_rowToMessage);
  }

  // -------------------------------------------------------------------------
  // Return messaging object
  // -------------------------------------------------------------------------

  return {
    registerAgent,
    listAgents,
    getAgent,
    unregisterAgent,
    send,
    mailbox,
    acknowledge,
    broadcast,
    createChannel,
    sendToChannel,
    getChannelMessages,
    getChannel,
    addChannelMember,
    removeChannelMember,
    closeChannel,
    reportProgress,
    getProgress,
    relayCheckpoint,
    awaitCheckpoint,
    history,
  };
}
