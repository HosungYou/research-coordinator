import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..', '..');
const claudeMd = readFileSync(join(ROOT, 'CLAUDE.md'), 'utf8');
const packageJson = JSON.parse(readFileSync(join(ROOT, 'package.json'), 'utf8'));

// =============================================================================
// CLAUDE.md v9.0.0 Documentation Validation Tests
// =============================================================================

describe('CLAUDE.md — Version References', () => {
  it('should have v9.0.0 in the title header', () => {
    assert.match(claudeMd, /# Diverga v9\.0\.0/);
  });

  it('should list v9.0.0 in the version summary block at the top', () => {
    assert.match(claudeMd, /\*\*v9\.0\.0\*\*/);
  });

  it('should have v9.0.0 entry in Version History section', () => {
    assert.match(claudeMd, /- \*\*v9\.0\.0\*\*:/);
  });

  it('should match package.json version', () => {
    assert.equal(packageJson.version, '9.0.0');
    assert.match(claudeMd, new RegExp(`v${packageJson.version}`));
  });

  it('should still reference v8.5.0 in version history (not removed)', () => {
    assert.match(claudeMd, /v8\.5\.0/);
  });
});

describe('CLAUDE.md — MCP Architecture (v9.0)', () => {
  it('should document 16 MCP tools (not 7)', () => {
    assert.match(claudeMd, /16 tools/);
  });

  it('should document the 3-server split', () => {
    assert.match(claudeMd, /checkpoint.*memory.*comm/is);
  });

  it('should document diverga-server.js as the entry point', () => {
    assert.match(claudeMd, /diverga-server\.js/);
  });

  it('should document tool-registry.js', () => {
    assert.match(claudeMd, /tool-registry\.js/);
  });

  it('should list checkpoint tools (3)', () => {
    assert.match(claudeMd, /diverga_check_prerequisites/);
    assert.match(claudeMd, /diverga_mark_checkpoint/);
    assert.match(claudeMd, /diverga_checkpoint_status/);
  });

  it('should list memory tools (7)', () => {
    assert.match(claudeMd, /diverga_project_status/);
    assert.match(claudeMd, /diverga_project_update/);
    assert.match(claudeMd, /diverga_decision_add/);
    assert.match(claudeMd, /diverga_decision_list/);
    assert.match(claudeMd, /diverga_priority_read/);
    assert.match(claudeMd, /diverga_priority_write/);
    assert.match(claudeMd, /diverga_export_yaml/);
  });

  it('should list comm tools (6)', () => {
    assert.match(claudeMd, /diverga_agent_register/);
    assert.match(claudeMd, /diverga_agent_list/);
    assert.match(claudeMd, /diverga_message_send/);
    assert.match(claudeMd, /diverga_message_mailbox/);
    assert.match(claudeMd, /diverga_message_acknowledge/);
    assert.match(claudeMd, /diverga_message_broadcast/);
  });
});

describe('CLAUDE.md — SQLite Backend (v9.0)', () => {
  it('should document SQLite as a backend option', () => {
    assert.match(claudeMd, /SQLite/i);
  });

  it('should document DIVERGA_BACKEND environment variable', () => {
    assert.match(claudeMd, /DIVERGA_BACKEND/);
  });

  it('should document WAL mode', () => {
    assert.match(claudeMd, /WAL/);
  });

  it('should document dual backend (YAML default + SQLite opt-in)', () => {
    assert.match(claudeMd, /YAML.*default/is);
    assert.match(claudeMd, /sqlite/i);
  });

  it('should document auto-migration from YAML to SQLite', () => {
    assert.match(claudeMd, /auto.?migrat/i);
  });
});

describe('CLAUDE.md — Agent Messaging (v9.0)', () => {
  it('should document agent messaging system', () => {
    assert.match(claudeMd, /agent.*messag/i);
  });

  it('should document register, send, mailbox, broadcast operations', () => {
    assert.match(claudeMd, /register/i);
    assert.match(claudeMd, /broadcast/i);
    assert.match(claudeMd, /mailbox/i);
  });
});

describe('CLAUDE.md — Structural Integrity', () => {
  it('should have all major sections', () => {
    const sections = [
      'Project Overview',
      'Quick Start',
      'Memory System',
      'Human Checkpoint System',
      'Checkpoint Enforcement Protocol',
      'Agent Structure',
      'Model Routing',
      'Version History',
    ];
    for (const section of sections) {
      assert.match(claudeMd, new RegExp(`##.*${section}`, 'i'),
        `Missing section: ${section}`);
    }
  });

  it('should have MCP Server Architecture section', () => {
    assert.match(claudeMd, /##.*MCP.*Server/i);
  });

  it('should document 44 agents total', () => {
    assert.match(claudeMd, /44.*agent/i);
  });

  it('should reference the MCP enforcement in checkpoint rules', () => {
    assert.match(claudeMd, /MCP.*enforcement|diverga_check_prerequisites/i);
  });
});
