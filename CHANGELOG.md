# Changelog

All notable changes to Research Coordinator will be documented in this file.

## [3.2.0] - 2025-01-25

### Added

#### OMC (oh-my-claudecode) Integration
- **21 OMC Agent Definition Files** (`.omc/agents/research/01-21`)
  - Each agent has: tier, model, category, parallel_group, human_checkpoint, triggers
  - Follows OMC agent specification format

- **Human Checkpoint System** (`.omc/checkpoints/`)
  - `checkpoint-definitions.yaml`: 7 checkpoints across 3 levels
    - 🔴 REQUIRED: CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL
    - 🟠 RECOMMENDED: CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW
    - 🟡 OPTIONAL: CP_VISUALIZATION_PREFERENCE, CP_RENDERING_METHOD
  - `checkpoint-handler.md`: Implementation protocol for checkpoint handling
  - `parallel-execution-rules.yaml`: 10 parallel execution groups with checkpoint boundaries

- **Model Routing Configuration** (`.omc/config/research-coordinator-routing.yaml`)
  - HIGH tier (Opus): #01, #02, #03, #09, #19 - Strategic decisions
  - MEDIUM tier (Sonnet): #04, #06, #10, #12, #15-18, #20, #21 - Standard analysis
  - LOW tier (Haiku): #05, #07, #08, #11, #13, #14 - Search, calculation, code
  - ~60% token savings compared to all-Opus approach

- **Research Orchestrator Skill** (`.omc/skills/research-orchestrator/SKILL.md`)
  - Coordinates Research Coordinator with OMC execution modes
  - Agent-tier quick reference table
  - Integration with ultrawork, ecomode, ralph modes

- **Comprehensive Documentation** (`docs/omc-integration.md`)
  - 450+ line guide for OMC integration
  - Usage scenarios, configuration references
  - Migration guide and troubleshooting

### Changed

- **CLAUDE.md**: Added OMC Integration v3.2.0 section
- **SKILL.md**: Updated to v3.2.0 with OMC integration, model routing table, checkpoint references

### Core Principle

> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**
> (Human decisions MUST be respected, AI only handles tasks beyond human scope)

### Compatibility

- **Backwards Compatible**: Works with Claude Code alone (no OMC required)
- **Enhanced with OMC**: Parallel execution, smart model routing, token efficiency

---

## [3.1.0] - Previous Release

- 21 research agents across 5 categories (A-E)
- VS-Research (Verbalized Sampling) methodology
- Nanobanana integration for visualizations
- Claude Code Skills system support

---

## File Structure (v3.2.0)

```
research-coordinator/
├── .claude/skills/
│   ├── research-coordinator/    # Master skill
│   └── research-agents/         # 21 individual agents
├── .omc/                        # NEW: OMC Integration
│   ├── agents/research/         # 21 OMC agent definitions
│   │   ├── 01-research-question-refiner.md
│   │   ├── 02-theoretical-framework-architect.md
│   │   └── ... (21 files)
│   ├── checkpoints/
│   │   ├── checkpoint-definitions.yaml
│   │   ├── checkpoint-handler.md
│   │   └── parallel-execution-rules.yaml
│   ├── config/
│   │   └── research-coordinator-routing.yaml
│   └── skills/research-orchestrator/
│       └── SKILL.md
├── docs/
│   └── omc-integration.md       # NEW: OMC integration guide
├── CLAUDE.md                    # Updated with OMC section
├── CHANGELOG.md                 # NEW: This file
└── README.md
```

---

## Agent Tier Summary

| Tier | Model | Agents | Use Case |
|------|-------|--------|----------|
| HIGH | Opus | #01, #02, #03, #09, #19 | Strategic decisions, critical analysis |
| MEDIUM | Sonnet | #04, #06, #10, #12, #15-18, #20, #21 | Standard analysis, quality assessment |
| LOW | Haiku | #05, #07, #08, #11, #13, #14 | Search, calculation, code generation |

---

## Usage

### Without OMC (Basic Mode)
```bash
/research-coordinator
```

### With OMC (Enhanced Mode)
```bash
ulw: 문헌 검색해줘     # Maximum parallelism
eco: 통계 분석해줘     # Token efficient
ralph: 연구 설계해줘   # Persistence until done
```

---

## Contributors

- Implementation: Claude Opus 4.5 with OMC orchestration
- Architect Verification: Passed
