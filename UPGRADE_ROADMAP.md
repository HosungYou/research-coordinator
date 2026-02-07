# Diverga v8.0.1-patch4 Upgrade Roadmap

**Status**: In Progress
**Target**: v8.1.0 (UI/UX Enhancement Release)
**Last Updated**: 2026-02-07

---

## Completed (v8.0.1-patch3 → v8.0.1-patch4)

### ✅ Phase A: English-First UI Changes
- **Files Modified**: 5 skill files
- **Changes**: Korean labels → English (triggers unchanged)
- **Impact**: Improved international accessibility
- **Files**:
  - `/skills/setup/SKILL.md`
  - `/skills/memory/SKILL.md`
  - `/skills/hud/SKILL.md`
  - `/skills/research-coordinator/SKILL.md`
  - `/skills/research-orchestrator/SKILL.md`

### ✅ Phase A.5: Box-Drawing Layout Fixes
- **Files Modified**: 5 skill files
- **Changes**: Fixed broken Unicode box characters in ASCII art
- **Impact**: Clean rendering in all terminal environments
- **Pattern**: `│ ├ └ ─ ┌ ┐` (consistent Unicode box-drawing)

### ✅ Phase B: Dashboard Main Screen
- **File Modified**: `/skills/help/SKILL.md`
- **Changes**:
  - Redesigned `/diverga` main dashboard
  - Clean layout with agent categories
  - Quick start guide
  - Installation verification
- **Impact**: Better first-run experience

