# Changelog

All notable changes to Diverga (formerly Research Coordinator) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [6.0.1] - 2026-01-25

### 🏗️ Agent Restructuring Release

### Changed

#### Agent Naming Convention
- **Renamed all 33 agents** from numbered format (01-21) to category-based format (A1-H2)
- Consistent naming: `{Category}{Number}-{agent-name}` (e.g., `A1-research-question-refiner`)
- Categories: A (Foundation), B (Evidence), C (Design), D (Data Collection), E (Analysis), F (Quality), G (Communication), H (Specialized)

#### Documentation Updates
- Updated `CLAUDE.md` with 33 agents and category-based naming
- Updated `AGENTS.md` with complete agent registry
- Updated `README.md` with v6.0.1 badges and content

#### Configuration Updates
- Updated `research-coordinator-routing.yaml` with all 33 agent references
- Updated `checkpoint-definitions.yaml` with agent-checkpoint mappings
- Updated `parallel-execution-rules.yaml` with dependency graph

---

## [6.0.0] - 2026-01-25

### 🎯 Major Release: Human-Centered Edition (Clean Slate)

> **Core Principle**: "Human decisions remain with humans. AI handles what's beyond human scope."
> **핵심 원칙**: "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

### Removed

#### Sisyphus Protocol ❌
- **Was**: "Work never stops until complete"
- **Problem**: Could bypass human checkpoints, enabling autonomous operation without approval
- **Now**: AI stops at EVERY checkpoint and waits for human decision

#### Iron Law of Continuation ❌
- **Was**: "Move to next agent OR human checkpoint"
- **Problem**: "OR" made checkpoints optional
- **Now**: Sequential flow: "checkpoint THEN next agent"

#### OMC Autonomous Modes ❌
- **Removed**: `ralph`, `ultrawork`, `autopilot`, `ecomode`, `swarm`, `ultrapilot`
- **Problem**: These modes enabled checkpoint bypass
- **Kept**: Model routing only (Opus/Sonnet/Haiku tiers)

#### Legacy Folder Structure ❌
- **Removed**: `.omc/` folder and all contents
- **Migrated**: Necessary files moved to `.claude/`

### Added

#### Human Checkpoint System (Core Feature)
Three checkpoint levels with mandatory enforcement:

| Level | Icon | Behavior |
|-------|------|----------|
| **REQUIRED** | 🔴 | System STOPS - Cannot proceed without explicit approval |
| **RECOMMENDED** | 🟠 | System PAUSES - Strongly suggests approval |
| **OPTIONAL** | 🟡 | System ASKS - Defaults available if skipped |

#### Required Checkpoints (🔴 MANDATORY)
- `CP_RESEARCH_DIRECTION`: Research question finalized
- `CP_PARADIGM_SELECTION`: Methodology approach (Quantitative/Qualitative/Mixed)
- `CP_THEORY_SELECTION`: Framework chosen with T-Score alternatives
- `CP_METHODOLOGY_APPROVAL`: Design complete with detailed review

#### Checkpoint State Storage
- Location: `.claude/state/checkpoints.json`
- Tracks all human decisions with timestamps
- Creates audit trail for research process

### Changed

#### Repository Renamed
- From: `research-coordinator`
- To: `Diverga`
- URL: https://github.com/HosungYou/Diverga

#### Folder Structure
- From: `.omc/` (OMC-centric)
- To: `.claude/` (Claude Code native)

#### Agent Count
- From: 27 agents
- To: 33 agents across 8 categories

### Migration Notes

Users upgrading from v5.0:
1. The `.omc/` folder is no longer used - safe to delete
2. OMC autonomous modes (`ralph`, `ultrawork`, etc.) are removed
3. Checkpoints are now mandatory - AI will stop and wait for your approval
4. Model routing still works - specify `haiku`, `sonnet`, or `opus` for task tiers

---

## [5.0.0] - 2025-01-25

### 🎯 Major Release: Sisyphus Edition

### Added

