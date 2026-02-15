/**
 * memory-server.js
 *
 * Memory MCP server for Diverga v9.0.
 * Handles project state, decisions, and priority context.
 * Split from checkpoint-server.js in v9.0.
 *
 * Uses YAML files for persistence with dual-path support
 * (research/ preferred, .research/ fallback).
 */

import yaml from 'js-yaml';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { deepMerge } from '../lib/utils.js';

// ---------------------------------------------------------------------------
// createMemoryServer(researchDir) -> server
// ---------------------------------------------------------------------------

export function createMemoryServer(researchDir) {
  if (!researchDir) throw new Error('Research directory is required');

  // Eagerly create both directories
  const _researchPath = join(researchDir, 'research');
  const _systemPath = join(researchDir, '.research');
  if (!existsSync(_researchPath)) mkdirSync(_researchPath, { recursive: true });
  if (!existsSync(_systemPath)) mkdirSync(_systemPath, { recursive: true });

  // -------------------------------------------------------------------------
  // Internal helpers
  // -------------------------------------------------------------------------

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

  function _writeResearchYaml(filename, data) {
    const researchPath = join(researchDir, 'research');
    if (!existsSync(researchPath)) mkdirSync(researchPath, { recursive: true });

    const yamlStr = yaml.dump(data, { lineWidth: 120, noRefs: true });
    writeFileSync(join(researchPath, filename), yamlStr, 'utf8');
  }

  function _ensureSystemDir() {
    const systemDir = join(researchDir, '.research');
    if (!existsSync(systemDir)) mkdirSync(systemDir, { recursive: true });
    return systemDir;
  }

  // -------------------------------------------------------------------------
  // readProjectState
  // -------------------------------------------------------------------------

  function readProjectState() {
    const data = _readYaml('project-state.yaml');
    if (!data || typeof data !== 'object') return {};
    return data;
  }

  // -------------------------------------------------------------------------
  // updateProjectState
  // -------------------------------------------------------------------------

  function updateProjectState(updates) {
    const current = readProjectState();
    const merged = deepMerge(current, updates);

    _writeResearchYaml('project-state.yaml', merged);

    return { updated: true, state: merged };
  }

  // -------------------------------------------------------------------------
  // addDecision
  // -------------------------------------------------------------------------

  function addDecision(checkpointId, selected, rationale, alternatives, metadata) {
    let dlData = _readYaml('decision-log.yaml') || { decisions: [] };
    if (!dlData.decisions || !Array.isArray(dlData.decisions)) {
      dlData.decisions = [];
    }

    const decisionId = `DEV_${String(dlData.decisions.length + 1).padStart(3, '0')}`;
    const now = new Date().toISOString();

    const decision = {
      decision_id: decisionId,
      checkpoint_id: checkpointId,
      selected,
      rationale,
      version: 1,
      timestamp: now,
    };

    if (alternatives && Array.isArray(alternatives) && alternatives.length > 0) {
      decision.alternatives_considered = alternatives;
    }

    if (metadata && typeof metadata === 'object' && Object.keys(metadata).length > 0) {
      decision.metadata = metadata;
    }

    dlData.decisions.push(decision);
    _writeResearchYaml('decision-log.yaml', dlData);

    // Update priority context
    const systemDir = _ensureSystemDir();
    const contextPath = join(systemDir, 'priority-context.md');
    let contextContent = '';
    if (existsSync(contextPath)) {
      contextContent = readFileSync(contextPath, 'utf8');
    }

    contextContent += `\n${checkpointId}: ${selected}`;
    if (contextContent.length > 500) {
      contextContent = contextContent.slice(-500);
    }
    writeFileSync(contextPath, contextContent, 'utf8');

    return { recorded: true, decision_id: decisionId };
  }

  // -------------------------------------------------------------------------
  // listDecisions
  // -------------------------------------------------------------------------

  function listDecisions(filters = {}) {
    const dlData = _readYaml('decision-log.yaml');
    if (!dlData?.decisions || !Array.isArray(dlData.decisions)) return [];

    let decisions = dlData.decisions;

    if (filters.checkpoint_id) {
      decisions = decisions.filter(d => d.checkpoint_id === filters.checkpoint_id);
    }

    if (filters.agent) {
      decisions = decisions.filter(d => d.metadata?.agent === filters.agent);
    }

    if (filters.after) {
      decisions = decisions.filter(d => d.timestamp > filters.after);
    }

    if (filters.before) {
      decisions = decisions.filter(d => d.timestamp < filters.before);
    }

    return decisions;
  }

  // -------------------------------------------------------------------------
  // readPriorityContext
  // -------------------------------------------------------------------------

  function readPriorityContext() {
    const contextPath = join(researchDir, '.research', 'priority-context.md');
    if (!existsSync(contextPath)) return '';
    return readFileSync(contextPath, 'utf8');
  }

  // -------------------------------------------------------------------------
  // writePriorityContext
  // -------------------------------------------------------------------------

  function writePriorityContext(content, maxChars = 500) {
    const systemDir = _ensureSystemDir();
    const contextPath = join(systemDir, 'priority-context.md');

    let truncated = content;
    if (truncated.length > maxChars) {
      truncated = truncated.slice(0, maxChars);
    }

    writeFileSync(contextPath, truncated, 'utf8');

    return { written: true, length: truncated.length };
  }

  // -------------------------------------------------------------------------
  // exportToYaml
  // -------------------------------------------------------------------------

  function exportToYaml() {
    const projectState = readProjectState();
    const decisions = listDecisions();
    const priorityContext = readPriorityContext();

    const exportData = {
      project_state: projectState,
      decisions,
      priority_context: priorityContext,
      exported_at: new Date().toISOString(),
      version: '9.0.0',
    };

    return yaml.dump(exportData, { lineWidth: 120, noRefs: true });
  }

  // -------------------------------------------------------------------------
  // Return server object
  // -------------------------------------------------------------------------

  return {
    readProjectState,
    updateProjectState,
    addDecision,
    listDecisions,
    readPriorityContext,
    writePriorityContext,
    exportToYaml,
  };
}
