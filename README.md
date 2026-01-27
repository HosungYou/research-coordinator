# Diverga 🌟

**Beyond Modal: AI Research Assistant That Thinks Creatively**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-6.4.0-brightgreen)](https://github.com/HosungYou/Diverga)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.ai/code)
[![VS Methodology](https://img.shields.io/badge/VS-Verbalized%20Sampling-green)](https://arxiv.org/abs/2510.01171)
[![Language](https://img.shields.io/badge/language-English%20%7C%20한국어-orange)](docs/i18n/ko/README-ko.md)
[![Agents](https://img.shields.io/badge/agents-40-purple)](docs/AGENTS.md)

---

## 🚀 Quick Start (3 Steps)

```bash
# Step 1: Add to Claude Code marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# Step 2: Install the plugin
/plugin install diverga

# Step 3: Run setup wizard
/diverga:setup
```

Then just say what you want:
```
"I want to conduct a meta-analysis on AI in education"
"체계적 문헌고찰을 시작하고 싶어"
"Help me design an experimental study"
```

Diverga auto-detects context and activates the right agents.

---

## 🌟 Why "Diverga"? Breaking Free from Mode Collapse

Most AI research assistants suffer from **mode collapse** - they always recommend the same predictable options:

> ❌ "For technology adoption, I recommend TAM." (every single time)
> ❌ "For your meta-analysis, use random effects model." (always)
> ❌ "Try thematic analysis for your qualitative study." (the obvious choice)

**Diverga is different.** Built on **Verbalized Sampling (VS) methodology** (arXiv:2510.01171), it actively prevents mode collapse and guides you toward **creative, defensible research choices**.

---

## ✨ v6.4 (Plugin Marketplace Edition)

### Core Principle

> **"Human decisions remain with humans. AI handles what's beyond human scope."**
> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**

### 🆕 What's New in v6.4

| Feature | Description |
|---------|-------------|
| **📦 Plugin Marketplace** | Install via `/plugin marketplace add` |
| **⚡ Auto-Trigger Dispatch** | Context-based automatic agent activation |
| **🔧 /diverga:setup Wizard** | Interactive configuration with LLM API, checkpoints, paradigm |
| **📋 /diverga:help** | Comprehensive agent reference |
| **🧠 40 Specialized Agents** | Complete research lifecycle coverage |

### What's in v6.3

| Feature | Description |
|---------|-------------|
| **📊 C5-MetaAnalysisMaster** | Multi-gate validation, workflow orchestration |
| **🔍 C6-DataIntegrityGuard** | Data extraction with provenance tracking |
| **⚠️ C7-ErrorPreventionEngine** | Pattern detection, error prevention |

### What's in v6.2

| Feature | Description |
|---------|-------------|
| **📄⚡ B5-ParallelDocumentProcessor** | Batch PDF processing with parallel workers |
| **🚀 High-throughput Processing** | Process 50-500 PDFs concurrently without memory overflow |
| **🔄 Fault Tolerance** | Automatic retry logic for failed extractions |

### What Was Added in v6.1

| Feature | Description |
|---------|-------------|
| **✨ Humanization Pipeline** | Transform AI-generated text to natural academic prose |
| **🔍 G5-AcademicStyleAuditor** | Detect 24 categories of AI writing patterns |
| **✨ G6-AcademicStyleHumanizer** | Transform patterns while preserving citations & statistics |
| **✅ F5-HumanizationVerifier** | Verify transformation integrity |
| **📋 Ethics Framework** | AI writing disclosure guidelines |

### Humanization Quick Start

```
"Check AI patterns in my draft"    → G5 analysis
"Humanize my abstract"             → Full pipeline (balanced mode)
"Humanize (conservative)"          → For journal submissions
"Export with humanization"         → Pipeline before Word export
```

**3 Transformation Modes**:
- **Conservative**: High-risk patterns only (5-15% text change)
- **Balanced**: Recommended default (15-30% text change)
- **Aggressive**: All patterns (30-50% text change)

### What's in v6.0

| Feature | Description |
|---------|-------------|
| **🔴 Mandatory Checkpoints** | AI STOPS and WAITS at critical decision points |
| **36 Specialized Agents** | 33 agents + 3 new humanization agents (A1-H2, F5, G5-G6) |
| **Human-Centered Design** | Every major decision requires explicit human approval |
| **Clean Architecture** | Simplified folder structure under `.claude/` |

### What Was Removed (v6.0)

| Removed | Reason |
|---------|--------|
| ❌ Sisyphus Protocol | Could bypass human checkpoints |
| ❌ Iron Law | "OR" made checkpoints optional |
| ❌ OMC Autonomous Modes | ralph/ultrawork/ecomode enabled bypass |

---

## 🎯 Human Checkpoint System

### Checkpoint Types

| Level | Icon | Behavior |
|-------|------|----------|
| **REQUIRED** | 🔴 | System STOPS - Cannot proceed without explicit approval |
| **RECOMMENDED** | 🟠 | System PAUSES - Strongly suggests approval |
| **OPTIONAL** | 🟡 | System ASKS - Defaults available if skipped |

### Required Checkpoints

| Checkpoint | When | What Happens |
|------------|------|--------------|
| CP_RESEARCH_DIRECTION | Research question finalized | Present VS options, WAIT for selection |
| CP_PARADIGM_SELECTION | Methodology approach | Ask Quantitative/Qualitative/Mixed |
| CP_THEORY_SELECTION | Framework chosen | Present alternatives with T-Scores |
| CP_METHODOLOGY_APPROVAL | Design complete | Detailed review required |

---

## 🧠 Core Innovation: Verbalized Sampling (VS) Methodology

### The Problem: Modal Recommendations

AI systems tend to recommend the most statistically common options - what we call **modal recommendations**. While safe, these lead to:
- Homogenized research landscapes
- Missed innovative opportunities
- Difficulty differentiating your work

### The Solution: Dynamic T-Score System

Diverga assigns **Typicality Scores (T-Score)** to all recommendations:

| T-Score | Interpretation | Diverga Behavior |
|---------|----------------|------------------|
| `T > 0.8` | **Modal** (most common) | ⚠️ Flags as "predictable" |
| `T 0.5-0.8` | **Established alternative** | ✅ Suggests as balanced choice |
| `T 0.3-0.5` | **Emerging approach** | ✅ Recommends for innovation |
| `T < 0.3` | **Novel/creative** | 🔬 Presents with strong rationale |

### VS in Action: Before vs. After

```
❌ WITHOUT VS (Mode Collapse):
   User: "Help me choose a theoretical framework for AI adoption study"
   AI: "I recommend Technology Acceptance Model (TAM)."
   (Same answer every time, T=0.92)

✅ WITH VS (Diverga):
   User: "Help me choose a theoretical framework for AI adoption study"

   🔴 CHECKPOINT: CP_THEORY_SELECTION

   Diverga: "Let me analyze options across the typicality spectrum:

   [Modal Awareness] TAM (T=0.92) and UTAUT (T=0.85) are predictable choices.

   Recommended Options:
   • Direction A (T≈0.6): Self-Determination Theory × TAM integration
   • Direction B (T≈0.4): Cognitive Load Theory + Adaptive Ecosystem ⭐
   • Direction C (T≈0.2): Neuroplasticity-based technology learning

   Which direction would you like to proceed?"
   (WAITS for human selection)
```

---

## 🏗️ Architecture (40 Agents in 8 Categories)

### Category A: Foundation (6 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| A1-research-question-refiner | Opus | FINER/PICO/SPIDER framework |
| A2-theoretical-framework-architect | Opus | Theory selection with VS |
| A3-devils-advocate | Opus | Critical evaluation |
| A4-research-ethics-advisor | Sonnet | IRB, ethical considerations |
| A5-paradigm-worldview-advisor | Opus | Quant/qual/mixed guidance |
| A6-conceptual-framework-visualizer | Sonnet | Visual framework design |

### Category B: Evidence (5 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| B1-systematic-literature-scout | Sonnet | PRISMA/qualitative search |
| B2-evidence-quality-appraiser | Sonnet | RoB, GRADE assessment |
| B3-effect-size-extractor | Haiku | Effect size calculations |
| B4-research-radar | Haiku | Trend monitoring |
| **B5-parallel-document-processor** 🆕 | Opus | Batch PDF processing with parallel workers |

### Category C: Design & Meta-Analysis (7 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| C1-quantitative-design-consultant | Opus | Experimental, survey design |
| C2-qualitative-design-consultant | Opus | Phenomenology, GT, case study |
| C3-mixed-methods-design-consultant | Opus | Sequential, convergent |
| C4-experimental-materials-developer | Sonnet | Treatment materials |
| **C5-meta-analysis-master** 🆕 | Opus | Multi-gate validation, workflow orchestration |
| **C6-data-integrity-guard** 🆕 | Sonnet | Data extraction with provenance |
| **C7-error-prevention-engine** 🆕 | Sonnet | Pattern detection, error prevention |

### Category D: Data Collection (4 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| D1-sampling-strategy-advisor | Sonnet | Probability/purposive sampling |
| D2-interview-focus-group-specialist | Sonnet | Protocols, transcription |
| D3-observation-protocol-designer | Haiku | Field notes |
| D4-measurement-instrument-developer | Opus | Scale construction |

### Category E: Analysis (5 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| E1-quantitative-analysis-guide | Opus | Statistical analysis |
| E2-qualitative-coding-specialist | Opus | Thematic, GT coding |
| E3-mixed-methods-integration | Opus | Joint displays, meta-inference |
| E4-analysis-code-generator | Haiku | R/Python/NVivo code |
| E5-sensitivity-analysis-designer | Sonnet | Robustness checks |

### Category F: Quality (5 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| F1-internal-consistency-checker | Haiku | Internal validity |
| F2-checklist-manager | Haiku | PRISMA/CONSORT/COREQ |
| F3-reproducibility-auditor | Sonnet | Open Science |
| F4-bias-trustworthiness-detector | Sonnet | Bias detection |
| **F5-humanization-verifier** 🆕 | Haiku | Transformation verification |

### Category G: Communication (6 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| G1-journal-matcher | Sonnet | Target journal selection |
| G2-academic-communicator | Sonnet | Audience adaptation |
| G3-peer-review-strategist | Opus | Review response |
| G4-preregistration-composer | Sonnet | OSF/AsPredicted |
| **G5-academic-style-auditor** 🆕 | Sonnet | AI pattern detection (24 categories) |
| **G6-academic-style-humanizer** 🆕 | Opus | Pattern transformation |

### Category H: Specialized (2 Agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| H1-ethnographic-research-advisor | Opus | Fieldwork, thick description |
| H2-action-research-facilitator | Opus | PAR, CBPR cycles |

---

## 🚀 Getting Started

### Installation (Claude Code Plugin)

```bash
# Install via Claude Code marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga
/plugin install diverga
/diverga:setup
```

### Alternative: Manual Installation

```bash
git clone https://github.com/HosungYou/Diverga.git
cd Diverga
```

### Usage

**Natural Language** (auto-triggers agents):
```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어요"
"Help me design an experimental study"
```

**Direct Commands**:
```
/diverga:setup          # Configuration wizard
/diverga:help           # Show all 40 agents
/diverga:meta-analysis  # Start meta-analysis workflow
diverga:c5              # Invoke specific agent
```

The system will:
1. Detect your paradigm
2. **ASK for confirmation** (🔴 CHECKPOINT)
3. Present VS alternatives with T-Scores
4. **WAIT for your selection**
5. Guide you through the pipeline with checkpoints

---

## 🔗 Integration Hub

### Built-in (No Setup)
| Tool | Use Case |
|------|----------|
| Excel | Data extraction, coding sheets |
| PowerPoint | Conference presentations |
| Word | Manuscripts, method sections |
| Python | Analysis scripts |
| Mermaid | Flow diagrams |

### Requires Setup
| Tool | Purpose |
|------|---------|
| Semantic Scholar | Literature retrieval |
| OpenAlex | Open access search |
| Zotero MCP | Reference management |
| R Scripts | Statistical analysis |

---

## 🌐 Multilingual Support

Diverga fully supports **Korean and English**:

```
English: "I want to conduct a systematic review"
Korean: "체계적 문헌고찰을 하고 싶어요"
Mixed: "메타분석을 하려는데, can you help?"
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](CLAUDE.md) | Full system documentation |
| [PLUGIN.md](PLUGIN.md) | Plugin marketplace definition |
| [AGENTS.md](AGENTS.md) | 40 agents detailed reference |
| [**Agent Orchestration Guide**](docs/AGENT-ORCHESTRATION-GUIDE.md) 🆕 | Comprehensive multi-agent pipelines (EN) |
| [**에이전트 오케스트레이션 가이드**](docs/AGENT-ORCHESTRATION-GUIDE-ko.md) 🆕 | 종합 멀티에이전트 파이프라인 (KO) |
| [**B5 Parallel Processing**](docs/B5-PARALLEL-PROCESSING.md) 🆕 | v6.2 parallel document processing |
| [Quick Start](docs/QUICKSTART.md) | Get started in 5 minutes |
| [VS Methodology](docs/VS-METHODOLOGY.md) | Deep dive into Verbalized Sampling |
| [Humanization Pipeline](docs/v6.1.0-humanization-pipeline.md) | v6.1 humanization documentation |
| [CHANGELOG](CHANGELOG.md) | Version history |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Claude Code](https://claude.ai/code) by Anthropic
- [Verbalized Sampling (arXiv:2510.01171)](https://arxiv.org/abs/2510.01171) - VS methodology foundation
- Social science research community for feedback

---

## 📖 Citation

```bibtex
@software{diverga,
  author = {You, Hosung},
  title = {Diverga: Beyond Modal AI Research Assistant},
  year = {2026},
  version = {6.4.0},
  url = {https://github.com/HosungYou/Diverga},
  note = {40 agents with VS Methodology, Human-Centered Design, Meta-Analysis System, Humanization Pipeline, and Plugin Marketplace. Prevents mode collapse through Verbalized Sampling (arXiv:2510.01171)}
}
```

---

**Made with 🌟 for Social Science Researchers**

*Diverga: Where creativity meets rigor. Beyond the obvious, toward the innovative.*
