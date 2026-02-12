/**
 * Comprehensive tests for checkpoint-logic.js
 *
 * Uses Node.js built-in test runner (node:test) and assert module.
 * Each test suite creates an isolated temporary directory for .research/ state
 * and cleans up after itself.
 */

import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import yaml from 'js-yaml';
import { createCheckpointLogic } from '../lib/checkpoint-logic.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PREREQ_MAP = JSON.parse(readFileSync(join(__dirname, '..', 'agent-prerequisite-map.json'), 'utf8'));

/**
 * Helper: create a fresh temp dir and logic instance for each suite.
 */
function createTestContext() {
  const tmpDir = mkdtempSync(join(tmpdir(), 'checkpoint-test-'));
  const logic = createCheckpointLogic(PREREQ_MAP, tmpDir);
  return { tmpDir, logic };
}

function cleanup(tmpDir) {
  rmSync(tmpDir, { recursive: true, force: true });
}

/** Write a YAML file into the temp research dir */
function writeTestYaml(tmpDir, filename, data) {
  const filepath = join(tmpDir, filename);
  const dir = dirname(filepath);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(filepath, yaml.dump(data, { lineWidth: 120, noRefs: true }), 'utf8');
}

/** Read a YAML file from the temp research dir */
function readTestYaml(tmpDir, filename) {
  const filepath = join(tmpDir, filename);
  if (!existsSync(filepath)) return null;
  return yaml.load(readFileSync(filepath, 'utf8'));
}

// ===========================================================================
// 1. checkPrerequisites
// ===========================================================================

