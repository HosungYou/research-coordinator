# AGENTS.md

> AI-readable documentation for Research Coordinator v4.0

## Project Overview

**Research Coordinator** is a Claude Code Skills-based AI research assistant system providing context-persistent support for the complete research lifecycle.

**Version**: 4.0.0
**Generated**: 2025-01-25
**Repository**: https://github.com/HosungYou/research-coordinator

---

## Core Philosophy

> "Human decisions remain with humans. AI handles what's beyond human scope."

- Strategic research decisions require human approval (checkpoints)
- AI prevents mode collapse through VS (Verbalized Sampling) methodology
- Context persistence eliminates re-explanation burden

---

## Architecture

### Directory Structure

```
research-coordinator/
├── .claude/skills/
│   ├── research-coordinator/          # Master coordinator
│   │   ├── SKILL.md                   # Main entry point (v4.0)
│   │   └── core/                      # Core systems
│   │       ├── project-state.md       # Context persistence
│   │       ├── pipeline-templates.md  # PRISMA workflows
│   │       ├── integration-hub.md     # Tool connections
│   │       ├── guided-wizard.md       # Conversation UX
│   │       └── auto-documentation.md  # Document generation
│   └── research-agents/               # 21 specialized agents
│       ├── 01-research-question-refiner/
│       ├── 02-theoretical-framework-architect/
│       └── ... (through 21)
├── docs/                              # Documentation
├── scripts/                           # Installation scripts
├── CONTRIBUTING.md                    # Contributor guide
├── CHANGELOG.md                       # Version history
└── README.md                          # Project overview
```

---

## Core Systems (v4.0)

### 1. Project State Management

**Location**: `.research/project-state.yaml`

Maintains research context across the entire lifecycle:
- Research question and PICO elements
- Theoretical framework and hypotheses
- Methodology decisions
- Integration status
- Decision audit trail

### 2. Pipeline Templates

Pre-configured workflows:
- **Systematic Review & Meta-Analysis**: PRISMA 2020 compliant, 8 stages
- **Experimental Study**: Pre-registered workflow
- **Survey Research**: Cross-sectional/longitudinal

### 3. Integration Hub

Available tools:
| Tool | Access | Purpose |
|------|--------|---------|
| Excel | Skill: ms-office-suite | Data extraction |
| PowerPoint | Skill: ms-office-suite | Presentations |
| Word | Skill: ms-office-suite | Manuscripts |
| R Scripts | Generated | Statistical analysis |
| Semantic Scholar | API | Literature search |
| Zotero | MCP | References |
| Nanobanana | API | AI visualization |

### 4. Guided Wizard

Conversation UX using `AskUserQuestion` tool:
- Explicit choice points for decisions
- Natural language between checkpoints
- Bilingual support (EN/KO)

### 5. Auto-Documentation

Generated documents:
- Decision Log (timestamped)
- PRISMA Checklist (auto-tracked)
- Methods Section Draft
- OSF Submission Package

---

## Agent Registry

### 3-Tier Structure

| Tier | Agents | Characteristics |
|------|--------|-----------------|
| **Flagship** | #02, #03, #10, #21 | Full VS methodology, strategic decisions |
| **Core** | #01, #05, #06, #09, #16, #17 | Essential capabilities, enhanced VS |
| **Support** | #04, #07-08, #11-15, #18-20 | Specialized tasks, light VS |

### Complete Agent List