#### Sisyphus Protocol
- **Continuation Enforcement**: AI never claims "done" prematurely
- **Agent-based Orchestration**: Tasks delegated to specialized agents
- **Paradigm-aware Completion**: Different completion criteria for quantitative/qualitative/mixed methods

#### Complete Qualitative Research Support
- **Phenomenology**: Bracketing, essence identification, meaning units
- **Grounded Theory**: Open/axial/selective coding, theoretical saturation
- **Case Study**: Thick description, pattern matching
- **Ethnography**: Fieldwork, cultural interpretation
- **Action Research**: PDSA cycles, participatory research

#### Mixed Methods Integration
- Joint Display tables
- Meta-inference generation
- Convergent/sequential design support

#### Paradigm Detection System
Auto-detection triggers with keyword recognition:
- **Quantitative**: "effect size", "meta-analysis", "statistical power"
- **Qualitative**: "phenomenology", "grounded theory", "thematic analysis"
- **Mixed Methods**: "convergent", "sequential", "joint display"

#### New Agents (v5.0)
- Category D: Data Collection (4 agents)
- Category H: Specialized Approaches (4 agents)
- Total: 27 agents across 8 categories

### Changed

#### VS Methodology Enhanced
- Paradigm-contextualized T-Scores
- 5 creativity mechanisms fully integrated
- 14 user checkpoints

---

## [4.0.0] - 2025-01-25

### 🎯 Major Release: Complete Architecture Integration

Research Coordinator v4.0 delivers context-persistent research support with full architectural consistency.

### Added

#### Core Systems (v4.0)
- **Project State System**: Context persistence across entire research lifecycle (`.research/project-state.yaml`)
- **Pipeline Templates**: Pre-configured PRISMA 2020, Meta-Analysis, Experimental, Survey workflows
- **Integration Hub**: Connections to Semantic Scholar, OpenAlex, Zotero MCP, Nanobanana, Office Suite
- **Guided Wizard**: AskUserQuestion-based UX for researchers with limited coding experience
- **Auto-Documentation**: Automatic generation of PRISMA diagrams, extraction sheets, method sections

#### Agent Architecture
- **3-Tier Structure**: Flagship (4), Core (6), Support (11) agents
- **v4.0 References**: All 21 agents now reference core v4.0 modules
- **Pipeline A-E**: Complete research lifecycle workflow with PRISMA 2020 alignment

### Changed

#### Documentation
- Restructured `docs/` for consistency (UPPERCASE naming, organized subdirectories)
- Added `docs/i18n/ko/` for Korean translations
- Added `docs/releases/` for version-specific notes
- Added `docs/internal/` for development documents

#### Core Modules
- Added `version: "4.0.0"` frontmatter to all core modules
- Standardized YAML frontmatter across all files

#### Agents
- All 21 agents updated to v4.0.0
- Added `tier:` field to YAML frontmatter
- Added v4.0 core module references to all agents
- Converted all agents from Korean to English

### Removed

- `figures/` directory (reference code only, not production)
- `docs/PYTHON.md` (removed with figures/)

---

## [3.1.1] - 2026-01-25

### 🛠️ Infrastructure Release: Architecture Enhancement

### Added

#### Agent Contract Validation System
- **`scripts/validate_agents.py`**: SKILL.md contract validator
- External dependency-free YAML parser
- Required frontmatter field validation
- Semantic version format checking
- FULL/ENHANCED/LIGHT level requirement validation
- JSON output option (for CI/CD integration)

#### Cross-Platform CLI Tool
- **`scripts/rc`**: Bash CLI (macOS/Linux)
- **`scripts/rc.py`**: Python CLI (all OS)
- Commands: help, status, list, validate, info, doctor

#### Windows Support
- **`scripts/install.ps1`**: PowerShell installation script
- Symbolic link / copy mode selection
- Automatic admin privilege detection
- Uninstall functionality

