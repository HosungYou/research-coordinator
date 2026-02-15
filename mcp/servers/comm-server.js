/**
 * comm-server.js
 *
 * Communication MCP server for Diverga v9.0.
 * Handles agent messaging for pipeline coordination.
 * Split from checkpoint-server.js in v9.0.
 *
 * Uses JSON files in .research/comm/ for persistence.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

// ---------------------------------------------------------------------------
// createCommServer(researchDir) -> server
// ---------------------------------------------------------------------------

export function createCommServer(researchDir) {
  if (!researchDir) throw new Error('Research directory is required');

  // Eagerly create comm directory
  const _commPath = join(researchDir, '.research', 'comm');
  if (!existsSync(_commPath)) mkdirSync(_commPath, { recursive: true });

  // -------------------------------------------------------------------------
  // Internal helpers
  // -------------------------------------------------------------------------

  function _commDir() {
    if (!existsSync(_commPath)) mkdirSync(_commPath, { recursive: true });
    return _commPath;
  }

  function _readJson(filename) {
    const dir = join(researchDir, '.research', 'comm');
    const filepath = join(dir, filename);
    if (!existsSync(filepath)) return null;
    try {
      return JSON.parse(readFileSync(filepath, 'utf8'));
    } catch {
      return null;
    }
  }

  function _writeJson(filename, data) {
    const dir = _commDir();
    writeFileSync(join(dir, filename), JSON.stringify(data, null, 2), 'utf8');
  }

  function _readAgents() {
    return _readJson('agents.json') || { agents: {} };
  }

  function _writeAgents(data) {
    _writeJson('agents.json', data);
  }

  function _readMessages() {
    return _readJson('messages.json') || { messages: [] };
  }

  function _writeMessages(data) {
    _writeJson('messages.json', data);
  }

  function _normalizeAgentId(id) {
    return id.toLowerCase();
  }

  function _nextMessageId(messages) {
    return `msg_${String(messages.length + 1).padStart(3, '0')}`;
  }

  // -------------------------------------------------------------------------
  // registerAgent
  // -------------------------------------------------------------------------

  function registerAgent(agentId, metadata = {}) {
    if (!agentId) throw new Error('Agent ID is required');

    const normalizedId = _normalizeAgentId(agentId);
    const data = _readAgents();
    const now = new Date().toISOString();

    const existing = data.agents[normalizedId];

    if (existing) {
      data.agents[normalizedId] = {
        ...existing,
        ...metadata,
        registered_at: existing.registered_at,
        updated_at: now,
      };
    } else {
      data.agents[normalizedId] = {
        ...metadata,
        registered_at: now,
      };
    }

    _writeAgents(data);

    return { registered: true, agent_id: normalizedId };
  }

  // -------------------------------------------------------------------------
  // listAgents
  // -------------------------------------------------------------------------

  function listAgents(filters = {}) {
    const data = _readAgents();
    let agents = Object.entries(data.agents).map(([id, meta]) => ({
      agent_id: id,
      ...meta,
    }));

    if (filters.status) {
      agents = agents.filter(a => a.status === filters.status);
    }

    if (filters.category) {
      agents = agents.filter(a => a.category === filters.category);
    }

    if (filters.model) {
      agents = agents.filter(a => a.model === filters.model);
    }

    return agents;
  }

  // -------------------------------------------------------------------------
  // send
  // -------------------------------------------------------------------------

  function send(from, to, content, metadata) {
    if (!from || !to) throw new Error('Both from and to are required');
    if (!content && content !== 0) throw new Error('Message content is required');

    const data = _readMessages();
    const messageId = _nextMessageId(data.messages);
    const now = new Date().toISOString();

    const message = {
      message_id: messageId,
      from,
      to,
      content,
      status: 'unread',
      sent_at: now,
    };

    if (metadata && typeof metadata === 'object' && Object.keys(metadata).length > 0) {
      message.metadata = metadata;
    }

    data.messages.push(message);
    _writeMessages(data);

    return { sent: true, message_id: messageId };
  }

  // -------------------------------------------------------------------------
  // mailbox
  // -------------------------------------------------------------------------

  function mailbox(agentId, options = {}) {
    const { status, from, includeRead = false, autoMark = true } = options;

    const data = _readMessages();
    let messages = data.messages.filter(m => m.to === agentId);

    if (status) {
      messages = messages.filter(m => m.status === status);
    } else if (!includeRead) {
      messages = messages.filter(m => m.status === 'unread');
    }

    if (from) {
      messages = messages.filter(m => m.from === from);
    }

    // Create return copies before modifying
    const result = messages.map(m => ({ ...m }));

    // Auto-mark unread messages as read
    if (autoMark !== false) {
      let modified = false;
      for (const msg of messages) {
        if (msg.status === 'unread') {
          msg.status = 'read';
          msg.read_at = new Date().toISOString();
          modified = true;
        }
      }
      if (modified) {
        _writeMessages(data);
      }
    }

    return result;
  }

  // -------------------------------------------------------------------------
  // acknowledge
  // -------------------------------------------------------------------------

  function acknowledge(messageId, response) {
    if (!messageId) throw new Error('Message ID is required');

    const data = _readMessages();
    const msg = data.messages.find(m => m.message_id === messageId);

    if (!msg) throw new Error(`Message ${messageId} not found`);

    msg.status = 'acknowledged';
    msg.acknowledged_at = new Date().toISOString();

    if (response !== undefined && response !== null) {
      msg.response = response;
    }

    _writeMessages(data);

    return { acknowledged: true, message_id: messageId };
  }

  // -------------------------------------------------------------------------
  // broadcast
  // -------------------------------------------------------------------------

  function broadcast(from, content, metadata) {
    if (!from) throw new Error('From (sender) is required');
    if (!content && content !== 0) throw new Error('Message content is required');

    const agentsData = _readAgents();
    const recipients = Object.keys(agentsData.agents).filter(id => id !== from);

    const data = _readMessages();
    const now = new Date().toISOString();

    for (const to of recipients) {
      const messageId = _nextMessageId(data.messages);
      const message = {
        message_id: messageId,
        from,
        to,
        content,
        status: 'unread',
        broadcast: true,
        sent_at: now,
      };

      if (metadata && typeof metadata === 'object' && Object.keys(metadata).length > 0) {
        message.metadata = metadata;
      }

      data.messages.push(message);
    }

    _writeMessages(data);

    return { sent: true, recipient_count: recipients.length };
  }

  // -------------------------------------------------------------------------
  // Return server object
  // -------------------------------------------------------------------------

  return {
    registerAgent,
    listAgents,
    send,
    mailbox,
    acknowledge,
    broadcast,
  };
}
