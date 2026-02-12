/**
 * checkpoint-logic.js
 *
 * Pure logic functions extracted from checkpoint-server.js for testability.
 * All functions receive a `researchDir` path (or a getter) so tests can
 * point them at a temporary directory instead of the real project.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import yaml from 'js-yaml';

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function readYaml(filepath) {
  if (!existsSync(filepath)) return null;
  return yaml.load(readFileSync(filepath, 'utf8'));
}

function writeYaml(filepath, data) {
  const dir = dirname(filepath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(filepath, yaml.dump(data, { lineWidth: 120, noRefs: true }), 'utf8');
}

// ---------------------------------------------------------------------------
// Path helpers (take researchDir as argument)
// ---------------------------------------------------------------------------

function decisionLogPath(researchDir) { return join(researchDir, 'decision-log.yaml'); }
function checkpointsPath(researchDir) { return join(researchDir, 'checkpoints.yaml'); }
function projectStatePath(researchDir) { return join(researchDir, 'project-state.yaml'); }
function priorityContextPath(researchDir) { return join(researchDir, 'priority-context.md'); }

// ---------------------------------------------------------------------------
// Exported: createCheckpointLogic(prereqMap, researchDir)
//
// Returns an object with all 7 tool functions bound to the given prereqMap
// and researchDir so they are fully self-contained and side-effect-free
// relative to any global state.
// ---------------------------------------------------------------------------

export function createCheckpointLogic(prereqMap, researchDir) {
  // Ensure the research directory exists
  if (!existsSync(researchDir)) mkdirSync(researchDir, { recursive: true });

  // -- internal helper used by markCheckpoint and decisionAdd -------------
  function updatePriorityContext() {
    const state = readYaml(projectStatePath(researchDir));
    const decisions = readYaml(decisionLogPath(researchDir));
    const cpStatus = checkpointStatus();

    const parts = [];
    if (state?.project?.name) parts.push(`Project: ${state.project.name}`);
    if (state?.research?.paradigm) parts.push(`Paradigm: ${state.research.paradigm}`);
    if (state?.research?.methodology) parts.push(`Method: ${state.research.methodology}`);
    if (state?.research?.question) parts.push(`RQ: ${state.research.question}`);

    const passedStr = cpStatus.passed.map(cp => `\u2705 ${cp}`).join(' ');
    const pendingStr = cpStatus.pending.map(cp => `\u274C ${cp}`).join(' ');
    if (passedStr) parts.push(passedStr);
    if (pendingStr) parts.push(pendingStr);

    if (decisions?.decisions?.length > 0) {
      const last = decisions.decisions[decisions.decisions.length - 1];
      parts.push(`Last: ${last.selected} (${last.timestamp.split('T')[0]})`);
    }

    const ctx = parts.join(' | ');
    if (ctx) priorityWrite(ctx);
  }

  // -- 1. checkPrerequisites ----------------------------------------------
  function checkPrerequisites(agentId) {
    const id = agentId.toLowerCase().replace(/[-_]/g, '');
    const shortId = id.match(/^[a-i]\d+/)?.[0] || id;
    const agent = prereqMap.agents[shortId];

    if (!agent) return { approved: true, missing: [], message: `Agent ${agentId} has no checkpoint requirements.` };
    if (agent.prerequisites.length === 0) return { approved: true, missing: [], message: 'Entry point agent \u2014 no prerequisites.' };

    const checkpoints = readYaml(checkpointsPath(researchDir));
    const decisions = readYaml(decisionLogPath(researchDir));

    const passedCPs = new Set();
    if (checkpoints?.checkpoints) {
      for (const stage of Object.values(checkpoints.checkpoints)) {
        if (Array.isArray(stage)) {
          for (const cp of stage) {
            if (cp.status === 'completed') passedCPs.add(cp.checkpoint_id);
          }
        }
      }
    }
    if (decisions?.decisions) {
      for (const d of decisions.decisions) {
        if (d.checkpoint_id) passedCPs.add(d.checkpoint_id);
      }
    }

    const missing = agent.prerequisites.filter(cp => !passedCPs.has(cp));
    return {
      approved: missing.length === 0,
      missing,
      passed: agent.prerequisites.filter(cp => passedCPs.has(cp)),
      own_checkpoints: agent.own_checkpoints,
      message: missing.length === 0
        ? `All prerequisites met for ${agentId}. Proceed with execution.`
        : `Missing prerequisites: ${missing.join(', ')}. Must complete these via AskUserQuestion before proceeding.`
    };
  }

  // -- 2. markCheckpoint --------------------------------------------------
  function markCheckpoint(checkpointId, decision, rationale) {
    const now = new Date().toISOString();
    const level = prereqMap.checkpoint_levels[checkpointId] || 'unknown';

    // Update checkpoints.yaml
    const data = readYaml(checkpointsPath(researchDir)) || { checkpoints: {}, current_stage: 'active', completed_stages: [] };
    if (!data.checkpoints.active) data.checkpoints.active = [];
    data.checkpoints.active = data.checkpoints.active.filter(cp => cp.checkpoint_id !== checkpointId);
    data.checkpoints.active.push({
      checkpoint_id: checkpointId,
      level: level.toUpperCase(),
      status: 'completed',
      completed_at: now,
      decision,
      rationale
    });
    writeYaml(checkpointsPath(researchDir), data);

    // Update decision-log.yaml
    const log = readYaml(decisionLogPath(researchDir)) || { decisions: [] };
    const decisionId = `DEV_${String(log.decisions.length + 1).padStart(3, '0')}`;
    log.decisions.push({
      decision_id: decisionId,
      checkpoint_id: checkpointId,
      timestamp: now,
      selected: decision,
      rationale,
      version: 1
    });
    writeYaml(decisionLogPath(researchDir), log);

    // Update priority context
    updatePriorityContext();

    return { recorded: true, checkpoint_id: checkpointId, decision_id: decisionId };
  }

  // -- 3. checkpointStatus ------------------------------------------------
  function checkpointStatus() {
    const data = readYaml(checkpointsPath(researchDir));
    const decisions = readYaml(decisionLogPath(researchDir));

    const passed = [];
    const pending = [];

    if (data?.checkpoints) {
      for (const [_stage, cps] of Object.entries(data.checkpoints)) {
        if (Array.isArray(cps)) {
          for (const cp of cps) {
            if (cp.status === 'completed') passed.push(cp.checkpoint_id);
            else pending.push(cp.checkpoint_id);
          }
        }
      }
    }

    // Also check decision log for passed checkpoints
    if (decisions?.decisions) {
      for (const d of decisions.decisions) {
        if (d.checkpoint_id && !passed.includes(d.checkpoint_id)) {
          passed.push(d.checkpoint_id);
        }
      }
    }

    // Determine blocked agents
    const blocked = [];
    for (const [agentId, agent] of Object.entries(prereqMap.agents)) {
      if (agent.prerequisites.length > 0) {
        const missing = agent.prerequisites.filter(cp => !passed.includes(cp));
        if (missing.length > 0) blocked.push({ agent: agentId, missing });
      }
    }

    return { passed, pending, blocked, total_decisions: decisions?.decisions?.length || 0 };
  }

  // -- 4. priorityRead ----------------------------------------------------
  function priorityRead() {
    const path = priorityContextPath(researchDir);
    if (!existsSync(path)) return { context: '', message: 'No priority context set yet.' };
    return { context: readFileSync(path, 'utf8') };
  }

  // -- 5. priorityWrite ---------------------------------------------------
  function priorityWrite(context) {
    if (context.length > 500) {
      context = context.substring(0, 500);
    }
    writeFileSync(priorityContextPath(researchDir), context, 'utf8');
    return { written: true, length: context.length };
  }

  // -- 6. projectStatus ---------------------------------------------------
  function projectStatus() {
    const state = readYaml(projectStatePath(researchDir));
    const decisions = readYaml(decisionLogPath(researchDir));
    const cpStatus = checkpointStatus();

    return {
      project: state?.project || { name: 'Not initialized', message: 'Run /diverga:memory init to set up.' },
      research: state?.research || {},
      checkpoints: cpStatus,
      decisions: decisions?.decisions?.slice(-10) || [],
      total_decisions: decisions?.decisions?.length || 0
    };
  }

  // -- 7. decisionAdd -----------------------------------------------------
  function decisionAdd(checkpointId, selected, rationale, alternativesConsidered) {
    const now = new Date().toISOString();
    const log = readYaml(decisionLogPath(researchDir)) || { decisions: [] };
    const decisionId = `DEV_${String(log.decisions.length + 1).padStart(3, '0')}`;

    const entry = {
      decision_id: decisionId,
      checkpoint_id: checkpointId,
      timestamp: now,
      selected,
      rationale,
      version: 1
    };
    if (alternativesConsidered) entry.alternatives_considered = alternativesConsidered;

    log.decisions.push(entry);
    writeYaml(decisionLogPath(researchDir), log);
    updatePriorityContext();

    return { recorded: true, decision_id: decisionId };
  }

  return {
    checkPrerequisites,
    markCheckpoint,
    checkpointStatus,
    priorityRead,
    priorityWrite,
    projectStatus,
    decisionAdd,
  };
}
