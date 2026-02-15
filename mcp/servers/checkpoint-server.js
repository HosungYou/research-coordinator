/**
 * checkpoint-server.js
 *
 * Checkpoint MCP server for Diverga v9.0.
 * Handles ONLY checkpoint and prerequisite tools.
 * Memory/decision tools are in memory-server.js.
 * Comm tools are in comm-server.js.
 *
 * Uses YAML files for persistence with dual-path support
 * (research/ preferred, .research/ fallback, root fallback).
 */

import yaml from 'js-yaml';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { CHECKPOINT_LEVELS } from '../lib/constants.js';

// ---------------------------------------------------------------------------
// createCheckpointServer(prereqMap, researchDir) -> server
// ---------------------------------------------------------------------------

export function createCheckpointServer(prereqMap, researchDir) {
  if (!prereqMap) throw new Error('Prerequisite map is required');
  if (!researchDir) throw new Error('Research directory is required');

  // -------------------------------------------------------------------------
  // Internal helpers
  // -------------------------------------------------------------------------

  function _normalizeAgentId(id) {
    const lower = id.toLowerCase();
    const match = lower.match(/^([a-z]\d+)/);
    return match ? match[1] : lower;
  }

  function _readYaml(filename) {
    const paths = [
      join(researchDir, 'research', filename),
      join(researchDir, '.research', filename),
      join(researchDir, filename),
    ];

    for (const p of paths) {
      if (existsSync(p)) {
        try {
          return yaml.load(readFileSync(p, 'utf8'));
        } catch {
          return null;
        }
      }
    }
    return null;
  }

  function _writeYaml(filename, data) {
    const researchPath = join(researchDir, 'research');
    if (!existsSync(researchPath)) mkdirSync(researchPath, { recursive: true });

    const yamlStr = yaml.dump(data, { lineWidth: 120, noRefs: true });
    writeFileSync(join(researchPath, filename), yamlStr, 'utf8');
    writeFileSync(join(researchDir, filename), yamlStr, 'utf8');
  }

  function _getPassedCheckpoints() {
    const passed = new Set();

    const cpData = _readYaml('checkpoints.yaml');
    if (cpData?.checkpoints) {
      for (const entries of Object.values(cpData.checkpoints)) {
        if (Array.isArray(entries)) {
          for (const cp of entries) {
            if (cp.status === 'completed' && cp.checkpoint_id) {
              passed.add(cp.checkpoint_id);
            }
          }
        }
      }
    }

    const dlData = _readYaml('decision-log.yaml');
    if (dlData?.decisions && Array.isArray(dlData.decisions)) {
      for (const d of dlData.decisions) {
        if (d.checkpoint_id) {
          passed.add(d.checkpoint_id);
        }
      }
    }

    return passed;
  }

  function _getPendingCheckpoints() {
    const pending = new Set();

    const cpData = _readYaml('checkpoints.yaml');
    if (cpData?.checkpoints) {
      for (const entries of Object.values(cpData.checkpoints)) {
        if (Array.isArray(entries)) {
          for (const cp of entries) {
            if (cp.status === 'pending' && cp.checkpoint_id) {
              pending.add(cp.checkpoint_id);
            }
          }
        }
      }
    }

    return pending;
  }

  function _readDecisionLog() {
    const data = _readYaml('decision-log.yaml');
    if (data?.decisions && Array.isArray(data.decisions)) {
      return data.decisions;
    }
    return [];
  }

  // -------------------------------------------------------------------------
  // checkPrerequisites
  // -------------------------------------------------------------------------

  function checkPrerequisites(agentId) {
    const normalizedId = _normalizeAgentId(agentId);
    const agentInfo = prereqMap.agents?.[normalizedId];

    if (!agentInfo) {
      return {
        approved: true,
        missing: [],
        message: `Agent ${normalizedId}: no prerequisites (unknown agent)`,
        own_checkpoints: [],
      };
    }

    if (agentInfo.entry_point || !agentInfo.prerequisites || agentInfo.prerequisites.length === 0) {
      return {
        approved: true,
        missing: [],
        message: `Agent ${normalizedId}: entry point / no prerequisites`,
        own_checkpoints: agentInfo.own_checkpoints || [],
      };
    }

    const passed = _getPassedCheckpoints();
    const missing = agentInfo.prerequisites.filter(cp => !passed.has(cp));

    return {
      approved: missing.length === 0,
      missing,
      message: missing.length === 0
        ? `Agent ${normalizedId}: all prerequisites met`
        : `Agent ${normalizedId}: missing ${missing.join(', ')}`,
      own_checkpoints: agentInfo.own_checkpoints || [],
    };
  }

  // -------------------------------------------------------------------------
  // markCheckpoint
  // -------------------------------------------------------------------------

  function markCheckpoint(cpId, decision, rationale) {
    const level = CHECKPOINT_LEVELS[cpId] || 'UNKNOWN';
    const now = new Date().toISOString();

    // --- Update checkpoints.yaml ---
    let cpData = _readYaml('checkpoints.yaml') || { checkpoints: { active: [] } };
    if (!cpData.checkpoints) cpData.checkpoints = { active: [] };
    if (!cpData.checkpoints.active) cpData.checkpoints.active = [];

    cpData.checkpoints.active = cpData.checkpoints.active.filter(
      cp => cp.checkpoint_id !== cpId
    );

    cpData.checkpoints.active.push({
      checkpoint_id: cpId,
      decision,
      rationale,
      level,
      status: 'completed',
      completed_at: now,
    });

    _writeYaml('checkpoints.yaml', cpData);

    // --- Update decision-log.yaml ---
    let dlData = _readYaml('decision-log.yaml') || { decisions: [] };
    if (!Array.isArray(dlData.decisions)) dlData.decisions = [];

    const decisionId = `DEV_${String(dlData.decisions.length + 1).padStart(3, '0')}`;

    dlData.decisions.push({
      decision_id: decisionId,
      checkpoint_id: cpId,
      selected: decision,
      rationale,
      version: 1,
      timestamp: now,
    });

    _writeYaml('decision-log.yaml', dlData);

    // --- Update priority context in .research/ ---
    const systemDir = join(researchDir, '.research');
    if (!existsSync(systemDir)) mkdirSync(systemDir, { recursive: true });

    const contextPath = join(systemDir, 'priority-context.md');
    let contextContent = '';
    if (existsSync(contextPath)) {
      contextContent = readFileSync(contextPath, 'utf8');
    }

    contextContent += `\n${cpId}: ${decision}`;
    if (contextContent.length > 500) {
      contextContent = contextContent.slice(-500);
    }
    writeFileSync(contextPath, contextContent, 'utf8');

    return {
      recorded: true,
      checkpoint_id: cpId,
      decision_id: decisionId,
    };
  }

  // -------------------------------------------------------------------------
  // checkpointStatus
  // -------------------------------------------------------------------------

  function checkpointStatus() {
    const passedSet = _getPassedCheckpoints();
    const passed = [...passedSet];

    const pendingAll = _getPendingCheckpoints();
    const pending = [...pendingAll].filter(cp => !passedSet.has(cp));

    const decisions = _readDecisionLog();
    const total_decisions = decisions.length;

    const blocked = [];
    if (prereqMap.agents) {
      for (const [agentId, agentInfo] of Object.entries(prereqMap.agents)) {
        if (agentInfo.entry_point) continue;
        if (!agentInfo.prerequisites || agentInfo.prerequisites.length === 0) continue;

        const missing = agentInfo.prerequisites.filter(cp => !passedSet.has(cp));
        if (missing.length > 0) {
          blocked.push({ agent: agentId, missing });
        }
      }
    }

    return { passed, pending, blocked, total_decisions };
  }

  // -------------------------------------------------------------------------
  // Return server object
  // -------------------------------------------------------------------------

  return {
    checkPrerequisites,
    markCheckpoint,
    checkpointStatus,
  };
}