### ✅ Phase C: Systematic Review Branding Cleanup
- **Files Modified**: 8 files (Category I skills + agents)
- **Changes**:
  - External branding → "Systematic Review Pipeline"
  - Removed hardcoded external paths
  - Updated to use `cd "$(pwd)"` (user's working directory)
  - Removed external branding from trigger keywords
- **Impact**: Generic, portable systematic review automation
- **Files**:
  - `/skills/i0/SKILL.md`
  - `/skills/i1/SKILL.md`
  - `/skills/i2/SKILL.md`
  - `/skills/i3/SKILL.md`
  - `/agents/i0.md`
  - `/agents/i1.md`
  - `/agents/i2.md`
  - `/agents/i3.md`

---

## Next Steps (v8.1.0 Planning)

### Phase D: Comprehensive UI Audit (RECOMMENDED)

Conduct full sweep of all 44 agent files for:

1. **Consistency Checks**:
   - [ ] Verify all box-drawing characters use Unicode (`│ ├ └ ─`)
   - [ ] Ensure English-first labels (Korean in parentheses)
   - [ ] Check trigger keyword consistency (EN/KR pairs)

2. **Documentation Standards**:
   - [ ] Standardize section headers across all agents
   - [ ] Ensure all agents have clear "Overview" sections
   - [ ] Verify checkpoint tables follow consistent format

3. **Example Code Blocks**:
   - [ ] Remove hardcoded paths
   - [ ] Use environment-agnostic examples
   - [ ] Add comments for clarity

### Phase E: Installation & Discovery Improvements

1. **Plugin Discovery**:
   - [ ] Test all 44 agents load correctly via `/plugin install diverga`
   - [ ] Verify local skill symlinks work (`~/.claude/skills/diverga-*`)
   - [ ] Ensure hyphen prefix (`/diverga-xxx`) works reliably

2. **Setup Wizard**:
   - [ ] Simplify `/diverga-setup` to 2 steps (already done in v8.0)
   - [ ] Add troubleshooting guide for common issues
   - [ ] Auto-detect if Claude Code is authenticated

3. **Version Management**:
   - [ ] Add version checker to `/diverga` dashboard
   - [ ] Show plugin vs. marketplace version comparison
   - [ ] Notify user of available updates

### Phase F: Agent Documentation Consistency

1. **Agent File Structure** (standardize across all 44 agents):
   ```markdown
   ---
   name: agent-id
   description: Brief description
   model: opus|sonnet|haiku
   tools: Read, Glob, Grep, Bash, Task
   ---

   # Agent Title

   **Agent ID**: XN
   **Category**: X - Category Name
   **Tier**: HIGH|MEDIUM|LOW (Model)

   ## Overview

   ## Capabilities (if applicable)

   ## Human Checkpoint Protocol (if applicable)

   ## Execution Commands (if applicable)

   ## Output Format

   ## Integration with Other Agents

   ## Auto-Trigger Keywords

   | Keywords (EN) | Keywords (KR) | Action |
   ```

2. **Checkpoint Documentation**:
   - [ ] Ensure all 🔴 REQUIRED checkpoints are documented
   - [ ] Add checkpoint behavior examples
   - [ ] Clarify when AI must STOP vs. ASK vs. PROCEED

3. **Inter-Agent References**:
   - [ ] Verify all "Related Agents" sections are accurate
   - [ ] Update integration examples to reflect v8.0 changes
   - [ ] Add dependency graphs (optional)

### Phase G: Memory System Enhancement

1. **Context Keywords**:
   - [ ] Expand trigger keyword coverage (currently EN/KR pairs)
   - [ ] Add fuzzy matching for common typos
   - [ ] Support phrase variations ("my research" = "research status")

2. **Decision Log**:
   - [ ] Add export to CSV/JSON
   - [ ] Implement decision search by stage/checkpoint
   - [ ] Show decision timeline visualization

3. **Session Continuity**:
   - [ ] Auto-resume last session on `/diverga` dashboard
   - [ ] Show "time since last session" indicator
   - [ ] Suggest next steps based on last checkpoint

### Phase H: Testing & Quality Assurance

1. **Agent Activation Tests**:
   - [ ] Test all 44 agents activate correctly via keywords
   - [ ] Verify model routing (haiku/sonnet/opus)
   - [ ] Ensure checkpoints trigger as expected

2. **Integration Tests**:
   - [ ] Test parallel execution groups (A1+A2+A5, etc.)
   - [ ] Verify sequential pipelines (C5→C6→C7)
   - [ ] Test cross-agent data passing

3. **User Experience**:
   - [ ] Test with fresh Claude Code installation
   - [ ] Verify all CLI commands work (`/diverga-xxx`)
   - [ ] Check error messages are helpful

---

## Version Targets

| Version | Focus | ETA |
|---------|-------|-----|
| **v8.0.1-patch4** | Branding cleanup + English UI | ✅ DONE (2026-02-07) |
| **v8.1.0** | UI/UX consistency + Installation | TBD |
| **v8.2.0** | Memory system v3 enhancements | TBD |
| **v9.0.0** | Multi-language support (beyond EN/KR) | TBD |

---

## Breaking Changes to Consider (v9.0)

1. **Agent ID Rename**:
   - Current: `diverga:a1`, `diverga:a2`, etc.
   - Proposed: `diverga:foundation-question-refiner`, etc.
   - Impact: More descriptive but breaks existing workflows

2. **Checkpoint System Redesign**:
   - Current: 🔴 🟠 🟡 (3 levels)
   - Proposed: Add 🟢 AUTO (no human input) level
   - Impact: Clearer automation boundaries

3. **Memory File Format**:
   - Current: YAML-based `.research/`
   - Proposed: SQLite for structured queries
   - Impact: Better performance, richer queries

---

## Maintenance Notes

### Files Modified in v8.0.1-patch4

```
skills/setup/SKILL.md         (Phase A)
skills/memory/SKILL.md        (Phase A)
skills/hud/SKILL.md           (Phase A)
skills/research-coordinator/SKILL.md  (Phase A)
skills/research-orchestrator/SKILL.md (Phase A)
skills/help/SKILL.md          (Phase B)
skills/i0/SKILL.md            (Phase C)
skills/i1/SKILL.md            (Phase C)
skills/i2/SKILL.md            (Phase C)
skills/i3/SKILL.md            (Phase C)
agents/i0.md                  (Phase C)
agents/i1.md                  (Phase C)
agents/i2.md                  (Phase C)
agents/i3.md                  (Phase C)
```

### Testing Checklist

- [x] Phase A: Verify English labels render correctly
- [x] Phase A.5: Verify box-drawing in terminal
- [x] Phase B: Test `/diverga` command shows new dashboard
- [x] Phase C: Verify no external branding in active files
- [ ] Phase D: Full agent audit (pending)
- [ ] Phase E: Installation test on fresh system (pending)

---

## Contributor Guide

To continue this roadmap:

1. **Pick a Phase** from "Next Steps" section
2. **Create Tasks** using TaskCreate for each sub-item
3. **Execute Changes** following the patterns from completed phases
4. **Update This File** with completion status
5. **Test Thoroughly** using the testing checklist
6. **Commit** with clear version bump (patch/minor/major)

---

## References

- **GitHub**: https://github.com/HosungYou/Diverga
- **Version History**: See `/CLAUDE.md` for full changelog
- **Agent Directory**: 44 agents across 9 categories (A-I)
- **Current Version**: v8.0.1-patch4 (2026-02-07)