| ID | Name | Tier | VS Level | Category |
|----|------|------|----------|----------|
| 01 | Research Question Refiner | Core | Enhanced | A: Theory & Design |
| 02 | Theoretical Framework Architect | Flagship | Full | A: Theory & Design |
| 03 | Devil's Advocate | Flagship | Full | A: Theory & Design |
| 04 | Research Ethics Advisor | Support | Enhanced | A: Theory & Design |
| 05 | Systematic Literature Scout | Core | Full | B: Literature & Evidence |
| 06 | Evidence Quality Appraiser | Core | Enhanced | B: Literature & Evidence |
| 07 | Effect Size Extractor | Support | Enhanced | B: Literature & Evidence |
| 08 | Research Radar | Support | Enhanced | B: Literature & Evidence |
| 09 | Research Design Consultant | Core | Enhanced | C: Methodology & Analysis |
| 10 | Statistical Analysis Guide | Flagship | Full | C: Methodology & Analysis |
| 11 | Analysis Code Generator | Support | Light | C: Methodology & Analysis |
| 12 | Sensitivity Analysis Designer | Support | Light | C: Methodology & Analysis |
| 13 | Internal Consistency Checker | Support | Light | D: Quality & Validation |
| 14 | Checklist Manager | Support | Light | D: Quality & Validation |
| 15 | Reproducibility Auditor | Support | Light | D: Quality & Validation |
| 16 | Bias Detector | Core | Full | D: Quality & Validation |
| 17 | Journal Matcher | Core | Light | E: Publication & Communication |
| 18 | Academic Communicator | Support | Light | E: Publication & Communication |
| 19 | Peer Review Strategist | Support | Light | E: Publication & Communication |
| 20 | Preregistration Composer | Support | Light | E: Publication & Communication |
| 21 | Conceptual Framework Visualizer | Flagship | Full | E: Publication & Communication |

---

## VS-Research Methodology

**Purpose**: Prevent mode collapse (AI always recommending the same thing)

### T-Score (Typicality Score)

| T-Score | Label | Meaning |
|---------|-------|---------|
| ≥ 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, requires strong justification |
| < 0.2 | Experimental | Highly novel, high risk/reward |

### 3-Stage Process (v4.0)

1. **Context & Modal Identification**: Understand context, identify "obvious" recommendations
2. **Divergent Exploration**: Generate alternatives with T-Scores
3. **Selection & Execution**: Human chooses, AI executes with rigor

---

## Human Checkpoints

| Level | Checkpoints | Behavior |
|-------|-------------|----------|
| 🔴 REQUIRED | CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL | Must pause for user approval |
| 🟠 RECOMMENDED | CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW | Should pause, can be skipped |
| 🟡 OPTIONAL | CP_VISUALIZATION_PREFERENCE | Defaults available |

---

## Auto-Trigger Keywords

| English | Korean | Agent |
|---------|--------|-------|
| research question, PICO | 연구 질문 | #01 |
| theoretical framework, conceptual model | 이론, 개념적 모형 | #02 |
| literature review, PRISMA | 문헌 검토, 체계적 리뷰 | #05 |
| statistics, ANOVA, regression | 통계 분석, 회귀 | #10 |
| visualization, figure | 시각화, 그림 | #21 |
| journal, submission | 저널, 투고 | #17 |
| IRB, ethics | 윤리 | #04 |
| reviewer, peer review | 리뷰어 | #19 |

---

## Model Routing (OMC Integration)

| Tier | Model | Agents |
|------|-------|--------|
| HIGH | Opus | #01, #02, #03, #09, #19 |
| MEDIUM | Sonnet | #04, #06, #10, #12, #15-18, #20-21 |
| LOW | Haiku | #05, #07, #08, #11, #13-14 |

---

## Key Files for AI Understanding

| File | Purpose |
|------|---------|
| `SKILL.md` | Master coordinator entry point |
| `core/project-state.md` | Context persistence schema |
| `core/pipeline-templates.md` | PRISMA workflow definitions |
| `core/integration-hub.md` | Tool connection guide |
| `.research/project-state.yaml` | Active project context (runtime) |
| `.research/decision-log.yaml` | Decision audit trail (runtime) |

---

## Usage Patterns

### Starting a Project
```
User: "I want to conduct a systematic review on AI in education"
→ Activates guided wizard
→ Creates .research/project-state.yaml
→ Begins Stage 1: Protocol Development
```

### Resuming a Project
```
User: "Continue my research project"
→ Reads .research/project-state.yaml
→ Injects context into conversation
→ Resumes from current stage
```

### Requesting Tool Integration
```
User: "Create an Excel spreadsheet for data extraction"
→ Uses ms-office-suite:excel skill
→ Generates formatted template
```

---

*This file enables AI assistants to understand Research Coordinator's architecture and operate effectively within it.*
