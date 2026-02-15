#!/usr/bin/env node

/**
 * doctor.js - Diagnostics for the Diverga project.
 *
 * Usage:
 *   node scripts/doctor.js
 *
 * Checks Node.js version, git status, version consistency, agent count,
 * SKILL.md presence, MCP server, TypeScript compilation, and package.json scripts.
 */

import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = join(__dirname, '..');

// ANSI colors
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const RESET = '\x1b[0m';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function readJSON(path) {
  return JSON.parse(readFileSync(path, 'utf-8'));
}

function subdirs(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
}

function pass(msg) {
  console.log(`  ${GREEN}\u2713${RESET} ${msg}`);
  return true;
}

function fail(msg) {
  console.log(`  ${RED}\u2717${RESET} ${msg}`);
  return false;
}

// ---------------------------------------------------------------------------
// Checks
// ---------------------------------------------------------------------------

function checkNodeVersion() {
  const raw = process.version; // e.g. "v22.0.0"
  const version = raw.replace(/^v/, '');
  const major = parseInt(version.split('.')[0], 10);
  if (major >= 18) {
    return pass(`Node.js ${raw} (>= 18.0.0)`);
  }
  return fail(`Node.js ${raw} (requires >= 18.0.0)`);
}

function checkGitRepo() {
  try {
    const branch = execSync('git rev-parse --abbrev-ref HEAD', {
      cwd: ROOT,
      encoding: 'utf-8',
    }).trim();
    return pass(`Git repository (branch: ${branch})`);
  } catch {
    return fail('Not a git repository');
  }
}

function checkVersionConsistency() {
  try {
    execSync('node scripts/sync-version.js --check', {
      cwd: ROOT,
      stdio: 'pipe',
    });
    const pkg = readJSON(join(ROOT, 'package.json'));
    return pass(`Version consistency (${pkg.version} across all files)`);
  } catch {
    const pkg = readJSON(join(ROOT, 'package.json'));
    return fail(`Version consistency (drift detected from ${pkg.version})`);
  }
}

function checkAgentCount() {
  const agentsPath = join(ROOT, 'config', 'agents.json');
  if (!existsSync(agentsPath)) {
    return fail('Agent count: config/agents.json not found');
  }
  try {
    const data = readJSON(agentsPath);
    const count = data.agents ? data.agents.length : 0;
    if (count === 44) {
      return pass(`Agent count: ${count} agents in config/agents.json`);
    }
    return fail(`Agent count: ${count} agents in config/agents.json (expected 44)`);
  } catch (e) {
    return fail(`Agent count: failed to parse config/agents.json`);
  }
}

function checkSkillFiles() {
  const agentsPath = join(ROOT, 'config', 'agents.json');
  if (!existsSync(agentsPath)) {
    return fail('SKILL.md files: config/agents.json not found');
  }

  const data = readJSON(agentsPath);
  const agents = data.agents || [];
  let found = 0;
  const missing = [];

  for (const agent of agents) {
    const skillPath = join(ROOT, 'skills', agent.id, 'SKILL.md');
    if (existsSync(skillPath)) {
      found++;
    } else {
      missing.push(agent.id);
    }
  }

  if (found === agents.length) {
    return pass(`SKILL.md files: ${found}/${agents.length} present`);
  }
  return fail(`SKILL.md files: ${found}/${agents.length} present (missing: ${missing.join(', ')})`);
}

function checkCodexSkillFiles() {
  const codexDir = join(ROOT, '.codex', 'skills');
  if (!existsSync(codexDir)) {
    return fail('Codex SKILL.md: .codex/skills/ directory not found');
  }

  const agentsPath = join(ROOT, 'config', 'agents.json');
  if (!existsSync(agentsPath)) {
    return fail('Codex SKILL.md: config/agents.json not found');
  }

  const data = readJSON(agentsPath);
  const agents = data.agents || [];
  let found = 0;
  const missing = [];

  for (const agent of agents) {
    const skillPath = join(codexDir, `diverga-${agent.id}`, 'SKILL.md');
    if (existsSync(skillPath)) {
      found++;
    } else {
      missing.push(agent.id);
    }
  }

  if (found === agents.length) {
    return pass(`Codex SKILL.md: ${found}/${agents.length} present`);
  }
  return fail(`Codex SKILL.md: ${found}/${agents.length} present (missing: ${missing.join(', ')})`);
}

function checkMcpServer() {
  const mcpPath = join(ROOT, 'mcp', 'checkpoint-server.js');
  if (existsSync(mcpPath)) {
    return pass('MCP server: checkpoint-server.js exists');
  }
  return fail('MCP server: checkpoint-server.js not found');
}

function checkTypeScript() {
  try {
    execSync('npx tsc --noEmit', {
      cwd: ROOT,
      stdio: 'pipe',
    });
    return pass('TypeScript: no errors');
  } catch (e) {
    const output = (e.stdout || '').toString();
    const errorLines = output.split('\n').filter(l => l.includes('error TS'));
    const count = errorLines.length;
    if (count > 0) {
      return fail(`TypeScript: ${count} error${count === 1 ? '' : 's'} found`);
    }
    return fail('TypeScript: compilation failed');
  }
}

function checkPackageScripts() {
  const pkg = readJSON(join(ROOT, 'package.json'));
  const scripts = pkg.scripts || {};
  const expected = [
    'build',
    'typecheck',
    'clean',
    'generate',
    'generate:check',
    'version:sync',
    'version:check',
    'release',
  ];

  let found = 0;
  const missing = [];
  for (const name of expected) {
    if (scripts[name]) {
      found++;
    } else {
      missing.push(name);
    }
  }

  if (found === expected.length) {
    return pass(`Package.json: ${found}/${expected.length} scripts defined`);
  }
  return fail(`Package.json: ${found}/${expected.length} scripts defined (missing: ${missing.join(', ')})`);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const pkg = readJSON(join(ROOT, 'package.json'));

  console.log(`\n${BOLD}Diverga Doctor v${pkg.version}${RESET}`);
  console.log('='.repeat(25 + pkg.version.length));
  console.log('');

  const checks = [
    checkNodeVersion,
    checkGitRepo,
    checkVersionConsistency,
    checkAgentCount,
    checkSkillFiles,
    checkCodexSkillFiles,
    checkMcpServer,
    checkTypeScript,
    checkPackageScripts,
  ];

  let passed = 0;
  const total = checks.length;

  for (const check of checks) {
    if (check()) passed++;
  }

  console.log('');
  if (passed === total) {
    console.log(`${GREEN}${BOLD}Summary: ${passed}/${total} checks passed${RESET}`);
  } else {
    console.log(`${RED}${BOLD}Summary: ${passed}/${total} checks passed${RESET}`);
  }
  console.log('');

  process.exit(passed === total ? 0 : 1);
}

main();
