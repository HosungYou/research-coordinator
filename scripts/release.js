#!/usr/bin/env node

/**
 * release.js - Automate version bumps, changelog updates, and git tagging.
 *
 * Usage:
 *   node scripts/release.js patch          # 8.4.0 → 8.4.1
 *   node scripts/release.js minor          # 8.4.0 → 8.5.0
 *   node scripts/release.js major          # 8.4.0 → 9.0.0
 *   node scripts/release.js 9.1.0          # explicit version
 *   node scripts/release.js patch --dry-run # preview without changes
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = join(__dirname, '..');

// ANSI colors
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const RESET = '\x1b[0m';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function readJSON(path) {
  return JSON.parse(readFileSync(path, 'utf-8'));
}

function writeJSON(path, data) {
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n', 'utf-8');
}

function run(cmd, opts = {}) {
  console.log(`  ${DIM}$ ${cmd}${RESET}`);
  try {
    execSync(cmd, { cwd: ROOT, stdio: 'inherit', ...opts });
    return true;
  } catch (e) {
    if (opts.allowFailure) return false;
    throw e;
  }
}

function today() {
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}

function bumpVersion(current, bump) {
  const [major, minor, patch] = current.split('.').map(Number);
  switch (bump) {
    case 'patch': return `${major}.${minor}.${patch + 1}`;
    case 'minor': return `${major}.${minor + 1}.0`;
    case 'major': return `${major + 1}.0.0`;
    default: return bump; // explicit version
  }
}

function isValidVersion(v) {
  return /^\d+\.\d+\.\d+$/.test(v);
}

// ---------------------------------------------------------------------------
// Git checks
// ---------------------------------------------------------------------------

function checkGitClean() {
  try {
    const status = execSync('git status --porcelain', { cwd: ROOT, encoding: 'utf-8' });
    if (status.trim().length > 0) {
      console.log(`\n${YELLOW}Warning:${RESET} Working tree is not clean:\n`);
      console.log(status);
      return false;
    }
    return true;
  } catch {
    console.log(`${YELLOW}Warning:${RESET} Unable to check git status.`);
    return false;
  }
}

// ---------------------------------------------------------------------------
// Changelog
// ---------------------------------------------------------------------------

function prependChangelog(oldVersion, newVersion) {
  const changelogPath = join(ROOT, 'CHANGELOG.md');
  if (!existsSync(changelogPath)) {
    console.log(`  ${YELLOW}Warning:${RESET} CHANGELOG.md not found, creating one.`);
    writeFileSync(changelogPath, '# Changelog\n\n', 'utf-8');
  }

  const existing = readFileSync(changelogPath, 'utf-8');
  const entry = `## [${newVersion}] - ${today()}

### Added
- (placeholder for release notes)

### Changed
- Version bumped from ${oldVersion} to ${newVersion}

`;

  // Insert after the first heading line(s) and any blank lines / separators
  const headerMatch = existing.match(/^(# Changelog\n(?:\n|---\n)*)/);
  let updated;
  if (headerMatch) {
    const headerEnd = headerMatch[0].length;
    updated = existing.slice(0, headerEnd) + '\n' + entry + existing.slice(headerEnd);
  } else {
    updated = entry + existing;
  }

  writeFileSync(changelogPath, updated, 'utf-8');
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const bump = args.find(a => !a.startsWith('-'));

  if (!bump) {
    console.log(`\n${RED}Error:${RESET} Missing version bump argument.\n`);
    console.log(`Usage: node scripts/release.js [patch|minor|major|X.Y.Z] [--dry-run]\n`);
    process.exit(1);
  }

  // Validate bump type
  const validBumps = ['patch', 'minor', 'major'];
  if (!validBumps.includes(bump) && !isValidVersion(bump)) {
    console.log(`\n${RED}Error:${RESET} Invalid bump "${bump}". Use patch, minor, major, or X.Y.Z\n`);
    process.exit(1);
  }

  // Check git state
  console.log(`\n${BOLD}${CYAN}release${RESET}  ${dryRun ? `${YELLOW}(dry run)${RESET} ` : ''}Preparing release...\n`);
  checkGitClean();

  // Read current version
  const pkgPath = join(ROOT, 'package.json');
  const pkg = readJSON(pkgPath);
  const oldVersion = pkg.version;
  const newVersion = bumpVersion(oldVersion, bump);

  if (!isValidVersion(newVersion)) {
    console.log(`${RED}Error:${RESET} Computed version "${newVersion}" is invalid.\n`);
    process.exit(1);
  }

  if (newVersion === oldVersion) {
    console.log(`${YELLOW}Warning:${RESET} New version is the same as current (${oldVersion}). Nothing to do.\n`);
    process.exit(0);
  }

  console.log(`  ${DIM}Current version:${RESET}  ${oldVersion}`);
  console.log(`  ${DIM}New version:${RESET}      ${GREEN}${newVersion}${RESET}`);
  console.log(`  ${DIM}Bump type:${RESET}        ${bump}`);
  console.log('');

  if (dryRun) {
    console.log(`${BOLD}Dry run summary:${RESET}`);
    console.log(`  1. Update package.json  ${oldVersion} → ${newVersion}`);
    console.log(`  2. Run sync-version.js --fix`);
    console.log(`  3. Run generate.js --write (if exists)`);
    console.log(`  4. Prepend CHANGELOG.md entry`);
    console.log(`  5. git add -A && git commit -m "release: v${newVersion}"`);
    console.log(`  6. git tag v${newVersion}`);
    console.log(`\n${YELLOW}Dry run complete. No changes made.${RESET}\n`);
    process.exit(0);
  }

  // Step 1: Update package.json
  console.log(`${CYAN}Step 1:${RESET} Updating package.json...`);
  pkg.version = newVersion;
  writeJSON(pkgPath, pkg);
  console.log(`  ${GREEN}\u2713${RESET} package.json updated to ${newVersion}\n`);

  // Step 2: Run sync-version.js --fix
  console.log(`${CYAN}Step 2:${RESET} Syncing versions across files...`);
  run('node scripts/sync-version.js --fix');
  console.log('');

  // Step 3: Run generate.js --write (if exists)
  const generatePath = join(ROOT, 'scripts', 'generate.js');
  if (existsSync(generatePath)) {
    console.log(`${CYAN}Step 3:${RESET} Running code generator...`);
    run('node scripts/generate.js --write');
    console.log('');
  } else {
    console.log(`${CYAN}Step 3:${RESET} ${DIM}generate.js not found, skipping.${RESET}\n`);
  }

  // Step 4: Update CHANGELOG.md
  console.log(`${CYAN}Step 4:${RESET} Updating CHANGELOG.md...`);
  prependChangelog(oldVersion, newVersion);
  console.log(`  ${GREEN}\u2713${RESET} CHANGELOG.md entry added\n`);

  // Step 5: Git commit
  console.log(`${CYAN}Step 5:${RESET} Creating git commit...`);
  run('git add -A');
  run(`git commit -m "release: v${newVersion}"`);
  console.log('');

  // Step 6: Git tag
  console.log(`${CYAN}Step 6:${RESET} Creating git tag...`);
  run(`git tag v${newVersion}`);
  console.log('');

  // Done
  console.log(`${GREEN}${BOLD}Release v${newVersion} created.${RESET}`);
  console.log(`Run ${CYAN}git push && git push --tags${RESET} to publish.\n`);
}

main();