describe('checkPrerequisites', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  after(() => {
    // cleanup last tmpDir; beforeEach creates new ones
  });

  it('entry point agent (a1) returns approved:true with no prerequisites', () => {
    const result = logic.checkPrerequisites('a1');
    assert.equal(result.approved, true);
    assert.deepEqual(result.missing, []);
    assert.match(result.message, /entry point|no prerequisites/i);
    cleanup(tmpDir);
  });

  it('agent with no checkpoint requirements (a4) returns approved:true', () => {
    const result = logic.checkPrerequisites('a4');
    assert.equal(result.approved, true);
    assert.deepEqual(result.missing, []);
    cleanup(tmpDir);
  });

  it('agent with unmet prerequisites returns approved:false and missing list', () => {
    // c5 requires CP_RESEARCH_DIRECTION and CP_METHODOLOGY_APPROVAL
    const result = logic.checkPrerequisites('c5');
    assert.equal(result.approved, false);
    assert.ok(result.missing.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.missing.includes('CP_METHODOLOGY_APPROVAL'));
    assert.equal(result.missing.length, 2);
    assert.match(result.message, /Missing prerequisites/);
    cleanup(tmpDir);
  });

  it('agent with all prerequisites met returns approved:true', () => {
    // Pre-populate checkpoints for c5's requirements
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
          { checkpoint_id: 'CP_METHODOLOGY_APPROVAL', status: 'completed' },
        ]
      }
    });

    const result = logic.checkPrerequisites('c5');
    assert.equal(result.approved, true);
    assert.deepEqual(result.missing, []);
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.passed.includes('CP_METHODOLOGY_APPROVAL'));
    assert.match(result.message, /All prerequisites met/);
    cleanup(tmpDir);
  });

  it('normalizes agent IDs: "C5", "c5", "c5-meta-analysis" all resolve to c5', () => {
    const r1 = logic.checkPrerequisites('C5');
    const r2 = logic.checkPrerequisites('c5');
    const r3 = logic.checkPrerequisites('c5-meta-analysis');
    const r4 = logic.checkPrerequisites('C5_MetaAnalysis_Master');

    // All should resolve to agent c5 (which has prerequisites)
    assert.equal(r1.approved, false);
    assert.equal(r2.approved, false);
    assert.equal(r3.approved, false);
    assert.equal(r4.approved, false);

    // All should have the same missing set
    assert.deepEqual(r1.missing, r2.missing);
    assert.deepEqual(r2.missing, r3.missing);
    assert.deepEqual(r3.missing, r4.missing);
    cleanup(tmpDir);
  });

  it('unknown agent returns approved:true (no restrictions)', () => {
    const result = logic.checkPrerequisites('z99-unknown-agent');
    assert.equal(result.approved, true);
    assert.deepEqual(result.missing, []);
    assert.match(result.message, /no checkpoint requirements/);
    cleanup(tmpDir);
  });

  it('recognizes prerequisites met via decision-log.yaml', () => {
    // a2 requires CP_RESEARCH_DIRECTION - put it in decision log instead of checkpoints
    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { checkpoint_id: 'CP_RESEARCH_DIRECTION', selected: 'AI in education', rationale: 'test' }
      ]
    });

    const result = logic.checkPrerequisites('a2');
    assert.equal(result.approved, true);
    assert.deepEqual(result.missing, []);
    cleanup(tmpDir);
  });

  it('partially met prerequisites shows correct missing and passed', () => {
    // c1 requires CP_PARADIGM_SELECTION and CP_RESEARCH_DIRECTION
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
        ]
      }
    });

    const result = logic.checkPrerequisites('c1');
    assert.equal(result.approved, false);
    assert.ok(result.missing.includes('CP_PARADIGM_SELECTION'));
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.equal(result.missing.length, 1);
    assert.equal(result.passed.length, 1);
    cleanup(tmpDir);
  });

  it('returns own_checkpoints for agents with prerequisites', () => {
    // a2 has prerequisites so it goes through the full code path that returns own_checkpoints
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
        ]
      }
    });
    const result = logic.checkPrerequisites('a2');
    assert.ok(Array.isArray(result.own_checkpoints));
    assert.ok(result.own_checkpoints.length > 0);
    assert.ok(result.own_checkpoints.some(cp => cp.id === 'CP_THEORY_SELECTION'));
    cleanup(tmpDir);
  });

  it('entry point agents return early without own_checkpoints field', () => {
    // a1 is an entry point and returns early, so own_checkpoints is not included
    const result = logic.checkPrerequisites('a1');
    assert.equal(result.approved, true);
    // The early-return path does not include own_checkpoints
    assert.equal(result.own_checkpoints, undefined);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 2. markCheckpoint
// ===========================================================================

describe('markCheckpoint', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  it('creates checkpoints.yaml if it does not exist', () => {
    assert.equal(existsSync(join(tmpDir, 'checkpoints.yaml')), false);

    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core research area');

    assert.equal(existsSync(join(tmpDir, 'checkpoints.yaml')), true);
    const data = readTestYaml(tmpDir, 'checkpoints.yaml');
    assert.ok(data.checkpoints.active.length > 0);
    cleanup(tmpDir);
  });

  it('creates decision-log.yaml if it does not exist', () => {
    assert.equal(existsSync(join(tmpDir, 'decision-log.yaml')), false);

    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core research area');

    assert.equal(existsSync(join(tmpDir, 'decision-log.yaml')), true);
    const data = readTestYaml(tmpDir, 'decision-log.yaml');
    assert.ok(data.decisions.length === 1);
    cleanup(tmpDir);
  });

  it('records checkpoint with correct structure in checkpoints.yaml', () => {
    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core research area');

    const data = readTestYaml(tmpDir, 'checkpoints.yaml');
    const cp = data.checkpoints.active[0];
    assert.equal(cp.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(cp.level, 'REQUIRED');
    assert.equal(cp.status, 'completed');
    assert.equal(cp.decision, 'AI in education');
    assert.equal(cp.rationale, 'Core research area');
    assert.ok(cp.completed_at); // ISO timestamp present
    cleanup(tmpDir);
  });

  it('records correct structure in decision-log.yaml', () => {
    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core research area');

    const data = readTestYaml(tmpDir, 'decision-log.yaml');
    const d = data.decisions[0];
    assert.equal(d.decision_id, 'DEV_001');
    assert.equal(d.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(d.selected, 'AI in education');
    assert.equal(d.rationale, 'Core research area');
    assert.equal(d.version, 1);
    assert.ok(d.timestamp);
    cleanup(tmpDir);
  });

  it('generates sequential decision IDs (DEV_001, DEV_002, ...)', () => {
    const r1 = logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'Decision 1', 'Rationale 1');
    const r2 = logic.markCheckpoint('CP_PARADIGM_SELECTION', 'Decision 2', 'Rationale 2');
    const r3 = logic.markCheckpoint('CP_THEORY_SELECTION', 'Decision 3', 'Rationale 3');

    assert.equal(r1.decision_id, 'DEV_001');
    assert.equal(r2.decision_id, 'DEV_002');
    assert.equal(r3.decision_id, 'DEV_003');

    const data = readTestYaml(tmpDir, 'decision-log.yaml');
    assert.equal(data.decisions.length, 3);
    cleanup(tmpDir);
  });

  it('updates priority context after marking', () => {
    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core');

    assert.equal(existsSync(join(tmpDir, 'priority-context.md')), true);
    const ctx = readFileSync(join(tmpDir, 'priority-context.md'), 'utf8');
    assert.ok(ctx.length > 0);
    // Should mention the checkpoint
    assert.ok(ctx.includes('CP_RESEARCH_DIRECTION'));
    cleanup(tmpDir);
  });

  it('replaces pending entry if exists for same checkpoint', () => {
    // Pre-populate with a pending entry
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'pending', level: 'REQUIRED' }
        ]
      },
      current_stage: 'active',
      completed_stages: []
    });

    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'Final decision', 'Updated rationale');

    const data = readTestYaml(tmpDir, 'checkpoints.yaml');
    // Should have exactly one entry, not two
    const matching = data.checkpoints.active.filter(cp => cp.checkpoint_id === 'CP_RESEARCH_DIRECTION');
    assert.equal(matching.length, 1);
    assert.equal(matching[0].status, 'completed');
    assert.equal(matching[0].decision, 'Final decision');
    cleanup(tmpDir);
  });

  it('returns correct response shape', () => {
    const result = logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'test', 'test');
    assert.equal(result.recorded, true);
    assert.equal(result.checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(result.decision_id, 'DEV_001');
    cleanup(tmpDir);
  });

  it('handles unknown checkpoint level gracefully', () => {
    const result = logic.markCheckpoint('UNKNOWN_CP_999', 'decision', 'rationale');
    assert.equal(result.recorded, true);

    const data = readTestYaml(tmpDir, 'checkpoints.yaml');
    const cp = data.checkpoints.active[0];
    assert.equal(cp.level, 'UNKNOWN');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 3. checkpointStatus
// ===========================================================================

describe('checkpointStatus', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  it('returns empty arrays when no checkpoints exist', () => {
    const result = logic.checkpointStatus();
    assert.deepEqual(result.passed, []);
    assert.deepEqual(result.pending, []);
    assert.equal(result.total_decisions, 0);
    assert.ok(Array.isArray(result.blocked));
    // blocked should list all agents that have prerequisites
    assert.ok(result.blocked.length > 0);
    cleanup(tmpDir);
  });

  it('returns passed checkpoints from checkpoints.yaml', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
          { checkpoint_id: 'CP_PARADIGM_SELECTION', status: 'completed' },
        ]
      }
    });

    const result = logic.checkpointStatus();
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.passed.includes('CP_PARADIGM_SELECTION'));
    assert.equal(result.passed.length, 2);
    cleanup(tmpDir);
  });

  it('returns passed checkpoints from decision-log.yaml', () => {
    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { checkpoint_id: 'CP_THEORY_SELECTION', selected: 'TAM', rationale: 'Well-established' },
      ]
    });

    const result = logic.checkpointStatus();
    assert.ok(result.passed.includes('CP_THEORY_SELECTION'));
    cleanup(tmpDir);
  });

  it('lists pending checkpoints correctly', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
          { checkpoint_id: 'CP_PARADIGM_SELECTION', status: 'pending' },
        ]
      }
    });

    const result = logic.checkpointStatus();
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.pending.includes('CP_PARADIGM_SELECTION'));
    cleanup(tmpDir);
  });

  it('lists blocked agents correctly', () => {
    // No checkpoints passed => agents with prerequisites are blocked
    const result = logic.checkpointStatus();

    // c5 requires CP_RESEARCH_DIRECTION and CP_METHODOLOGY_APPROVAL
    const c5blocked = result.blocked.find(b => b.agent === 'c5');
    assert.ok(c5blocked, 'c5 should be in blocked list');
    assert.ok(c5blocked.missing.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(c5blocked.missing.includes('CP_METHODOLOGY_APPROVAL'));
    cleanup(tmpDir);
  });

  it('unblocks agents when their prerequisites are met', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
        ]
      }
    });

    const result = logic.checkpointStatus();
    // a2 only requires CP_RESEARCH_DIRECTION, so it should NOT be blocked
    const a2blocked = result.blocked.find(b => b.agent === 'a2');
    assert.equal(a2blocked, undefined, 'a2 should not be blocked when CP_RESEARCH_DIRECTION is passed');
    cleanup(tmpDir);
  });

  it('deduplicates checkpoints from both sources', () => {
    // Same checkpoint in both checkpoints.yaml and decision-log.yaml
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
        ]
      }
    });
    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { checkpoint_id: 'CP_RESEARCH_DIRECTION', selected: 'AI', rationale: 'test' },
      ]
    });

    const result = logic.checkpointStatus();
    const cpCount = result.passed.filter(cp => cp === 'CP_RESEARCH_DIRECTION').length;
    assert.equal(cpCount, 1, 'Should not duplicate CP_RESEARCH_DIRECTION');
    cleanup(tmpDir);
  });

  it('returns total_decisions count', () => {
    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { checkpoint_id: 'CP_A', selected: 'x', rationale: 'r' },
        { checkpoint_id: 'CP_B', selected: 'y', rationale: 'r' },
        { checkpoint_id: 'CP_C', selected: 'z', rationale: 'r' },
      ]
    });

    const result = logic.checkpointStatus();
    assert.equal(result.total_decisions, 3);
    cleanup(tmpDir);
  });

  it('handles multiple stages in checkpoints.yaml', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        stage1: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
        ],
        stage2: [
          { checkpoint_id: 'CP_PARADIGM_SELECTION', status: 'completed' },
        ],
        active: [
          { checkpoint_id: 'CP_METHODOLOGY_APPROVAL', status: 'pending' },
        ]
      }
    });

    const result = logic.checkpointStatus();
    assert.ok(result.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(result.passed.includes('CP_PARADIGM_SELECTION'));
    assert.ok(result.pending.includes('CP_METHODOLOGY_APPROVAL'));
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 4. priorityRead
// ===========================================================================

describe('priorityRead', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  it('returns empty context and message when file does not exist', () => {
    const result = logic.priorityRead();
    assert.equal(result.context, '');
    assert.ok(result.message);
    assert.match(result.message, /No priority context/);
    cleanup(tmpDir);
  });

  it('returns file content when file exists', () => {
    const content = 'Project: AI Study | Paradigm: Quantitative';
    writeFileSync(join(tmpDir, 'priority-context.md'), content, 'utf8');

    const result = logic.priorityRead();
    assert.equal(result.context, content);
    assert.equal(result.message, undefined); // no message when content exists
    cleanup(tmpDir);
  });

  it('returns exact content without modification', () => {
    const content = 'Special chars: @#$% & newlines\nline2\nline3';
    writeFileSync(join(tmpDir, 'priority-context.md'), content, 'utf8');

    const result = logic.priorityRead();
    assert.equal(result.context, content);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 5. priorityWrite
// ===========================================================================

describe('priorityWrite', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  it('writes context to file', () => {
    const result = logic.priorityWrite('Hello priority context');
    assert.equal(result.written, true);
    assert.equal(result.length, 'Hello priority context'.length);

    const content = readFileSync(join(tmpDir, 'priority-context.md'), 'utf8');
    assert.equal(content, 'Hello priority context');
    cleanup(tmpDir);
  });

  it('truncates to 500 chars if longer', () => {
    const longText = 'A'.repeat(600);
    const result = logic.priorityWrite(longText);

    assert.equal(result.written, true);
    assert.equal(result.length, 500);

    const content = readFileSync(join(tmpDir, 'priority-context.md'), 'utf8');
    assert.equal(content.length, 500);
    cleanup(tmpDir);
  });

  it('does not truncate text at exactly 500 chars', () => {
    const exact500 = 'B'.repeat(500);
    const result = logic.priorityWrite(exact500);

    assert.equal(result.length, 500);

    const content = readFileSync(join(tmpDir, 'priority-context.md'), 'utf8');
    assert.equal(content.length, 500);
    cleanup(tmpDir);
  });

  it('does not truncate text under 500 chars', () => {
    const shortText = 'C'.repeat(499);
    const result = logic.priorityWrite(shortText);

    assert.equal(result.length, 499);
    cleanup(tmpDir);
  });

  it('returns written:true and length', () => {
    const result = logic.priorityWrite('test');
    assert.equal(result.written, true);
    assert.equal(typeof result.length, 'number');
    assert.equal(result.length, 4);
    cleanup(tmpDir);
  });

  it('overwrites existing content', () => {
    logic.priorityWrite('first');
    logic.priorityWrite('second');

    const content = readFileSync(join(tmpDir, 'priority-context.md'), 'utf8');
    assert.equal(content, 'second');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 6. projectStatus
// ===========================================================================

describe('projectStatus', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  it('returns "Not initialized" when no project-state.yaml', () => {
    const result = logic.projectStatus();
    assert.equal(result.project.name, 'Not initialized');
    assert.ok(result.project.message);
    assert.deepEqual(result.research, {});
    assert.deepEqual(result.decisions, []);
    assert.equal(result.total_decisions, 0);
    cleanup(tmpDir);
  });

  it('returns project data when files exist', () => {
    writeTestYaml(tmpDir, 'project-state.yaml', {
      project: { name: 'AI Education Study', created: '2025-01-01' },
      research: {
        paradigm: 'quantitative',
        methodology: 'meta-analysis',
        question: 'How does AI improve learning outcomes?'
      }
    });

    const result = logic.projectStatus();
    assert.equal(result.project.name, 'AI Education Study');
    assert.equal(result.research.paradigm, 'quantitative');
    assert.equal(result.research.methodology, 'meta-analysis');
    assert.equal(result.research.question, 'How does AI improve learning outcomes?');
    cleanup(tmpDir);
  });

  it('includes checkpoint status', () => {
    writeTestYaml(tmpDir, 'checkpoints.yaml', {
      checkpoints: {
        active: [
          { checkpoint_id: 'CP_RESEARCH_DIRECTION', status: 'completed' },
        ]
      }
    });

    const result = logic.projectStatus();
    assert.ok(result.checkpoints);
    assert.ok(result.checkpoints.passed.includes('CP_RESEARCH_DIRECTION'));
    cleanup(tmpDir);
  });

  it('includes last 10 decisions', () => {
    const decisions = [];
    for (let i = 1; i <= 15; i++) {
      decisions.push({
        decision_id: `DEV_${String(i).padStart(3, '0')}`,
        checkpoint_id: `CP_TEST_${i}`,
        selected: `Decision ${i}`,
        rationale: `Rationale ${i}`,
        timestamp: new Date().toISOString(),
        version: 1
      });
    }
    writeTestYaml(tmpDir, 'decision-log.yaml', { decisions });

    const result = logic.projectStatus();
    assert.equal(result.decisions.length, 10);
    assert.equal(result.total_decisions, 15);
    // Should be the last 10 (items 6-15)
    assert.equal(result.decisions[0].decision_id, 'DEV_006');
    assert.equal(result.decisions[9].decision_id, 'DEV_015');
    cleanup(tmpDir);
  });

  it('returns empty decisions array when no decision log', () => {
    const result = logic.projectStatus();
    assert.deepEqual(result.decisions, []);
    assert.equal(result.total_decisions, 0);
    cleanup(tmpDir);
  });

  it('returns full decisions when fewer than 10', () => {
    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x', rationale: 'r', timestamp: new Date().toISOString(), version: 1 },
        { decision_id: 'DEV_002', checkpoint_id: 'CP_B', selected: 'y', rationale: 'r', timestamp: new Date().toISOString(), version: 1 },
      ]
    });

    const result = logic.projectStatus();
    assert.equal(result.decisions.length, 2);
    assert.equal(result.total_decisions, 2);
    cleanup(tmpDir);
  });
});

// ===========================================================================
// 7. decisionAdd
// ===========================================================================

describe('decisionAdd', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  it('adds decision to log', () => {
    const result = logic.decisionAdd('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus area');

    assert.equal(result.recorded, true);
    assert.equal(result.decision_id, 'DEV_001');

    const data = readTestYaml(tmpDir, 'decision-log.yaml');
    assert.equal(data.decisions.length, 1);
    assert.equal(data.decisions[0].checkpoint_id, 'CP_RESEARCH_DIRECTION');
    assert.equal(data.decisions[0].selected, 'AI in education');
    assert.equal(data.decisions[0].rationale, 'Core focus area');
    assert.equal(data.decisions[0].version, 1);
    assert.ok(data.decisions[0].timestamp);
    cleanup(tmpDir);
  });

  it('generates sequential decision IDs', () => {
    const r1 = logic.decisionAdd('CP_A', 'sel1', 'rat1');
    const r2 = logic.decisionAdd('CP_B', 'sel2', 'rat2');
    const r3 = logic.decisionAdd('CP_C', 'sel3', 'rat3');

    assert.equal(r1.decision_id, 'DEV_001');
    assert.equal(r2.decision_id, 'DEV_002');
    assert.equal(r3.decision_id, 'DEV_003');
    cleanup(tmpDir);
  });

  it('includes alternatives_considered when provided', () => {
    logic.decisionAdd(
      'CP_PARADIGM_SELECTION',
      'Quantitative',
      'Best fit for RCT design',
      ['Qualitative', 'Mixed Methods']
    );

    const data = readTestYaml(tmpDir, 'decision-log.yaml');
    const d = data.decisions[0];
    assert.ok(Array.isArray(d.alternatives_considered));
    assert.deepEqual(d.alternatives_considered, ['Qualitative', 'Mixed Methods']);
    cleanup(tmpDir);
  });

  it('omits alternatives_considered when not provided', () => {
    logic.decisionAdd('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus');

    const data = readTestYaml(tmpDir, 'decision-log.yaml');
    const d = data.decisions[0];
    assert.equal(d.alternatives_considered, undefined);
    cleanup(tmpDir);
  });

  it('updates priority context after adding decision', () => {
    logic.decisionAdd('CP_RESEARCH_DIRECTION', 'AI in education', 'Core focus');

    assert.equal(existsSync(join(tmpDir, 'priority-context.md')), true);
    const ctx = readFileSync(join(tmpDir, 'priority-context.md'), 'utf8');
    assert.ok(ctx.length > 0);
    cleanup(tmpDir);
  });

  it('creates decision-log.yaml if it does not exist', () => {
    assert.equal(existsSync(join(tmpDir, 'decision-log.yaml')), false);

    logic.decisionAdd('CP_RESEARCH_DIRECTION', 'test', 'test');

    assert.equal(existsSync(join(tmpDir, 'decision-log.yaml')), true);
    cleanup(tmpDir);
  });

  it('appends to existing decision log', () => {
    writeTestYaml(tmpDir, 'decision-log.yaml', {
      decisions: [
        { decision_id: 'DEV_001', checkpoint_id: 'CP_A', selected: 'x', rationale: 'r', timestamp: '2025-01-01T00:00:00Z', version: 1 }
      ]
    });

    logic.decisionAdd('CP_B', 'y', 'r2');

    const data = readTestYaml(tmpDir, 'decision-log.yaml');
    assert.equal(data.decisions.length, 2);
    assert.equal(data.decisions[1].decision_id, 'DEV_002');
    assert.equal(data.decisions[1].checkpoint_id, 'CP_B');
    cleanup(tmpDir);
  });
});

// ===========================================================================
// Integration: cross-function behavior
// ===========================================================================

describe('integration: cross-function behavior', () => {
  let tmpDir, logic;

  beforeEach(() => {
    ({ tmpDir, logic } = createTestContext());
  });

  it('markCheckpoint makes prerequisites pass for dependent agents', () => {
    // Before: a2 is blocked (needs CP_RESEARCH_DIRECTION)
    const before = logic.checkPrerequisites('a2');
    assert.equal(before.approved, false);

    // Mark the prerequisite
    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI in education', 'Core topic');

    // After: a2 should be approved
    const after = logic.checkPrerequisites('a2');
    assert.equal(after.approved, true);
    cleanup(tmpDir);
  });

  it('decisionAdd makes prerequisites pass for dependent agents', () => {
    const before = logic.checkPrerequisites('a2');
    assert.equal(before.approved, false);

    logic.decisionAdd('CP_RESEARCH_DIRECTION', 'AI in education', 'Core topic');

    const after = logic.checkPrerequisites('a2');
    assert.equal(after.approved, true);
    cleanup(tmpDir);
  });

  it('checkpointStatus reflects markCheckpoint changes', () => {
    const before = logic.checkpointStatus();
    assert.equal(before.passed.length, 0);

    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI', 'test');
    logic.markCheckpoint('CP_PARADIGM_SELECTION', 'Quantitative', 'test');

    const after = logic.checkpointStatus();
    assert.ok(after.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(after.passed.includes('CP_PARADIGM_SELECTION'));
    assert.equal(after.total_decisions, 2);
    cleanup(tmpDir);
  });

  it('projectStatus integrates project state, decisions, and checkpoints', () => {
    writeTestYaml(tmpDir, 'project-state.yaml', {
      project: { name: 'Integration Test' },
      research: { paradigm: 'mixed', question: 'Does X affect Y?' }
    });

    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'X affects Y', 'Core');
    logic.decisionAdd('CP_PARADIGM_SELECTION', 'Mixed Methods', 'Best fit');

    const status = logic.projectStatus();
    assert.equal(status.project.name, 'Integration Test');
    assert.equal(status.research.paradigm, 'mixed');
    // markCheckpoint writes 1 entry to decision-log, decisionAdd writes 1 entry = 2 total
    assert.equal(status.total_decisions, 2);
    assert.ok(status.checkpoints.passed.length > 0);
    cleanup(tmpDir);
  });

  it('priority context auto-updates reflect project state', () => {
    writeTestYaml(tmpDir, 'project-state.yaml', {
      project: { name: 'Context Test' },
      research: { paradigm: 'quantitative', question: 'How?' }
    });

    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'test', 'test');

    const ctx = logic.priorityRead();
    assert.ok(ctx.context.includes('Project: Context Test'));
    assert.ok(ctx.context.includes('Paradigm: quantitative'));
    assert.ok(ctx.context.includes('RQ: How?'));
    cleanup(tmpDir);
  });

  it('full pipeline: mark multiple checkpoints to unblock deep agents', () => {
    // c5 requires CP_RESEARCH_DIRECTION + CP_METHODOLOGY_APPROVAL

    // Step 1: c5 blocked
    assert.equal(logic.checkPrerequisites('c5').approved, false);

    // Step 2: mark first prerequisite
    logic.markCheckpoint('CP_RESEARCH_DIRECTION', 'AI Learning', 'Core');
    assert.equal(logic.checkPrerequisites('c5').approved, false); // still missing one

    // Step 3: mark second prerequisite
    logic.markCheckpoint('CP_METHODOLOGY_APPROVAL', 'Meta-analysis', 'Best fit');
    assert.equal(logic.checkPrerequisites('c5').approved, true); // now approved

    // Step 4: verify checkpoint status is consistent
    const status = logic.checkpointStatus();
    assert.ok(status.passed.includes('CP_RESEARCH_DIRECTION'));
    assert.ok(status.passed.includes('CP_METHODOLOGY_APPROVAL'));

    // Step 5: c5 should not be in blocked list
    const c5blocked = status.blocked.find(b => b.agent === 'c5');
    assert.equal(c5blocked, undefined, 'c5 should not be blocked');
    cleanup(tmpDir);
  });
});