#### Testing & Quality
- **`tests/test_validate_agents.py`**: 18 unit tests
- **`pyproject.toml`**: Python project configuration
- **`requirements-dev.txt`**: Development dependencies

#### Documentation
- **`CONTRIBUTING.md`**: Contribution guidelines
- **`docs/QUICKSTART.md`**: 5-minute quick start guide

---

## [3.1.0] - 2025-01-24

### 🎨 Feature Release: Conceptual Framework Visualizer

Added 21st agent for visualizing conceptual frameworks with Code-First approach.

### Added

#### New Agent: 21-Conceptual-Framework-Visualizer
- **Full VS (5 stages)** for maximum creativity
- **Code-First, Image-Second** approach: Logic structure → Code → Visualization
- **Multi-modality support**: Mermaid, Graphviz, Python NetworkX, D3.js + SVG

---

## [3.0.0] - 2025-01-24

### 🎯 Major Release: VS-Research v3.0

Major upgrade of Verbalized Sampling methodology with Dynamic T-Score system, 5 creativity mechanisms, and 14 user checkpoints.

### Added

#### Core Infrastructure
- **VS Engine v3.0** (`core/vs-engine.md`)
- **Dynamic T-Score System** (`core/t-score-dynamics.md`)

#### Interaction System
- **14 User Checkpoints** (`interaction/user-checkpoints.md`)

#### 5 Creativity Mechanisms
| Mechanism | Description |
|-----------|-------------|
| Forced Analogy | Borrow concepts from distant fields |
| Iterative Loop | 3-5 divergent-convergent cycles |
| Semantic Distance | Explore conceptually distant ideas |
| Temporal Reframing | Shift time perspectives |
| Community Simulation | Simulate academic discussions |

### Changed

#### 3-Tier Agent Upgrade
All 20 agents upgraded to v3.0:
- **FULL**: 02, 03, 05, 10, 16 (5 agents) - All 5 mechanisms
- **ENHANCED**: 01, 04, 06, 07, 08, 09 (6 agents) - 3 mechanisms
- **LIGHT**: 11-15, 17-20 (9 agents) - Modal awareness only

---

## [2.1.0] - 2025-01-23

### Changed
- **Single plugin, all skills**: `research-coordinator` plugin contains all 21 skills
- Simplified installation (2 lines)
- marketplace.json structure changed (Anthropic document-skills pattern)

---

## [2.0.0] - 2025-01-22

### Added
- **Verbalized Sampling (VS) methodology** integration
- arXiv:2510.01171 based Mode Collapse prevention
- T-Score (Typicality Score) system
- VS application levels (Full/Enhanced/Light)

---

## [1.0.0] - 2025-01-22

### Added
- Initial release
- 20 specialized research agents
- Master coordinator (auto-dispatch)
- 5 category structure
- Context-aware automatic agent activation
- Trigger keyword system
- Korean/English bilingual support
- Claude Code Skills system integration

---

## Version History Summary

| Version | Date | Key Changes |
|---------|------|-------------|
| **6.0.1** | 2026-01-25 | Agent restructuring to category-based naming (A1-H2), 33 agents |
| **6.0.0** | 2026-01-25 | **Human-Centered Edition**: Removed Sisyphus/OMC modes, mandatory checkpoints |
| 5.0.0 | 2025-01-25 | Sisyphus protocol, paradigm detection, 27 agents |
| 4.0.0 | 2025-01-25 | Context persistence, pipeline templates, integration hub |
| 3.1.1 | 2026-01-25 | Infrastructure: Contract validation, CLI tools, Windows support |
| 3.1.0 | 2025-01-24 | Feature: Conceptual Framework Visualizer (21st agent) |
| 3.0.0 | 2025-01-24 | VS-Research v3.0: Dynamic T-Score, 5 Creativity Mechanisms |
| 2.1.0 | 2025-01-23 | Single plugin with all 21 skills |
| 2.0.0 | 2025-01-22 | VS methodology integration |
| 1.0.0 | 2025-01-22 | Initial release |
