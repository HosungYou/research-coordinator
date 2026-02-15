/**
 * sqlite-state.js
 *
 * SQLite state store for Diverga v9.0.
 * Replaces YAML files as the source of truth for checkpoints, decisions,
 * project state, messages, and agents. YAML becomes export-only format.
 *
 * Uses better-sqlite3 for synchronous, WAL-mode access.
 */

import Database from 'better-sqlite3';
import yaml from 'js-yaml';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { CHECKPOINT_LEVELS } from './constants.js';
import { deepMerge } from './utils.js';

// ---------------------------------------------------------------------------
// createStateStore(dbPath) -> store
// ---------------------------------------------------------------------------

export function createStateStore(dbPath) {
  // Ensure parent directory exists
  const dir = dirname(dbPath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

  const db = new Database(dbPath);

  // Enable WAL mode for concurrent access
  db.pragma('journal_mode = WAL');

  // Create tables (idempotent with IF NOT EXISTS)
  db.exec(`
    CREATE TABLE IF NOT EXISTS checkpoints (
      checkpoint_id TEXT PRIMARY KEY,
      decision TEXT,
      rationale TEXT,
      level TEXT,
      status TEXT,
      completed_at TEXT
    );

    CREATE TABLE IF NOT EXISTS decisions (
      decision_id TEXT PRIMARY KEY,
      checkpoint_id TEXT,
      selected TEXT,
      rationale TEXT,
      context TEXT,
      version INTEGER,
      timestamp TEXT
    );

    CREATE TABLE IF NOT EXISTS project_state (
      key TEXT PRIMARY KEY,
      value TEXT
    );

    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY,
      from_agent TEXT,
      to_agent TEXT,
      content TEXT,
      type TEXT,
      priority TEXT,
      timestamp TEXT
    );

    CREATE TABLE IF NOT EXISTS agents (
      agent_id TEXT PRIMARY KEY,
      role TEXT,
      model TEXT,
      capabilities TEXT
    );

    CREATE TABLE IF NOT EXISTS schema_version (
      version INTEGER,
      applied_at TEXT
    );
  `);

  // Insert schema version if table is empty
  const versionRow = db.prepare('SELECT version FROM schema_version LIMIT 1').get();
  if (!versionRow) {
    db.prepare('INSERT INTO schema_version (version, applied_at) VALUES (?, ?)').run(
      1,
      new Date().toISOString()
    );
  }

  // -------------------------------------------------------------------------
  // Prepared statements
  // -------------------------------------------------------------------------

  const stmts = {
    upsertCheckpoint: db.prepare(`
      INSERT INTO checkpoints (checkpoint_id, decision, rationale, level, status, completed_at)
      VALUES (@checkpoint_id, @decision, @rationale, @level, @status, @completed_at)
      ON CONFLICT(checkpoint_id) DO UPDATE SET
        decision = @decision,
        rationale = @rationale,
        level = @level,
        status = @status,
        completed_at = @completed_at
    `),
    getCheckpoint: db.prepare('SELECT * FROM checkpoints WHERE checkpoint_id = ?'),
    listCheckpoints: db.prepare('SELECT * FROM checkpoints ORDER BY completed_at DESC, rowid DESC'),
    getCheckpointsByLevel: db.prepare('SELECT * FROM checkpoints WHERE level = ? ORDER BY completed_at DESC, rowid DESC'),

    insertDecision: db.prepare(`
      INSERT INTO decisions (decision_id, checkpoint_id, selected, rationale, context, version, timestamp)
      VALUES (@decision_id, @checkpoint_id, @selected, @rationale, @context, @version, @timestamp)
    `),
    countDecisions: db.prepare('SELECT COUNT(*) as cnt FROM decisions'),
    listDecisions: db.prepare('SELECT * FROM decisions ORDER BY timestamp DESC, rowid DESC'),
    getDecision: db.prepare('SELECT * FROM decisions WHERE decision_id = ?'),

    getProjectState: db.prepare('SELECT value FROM project_state WHERE key = ?'),
    upsertProjectState: db.prepare(`
      INSERT INTO project_state (key, value) VALUES (@key, @value)
      ON CONFLICT(key) DO UPDATE SET value = @value
    `),
  };

  // -------------------------------------------------------------------------
  // Checkpoint methods
  // -------------------------------------------------------------------------

  function markCheckpoint(cpId, decision, rationale) {
    const level = CHECKPOINT_LEVELS[cpId] || 'OPTIONAL';
    const now = new Date().toISOString();

    stmts.upsertCheckpoint.run({
      checkpoint_id: cpId,
      decision,
      rationale: rationale ?? null,
      level: level.toUpperCase(),
      status: 'completed',
      completed_at: now,
    });

    return { recorded: true, checkpoint_id: cpId };
  }

  function getCheckpoint(cpId) {
    const row = stmts.getCheckpoint.get(cpId);
    return row || null;
  }

  function listCheckpoints() {
    return stmts.listCheckpoints.all();
  }

  function isCheckpointApproved(cpId) {
    const row = stmts.getCheckpoint.get(cpId);
    return !!row;
  }

  function getCheckpointsByLevel(level) {
    return stmts.getCheckpointsByLevel.all(level.toUpperCase());
  }

  // -------------------------------------------------------------------------
  // Decision methods
  // -------------------------------------------------------------------------

  function _nextDecisionId() {
    const { cnt } = stmts.countDecisions.get();
    return `DEV_${String(cnt + 1).padStart(3, '0')}`;
  }

  function addDecision(cpId, selected, rationale, context) {
    const decisionId = _nextDecisionId();
    const now = new Date().toISOString();

    let contextStr = null;
    if (context !== undefined && context !== null) {
      contextStr = typeof context === 'object' ? JSON.stringify(context) : String(context);
    }

    stmts.insertDecision.run({
      decision_id: decisionId,
      checkpoint_id: cpId,
      selected,
      rationale,
      context: contextStr,
      version: 1,
      timestamp: now,
    });

    return { recorded: true, decision_id: decisionId };
  }

  function _parseDecisionContext(row) {
    if (!row) return null;
    const result = { ...row };
    if (result.context) {
      try {
        result.context = JSON.parse(result.context);
      } catch {
        // leave as string
      }
    }
    return result;
  }

  function listDecisions() {
    const rows = stmts.listDecisions.all();
    return rows.map(_parseDecisionContext);
  }

  function getDecision(decisionId) {
    const row = stmts.getDecision.get(decisionId);
    if (!row) return null;
    return _parseDecisionContext(row);
  }

  function amendDecision(decisionId, newSelected, newRationale) {
    const original = stmts.getDecision.get(decisionId);
    if (!original) return { recorded: false, error: 'Decision not found' };

    const newId = _nextDecisionId();
    const now = new Date().toISOString();

    stmts.insertDecision.run({
      decision_id: newId,
      checkpoint_id: original.checkpoint_id,
      selected: newSelected,
      rationale: newRationale,
      context: original.context,
      version: original.version + 1,
      timestamp: now,
    });

    return { recorded: true, decision_id: newId };
  }

  // -------------------------------------------------------------------------
  // Project state methods
  // -------------------------------------------------------------------------

  function getProjectState() {
    const row = stmts.getProjectState.get('_state');
    if (!row || !row.value) return {};
    try {
      const parsed = JSON.parse(row.value);
      // Remove internal _stage key from returned state
      const { _stage, ...rest } = parsed;
      return rest;
    } catch {
      return {};
    }
  }

  function _getRawState() {
    const row = stmts.getProjectState.get('_state');
    if (!row || !row.value) return {};
    try {
      return JSON.parse(row.value);
    } catch {
      return {};
    }
  }

  function updateProjectState(updates) {
    const current = _getRawState();
    const merged = deepMerge(current, updates);
    stmts.upsertProjectState.run({
      key: '_state',
      value: JSON.stringify(merged),
    });
  }

  function setStage(stageName) {
    const current = _getRawState();
    current._stage = stageName;
    stmts.upsertProjectState.run({
      key: '_state',
      value: JSON.stringify(current),
    });
  }

  function getStage() {
    const current = _getRawState();
    return current._stage || null;
  }

  // -------------------------------------------------------------------------
  // YAML export methods
  // -------------------------------------------------------------------------

  function exportCheckpointsYaml() {
    const checkpoints = listCheckpoints();
    const data = { checkpoints: { active: checkpoints } };
    return yaml.dump(data, { lineWidth: 120, noRefs: true });
  }

  function exportDecisionLogYaml() {
    const decisions = listDecisions();
    const data = { decisions };
    return yaml.dump(data, { lineWidth: 120, noRefs: true });
  }

  function exportProjectStateYaml() {
    const state = getProjectState();
    return yaml.dump(state, { lineWidth: 120, noRefs: true });
  }

  function exportAll(outputDir) {
    if (!existsSync(outputDir)) mkdirSync(outputDir, { recursive: true });

    writeFileSync(join(outputDir, 'checkpoints.yaml'), exportCheckpointsYaml(), 'utf8');
    writeFileSync(join(outputDir, 'decision-log.yaml'), exportDecisionLogYaml(), 'utf8');
    writeFileSync(join(outputDir, 'project-state.yaml'), exportProjectStateYaml(), 'utf8');
  }

  // -------------------------------------------------------------------------
  // Migration from YAML
  // -------------------------------------------------------------------------

  function migrateFromYaml(researchDir) {
    const skipped = [];

    // --- Checkpoints ---
    const cpPath = join(researchDir, 'checkpoints.yaml');
    if (existsSync(cpPath)) {
      try {
        const cpData = yaml.load(readFileSync(cpPath, 'utf8'));
        if (cpData?.checkpoints?.active && Array.isArray(cpData.checkpoints.active)) {
          for (const cp of cpData.checkpoints.active) {
            const level = cp.level || CHECKPOINT_LEVELS[cp.checkpoint_id] || 'OPTIONAL';
            stmts.upsertCheckpoint.run({
              checkpoint_id: cp.checkpoint_id,
              decision: cp.decision || null,
              rationale: cp.rationale || null,
              level: level.toUpperCase(),
              status: cp.status || 'completed',
              completed_at: cp.completed_at || new Date().toISOString(),
            });
          }
        }
      } catch {
        skipped.push('checkpoints.yaml (parse error)');
      }
    } else {
      skipped.push('checkpoints.yaml (not found)');
    }

    // --- Decisions ---
    const dlPath = join(researchDir, 'decision-log.yaml');
    if (existsSync(dlPath)) {
      try {
        const dlData = yaml.load(readFileSync(dlPath, 'utf8'));
        if (dlData?.decisions && Array.isArray(dlData.decisions)) {
          for (const d of dlData.decisions) {
            // Check if already exists (idempotent)
            const existing = stmts.getDecision.get(d.decision_id);
            if (existing) continue;

            let contextStr = null;
            if (d.context !== undefined && d.context !== null) {
              contextStr = typeof d.context === 'object' ? JSON.stringify(d.context) : String(d.context);
            }

            stmts.insertDecision.run({
              decision_id: d.decision_id,
              checkpoint_id: d.checkpoint_id || null,
              selected: d.selected || null,
              rationale: d.rationale || null,
              context: contextStr,
              version: d.version || 1,
              timestamp: d.timestamp || new Date().toISOString(),
            });
          }
        }
      } catch {
        skipped.push('decision-log.yaml (parse error)');
      }
    } else {
      skipped.push('decision-log.yaml (not found)');
    }

    // --- Project State ---
    const psPath = join(researchDir, 'project-state.yaml');
    if (existsSync(psPath)) {
      try {
        const psData = yaml.load(readFileSync(psPath, 'utf8'));
        if (psData && typeof psData === 'object') {
          updateProjectState(psData);
        }
      } catch {
        skipped.push('project-state.yaml (parse error)');
      }
    } else {
      skipped.push('project-state.yaml (not found)');
    }

    return { success: true, skipped };
  }

  // -------------------------------------------------------------------------
  // Return store object
  // -------------------------------------------------------------------------

  function close() {
    db.close();
  }

  return {
    db,
    close,
    markCheckpoint,
    getCheckpoint,
    listCheckpoints,
    isCheckpointApproved,
    getCheckpointsByLevel,
    addDecision,
    listDecisions,
    getDecision,
    amendDecision,
    getProjectState,
    updateProjectState,
    setStage,
    getStage,
    exportCheckpointsYaml,
    exportDecisionLogYaml,
    exportProjectStateYaml,
    exportAll,
    migrateFromYaml,
  };
}
