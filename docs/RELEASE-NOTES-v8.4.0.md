# Diverga v8.4.0 Release Notes

**Release Date**: 2026-02-12
**Code Name**: Researcher Visibility & Pipeline Safety
**Previous Version**: v8.3.0

---

## Overview

Diverga v8.4.0 addresses two critical usability issues reported by researchers:

1. **Hidden Directory Problem**: Research state files were stored in `.research/` (dot-prefix hidden folder), making them invisible in file explorers. Researchers couldn't find their project files, decision logs, or checkpoint states without terminal commands.

2. **Pipeline Safety Gap**: When databases requiring API keys (Scopus, Web of Science) were selected, missing keys caused silent skipping instead of stopping to ask the researcher. This led to incomplete data collection without user awareness.

### Key Highlights

- **Dual directory structure**: `.research/` (system) + `research/` (researcher-visible)
- **Automatic migration**: Existing `.research/` projects auto-migrate public files on first access
- **New checkpoint**: `SCH_API_KEY_VALIDATION` blocks pipeline when required API keys are missing
- **Full backward compatibility**: No breaking changes for existing projects
- **9 files modified** across MCP server, HUD, context manager, and documentation

---

## What's New

### 1. Dual Directory Structure (Phase A)

**Problem**: All research state files were hidden in `.research/`, invisible to researchers in Finder/Explorer.

**Solution**: Split into two directories with clear separation of concerns:

```
project-root/
├── .research/                  # System files (hidden - internal use only)
│   ├── hud-state.json          # HUD display cache
│   ├── priority-context.md     # Compressed context (500 chars max)
│   └── sessions/               # Session records
│
├── research/                   # Researcher-visible files (NEW)
│   ├── project-state.yaml      # Project metadata
│   ├── decision-log.yaml       # All research decisions (audit trail)
│   ├── checkpoints.yaml        # Checkpoint states & progress
│   ├── baselines/              # Stable research foundations
│   │   ├── literature/
│   │   ├── methodology/
│   │   └── framework/
│   └── changes/
│       ├── current/            # Active work
│       └── archive/            # Completed stages
│
└── docs/                       # Auto-generated documentation
```

**File Classification Logic**:

| File | Location | Reason |
|------|----------|--------|
| `project-state.yaml` | `research/` | Researcher needs to see project status |
| `decision-log.yaml` | `research/` | Research decision audit trail - critical for researchers |
| `checkpoints.yaml` | `research/` | Progress tracking visibility |
| `baselines/` | `research/` | Research foundations - researcher's reference material |
| `changes/` | `research/` | Active work history |
| `hud-state.json` | `.research/` | Pure system cache - no research value |
| `priority-context.md` | `.research/` | Internal context compression - system only |
| `sessions/` | `.research/` | System session records |

### 2. Automatic Migration

Existing projects with files in `.research/` are automatically migrated:

```javascript
// On first access, checkpoint-logic.js copies public files:
// .research/project-state.yaml  → research/project-state.yaml
// .research/decision-log.yaml   → research/decision-log.yaml
// .research/checkpoints.yaml    → research/checkpoints.yaml
```

- **Non-destructive**: Original `.research/` files are preserved (copied, not moved)
- **Idempotent**: Migration only runs if target file doesn't exist
- **Backward-compatible**: `findProjectRoot()` searches for both directories

### 3. API Key Validation Checkpoint (Phase B)

**Problem**: Selecting Scopus or Web of Science without API keys caused silent database skipping.

**Solution**: New `SCH_API_KEY_VALIDATION` checkpoint blocks the pipeline:

```
Database Selection → API Key Check → 🔴 SCH_API_KEY_VALIDATION
                                         ├─ "Provide Key" → Show setup instructions → Re-validate
                                         ├─ "Skip DB" → Remove from selection → Re-confirm
                                         └─ "Pause" → Save state → Stop pipeline
```

**Checkpoint Details**:

| Property | Value |
|----------|-------|
| ID | `SCH_API_KEY_VALIDATION` |
| Level | 🔴 REQUIRED |
| Applies to | I1-PaperRetrievalAgent |
| Dependency Level | Level 3 (same as SCH_DATABASE_SELECTION) |
| Cannot proceed without | `true` |

**API Key Requirements by Database**:

| Database | Environment Variable | Required? |
|----------|---------------------|-----------|
| Semantic Scholar | `S2_API_KEY` | Optional (recommended for rate limits) |
| OpenAlex | Email (polite pool) | Optional |
| arXiv | None | No key needed |
| Scopus | `SCOPUS_API_KEY` | **Required** |
| Web of Science | `WOS_API_KEY` | **Required** |

### 4. New `validateApiKeys()` Function

Added to `mcp/lib/checkpoint-logic.js` as an exported utility:

```javascript
import { validateApiKeys } from './lib/checkpoint-logic.js';

const result = validateApiKeys(['semantic_scholar', 'scopus', 'wos']);
// {
//   missing: [
//     { database: 'scopus', envKey: 'SCOPUS_API_KEY', required: true },
//     { database: 'wos', envKey: 'WOS_API_KEY', required: true }
//   ],
//   optional: [
//     { database: 'semantic_scholar', envKey: 'S2_API_KEY', required: false }
//   ],
//   allValid: false
// }
```

---

## Files Modified (9 total)

### Phase A: Directory Structure

| File | Change |
|------|--------|
| `mcp/lib/checkpoint-logic.js` | Dual-path system with `publicDir` parameter, migration logic, bound path helpers |
| `mcp/checkpoint-server.js` | New `getPublicResearchDir()` function, passes both dirs to logic |
| `lib/hud/state.ts` | `findProjectRoot()` searches both dirs, `loadProjectState/loadCheckpoints` try public first |
| `.opencode/plugins/diverga/hooks/context-manager.ts` | `CONTEXT_PATHS` updated to `research/` |
| `CLAUDE.md` | Directory structure docs, path references, version history |

### Phase B: API Key Checkpoint

| File | Change |
|------|--------|
| `mcp/agent-prerequisite-map.json` | `SCH_API_KEY_VALIDATION` in i1 checkpoints, levels, dependency order |
| `.claude/references/checkpoint-templates.md` | Bilingual AskUserQuestion template (3 options) |
| `skills/i1/SKILL.md` | Error handling: skip→STOP, new checkpoint protocol section |
| `.claude/checkpoints/checkpoint-definitions.yaml` | New checkpoint definition (required, 🔴) |
| `mcp/lib/checkpoint-logic.js` | `validateApiKeys()` exported function |

---

## Migration Guide

### For Existing Projects

**No action required.** On first access after updating to v8.4.0:

1. The system automatically creates `research/` directory
2. Copies `project-state.yaml`, `decision-log.yaml`, `checkpoints.yaml` from `.research/` to `research/`
3. Original files in `.research/` are preserved
4. All tools read from `research/` first, fall back to `.research/`

### For New Projects

New projects will automatically use the dual-directory structure:
- System files → `.research/`
- Researcher files → `research/`

### Verification

```bash
# After updating, verify the structure:
ls -la project-root/          # research/ folder should be visible
ls -la project-root/.research/ # Only system files (hud-state, priority-context, sessions)
ls -la project-root/research/  # Research state files visible here
```

---

## Breaking Changes

**None.** Full backward compatibility maintained.

---

## Known Issues

- Legacy scripts that hardcode `.research/` paths will still work (files exist in both locations)
- The `.research/` copies of migrated files are not automatically synced; `research/` is the source of truth after migration

---

## Upgrade Path

```
v8.3.0 → v8.4.0: Automatic (no manual steps required)
```

---

## Contributors

- Hosung You (@HosungYou)
