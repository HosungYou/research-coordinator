# Research Coordinator 🧬

**AI Research Assistant for the Complete Research Lifecycle**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-5.0.0-brightgreen)](https://github.com/HosungYou/research-coordinator)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai/code)
[![VS Methodology](https://img.shields.io/badge/VS-Verbalized%20Sampling-green)](https://arxiv.org/abs/2510.01171)
[![Language](https://img.shields.io/badge/language-English%20%7C%20한국어-orange)](docs/README-ko.md)

---

## 🎯 Overview

Research Coordinator is a specialized AI assistant system that supports the complete research lifecycle through **27 context-aware agents**. Built on Claude Code Skills with Sisyphus Protocol enforcement, it maintains project context from initial question formulation through to publication and ensures completion through agent-based orchestration.

### What Makes This Different?

**Context Persistence Across Research Lifecycle** - Unlike general AI tools that require re-explaining your research every conversation, Research Coordinator maintains:
- Your research question and theoretical framework
- Methodological decisions and their rationale
- Literature search strategies and results
- Analysis plans and intermediate findings
- Review history and revision decisions

All in a single platform, accessible throughout your project.

## ✨ New in v5.0.0 (Sisyphus Edition)

### 🔄 Sisyphus Protocol: Continuation Enforcement
Research tasks must be **completed** before Claude Code moves on:
- **Agent-Based Orchestration**: Work delegated to specialized agents, not performed directly
- **Paradigm-Aware Completion**: Different verification criteria for quantitative/qualitative/mixed methods
- **Iron Law**: NO completion claims without fresh verification evidence

```
Before claiming "done":
1. IDENTIFY: What proves this claim?
2. RUN: Execute verification command
3. READ: Check output - did it pass?
4. ONLY THEN: Claim completion with evidence
```

### 🎯 Paradigm Detection & Agent Packs
Automatic detection activates appropriate agent sets:

| Paradigm | Auto-Detected Keywords | Agent Pack | Completion Criteria |
|----------|------------------------|------------|---------------------|
| **Quantitative** | "meta-analysis", "effect size", "statistical power" | A1-A5, C1-C4, E1-E4 | All tests pass, effect sizes calculated |
| **Qualitative** | "phenomenology", "grounded theory", "thematic analysis" | A1-A5, D1-D4, E1-E4 | Saturation achieved, inter-coder reliability |
| **Mixed Methods** | "convergent", "explanatory sequential", "joint display" | All 27 agents | Both paradigm criteria + meta-inference |

### 🔬 Full Qualitative Research Support (NEW)
27 agents now cover complete qualitative research lifecycle:
- **Phenomenology**: Bracketing, essence identification, meaning units
- **Grounded Theory**: Open/axial/selective coding, theoretical saturation
- **Case Study**: Thick description, pattern matching, cross-case synthesis
- **Ethnography**: Fieldwork protocols, participant observation, cultural interpretation
- **Action Research**: PDSA cycles, participatory engagement, change documentation

### 🔀 Mixed Methods Integration (NEW)
- **Joint Display Tables**: Quantitative + qualitative side-by-side
- **Meta-Inference Generation**: Integration synthesis from both data types
- **Convergent Design**: Parallel data collection with merging analysis
- **Explanatory Sequential**: QUANT → qual follow-up exploration
- **Exploratory Sequential**: QUAL → quant validation

### 📋 Enhanced Pipeline Templates
Now includes paradigm-specific workflows:
- **Quantitative**: PRISMA 2020 Systematic Review (7 stages), Meta-Analysis, RCT/Quasi-Experimental
- **Qualitative**: Grounded Theory (6 stages), Phenomenology (5 stages), Case Study (4 stages)
- **Mixed Methods**: Convergent (3 phases), Explanatory Sequential (4 phases), Exploratory Sequential (4 phases)

## 🏗️ Architecture (27 Agents in 8 Categories)

### Category A: Research Foundation (5 Agents)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **A1** | **Research Question Refiner** | FINER/PICO/SPIDER framework | All | Enhanced |
| **A2** | **Theoretical Framework Architect** | Theory selection, conceptual models | All | Full |
| **A3** | **Hypothesis Generator** | Testable hypotheses, research predictions | Quantitative/Mixed | Enhanced |
| **A4** | **Devil's Advocate** | Critical evaluation, alternative perspectives | All | Full |
| **A5** | **Paradigm Advisor (NEW)** | Quantitative/qualitative/mixed methods guidance | All | Enhanced |

### Category B: Literature & Evidence (4 Agents)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **B1** | **Systematic Literature Scout** | PRISMA/qualitative synthesis search | All | Full |
| **B2** | **Evidence Quality Appraiser** | Methodological quality, CASP/JBI appraisal | All | Enhanced |
| **B3** | **Effect Size Extractor** | Quantitative effect sizes, qualitative themes | All | Enhanced |
| **B4** | **Research Radar** | Trend monitoring, emerging methods | All | Enhanced |

### Category C: Study Design (4 Agents)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **C1** | **Research Design Consultant** | Design optimization, validity threats | All | Enhanced |
| **C2** | **Sample Size Calculator (NEW)** | Power analysis, saturation estimation | Quantitative/Mixed | Light |
| **C3** | **Measurement Validator (NEW)** | Scale selection, reliability/validity checks | Quantitative/Mixed | Enhanced |
| **C4** | **Research Ethics Advisor (NEW)** | IRB protocols, informed consent, data protection | All | Enhanced |

### Category D: Data Collection (4 Agents - ALL NEW)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **D1** | **Interview Protocol Designer** | Semi-structured interview guides | Qualitative/Mixed | Enhanced |
| **D2** | **Survey Instrument Designer** | Questionnaire design, item generation | Quantitative/Mixed | Enhanced |
| **D3** | **Observation Framework Builder** | Ethnographic fieldwork protocols | Qualitative | Enhanced |
| **D4** | **Data Quality Monitor** | Missing data, outliers, quality checks | All | Light |

### Category E: Analysis (4 Agents)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **E1** | **Statistical Analysis Guide** | Quantitative analysis methods | Quantitative/Mixed | Full |
| **E2** | **Qualitative Coding Assistant (NEW)** | Thematic analysis, grounded theory coding | Qualitative/Mixed | Enhanced |
| **E3** | **Mixed Methods Integrator (NEW)** | Joint displays, meta-inference generation | Mixed | Full |
| **E4** | **Analysis Code Generator** | R/Python/NVivo scripts | All | Light |

### Category F: Quality & Validation (4 Agents)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **F1** | **Internal Consistency Checker** | Logical consistency verification | All | Light |
| **F2** | **Checklist Manager** | PRISMA/CONSORT/COREQ compliance | All | Light |
| **F3** | **Reproducibility Auditor** | Data/code sharing, transparency | All | Light |
| **F4** | **Bias Detector** | Selection/reporting/confirmation bias | All | Full |

### Category G: Publication & Communication (4 Agents)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **G1** | **Journal Matcher** | Target journal identification | All | Light |
| **G2** | **Academic Communicator** | Audience-adapted writing | All | Light |
| **G3** | **Peer Review Strategist** | Review response strategies | All | Light |
| **G4** | **Preregistration Composer** | OSF/AsPredicted protocols | All | Light |

### Category H: Specialized Approaches (2 Agents - ALL NEW)
| # | Agent | Purpose | Paradigm | VS Level |
|---|-------|---------|----------|----------|
| **H1** | **Action Research Facilitator** | PDSA cycles, participatory methods | Action Research | Full |
| **H2** | **Community-Based Research Advisor** | Participatory engagement, co-creation | CBPR | Full |

### Master Agent
| # | Agent | Purpose |
|---|-------|---------|
| **M1** | **Research Coordinator Master** | Auto-dispatch, paradigm detection, workflow orchestration |

## 🚀 Getting Started

### Installation

**Option 1: Marketplace Install (Recommended)**
```bash
# Add marketplace (one-time setup)
claude plugin marketplace add HosungYou/research-coordinator

# Install all 27 skills + master
claude plugin install research-coordinator
```

**Option 2: Local Development**
```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

### Verify Installation
```bash
claude plugin list | grep research-coordinator
```

Expected output:
```
❯ research-coordinator@research-coordinator-skills
  Version: 5.0.0
  Status: ✔ enabled
```

## 📖 Usage

### Natural Language Interface

Simply describe what you want to do:

```
"I want to conduct a systematic review on AI in education"
→ Activates PRISMA 2020 pipeline template

"메타분석 연구를 시작하고 싶어요"
→ Launches meta-analysis workflow (Korean support)

"Help me design an experimental study comparing two interventions"
→ Guides through experimental design wizard
```

### Master Skill Command

```bash
/research-coordinator
```

The master skill analyzes conversation context and automatically dispatches appropriate agents.

### Direct Agent Invocation

```bash
/theoretical-framework-architect    # Theory selection
/systematic-literature-scout        # PRISMA search
/statistical-analysis-guide         # Analysis planning
/journal-matcher                    # Publication targeting
```

### Auto-Trigger Example

```
User: "Planning a meta-analysis on effectiveness of AI tutoring systems"

Claude: [Auto-detected: "meta-analysis", "effectiveness"]
        → Paradigm: Quantitative
        → Activating agents:
          B1 Systematic Literature Scout
          B3 Effect Size Extractor
          E1 Statistical Analysis Guide
        → Initializing PRISMA 2020 workflow...
```

## 🔬 Paradigm Detection & Agent Packs

Research Coordinator automatically detects your research paradigm and activates appropriate agent packs:

### Detection Triggers

| Paradigm | Auto-Detected Keywords | Example Phrases |
|----------|------------------------|-----------------|
| **Quantitative** | "meta-analysis", "effect size", "statistical power", "RCT", "regression" | "I want to conduct a meta-analysis", "Planning an experimental study" |
| **Qualitative** | "phenomenology", "grounded theory", "thematic analysis", "lived experience", "saturation" | "Exploring lived experiences of...", "Grounded theory study on..." |
| **Mixed Methods** | "convergent", "explanatory sequential", "joint display", "meta-inference", "integration" | "Convergent mixed methods design", "QUANT → qual follow-up" |
| **Action Research** | "PDSA", "participatory", "co-creation", "iterative cycles", "change process" | "Action research in my classroom", "Collaborative inquiry project" |

### Agent Pack Activation

| Paradigm | Activated Agents | Completion Criteria |
|----------|------------------|---------------------|
| **Quantitative** | A1-A5, B1-B4, C1-C4, E1+E4, F1-F4, G1-G4 | - All tests pass<br>- Effect sizes calculated<br>- Power analysis complete<br>- Data/code shared |
| **Qualitative** | A1-A2+A4-A5, B1-B4, C1+C4, D1-D4, E2+E4, F1-F4, G1-G4 | - Theoretical saturation achieved<br>- Inter-coder reliability ≥0.80<br>- Member checking complete<br>- Audit trail documented |
| **Mixed Methods** | All 27 agents | - Both paradigm criteria met<br>- Joint display created<br>- Meta-inference generated<br>- Integration synthesis written |
| **Action Research** | A1-A2+A4-A5, C1+C4, D1+D3-D4, H1, F1-F4, G1-G4 | - PDSA cycles documented<br>- Participant validation complete<br>- Change outcomes measured<br>- Reflective journal maintained |

### Paradigm-Specific Workflows

**Quantitative Example**:
```
User: "Meta-analysis on AI chatbots for language learning"

1. B1-Systematic Literature Scout: PRISMA search strategy
2. C2-Sample Size Calculator: Minimum k studies for power
3. B3-Effect Size Extractor: Standardized mean differences
4. E1-Statistical Analysis Guide: Random effects model, heterogeneity
5. F4-Bias Detector: Publication bias analysis
6. G1-Journal Matcher: Meta-analysis journals
```

**Qualitative Example**:
```
User: "Grounded theory study on teacher adoption of AI tools"

1. D1-Interview Protocol Designer: Semi-structured interview guide
2. D4-Data Quality Monitor: Saturation tracking
3. E2-Qualitative Coding Assistant: Open → axial → selective coding
4. F2-Checklist Manager: COREQ compliance
5. A2-Theoretical Framework Architect: Substantive theory generation
6. G1-Journal Matcher: Qualitative research journals
```

**Mixed Methods Example**:
```
User: "Convergent design: survey + interviews on student perceptions"

1. [Parallel QUANT] D2-Survey Instrument Designer + C2-Sample Size Calculator
2. [Parallel QUAL] D1-Interview Protocol Designer + D4-Saturation Monitor
3. [Integration] E3-Mixed Methods Integrator: Joint display table
4. [Integration] E3-Mixed Methods Integrator: Meta-inference generation
5. F2-Checklist Manager: Good Reporting of Mixed Methods Article (GRAMMS)
```

## 🔄 Sisyphus Protocol: Continuation Enforcement

**Core Principle**: Research tasks must be **completed** before moving on. No half-finished work.

### The Iron Law

```
BEFORE claiming "done", "fixed", or "complete":
1. IDENTIFY: What command proves this claim?
2. RUN: Execute verification command
3. READ: Check output - did it actually pass?
4. ONLY THEN: Make the claim WITH evidence
```

### Agent-Based Work Orchestration

Research Coordinator delegates substantive work to specialized agents, not performing code changes directly:

| Work Type | Delegation Strategy |
|-----------|---------------------|
| Simple code lookup | Explore agents (Haiku) |
| Feature implementation | Executor agents (Sonnet) |
| Complex refactoring | Executor-high agents (Opus) |
| Analysis design | Statistical/Qualitative guides (Opus) |
| Quality checks | QA/Bias detector agents (Sonnet) |

### Completion Verification Per Paradigm

| Paradigm | Verification Evidence Required |
|----------|-------------------------------|
| **Quantitative** | - All statistical tests executed<br>- Effect sizes calculated with CI<br>- Power analysis shows adequate N<br>- Diagnostic plots generated<br>- Results tables formatted |
| **Qualitative** | - Theoretical saturation demonstrated<br>- Inter-coder reliability ≥0.80 (kappa/ICC)<br>- Member checking feedback documented<br>- Audit trail complete with decision log<br>- Reflexivity statement written |
| **Mixed Methods** | - Both QUANT and QUAL criteria met<br>- Joint display table created<br>- Meta-inference statement written<br>- Integration synthesis complete<br>- Divergence/convergence identified |

### Red Flags (STOP and Verify)

- Using "should", "probably", "seems to"
- Expressing satisfaction before running verification
- Claiming completion without fresh test/build output
- Marking todo as complete without evidence

### Example: Proper Completion Claim

**Bad (No Evidence)**:
```
"I've implemented thematic analysis. The codes look good!"
```

**Good (With Evidence)**:
```
"Thematic analysis complete. Evidence:
1. [EXECUTED] qualitative-coding-assistant: 47 codes generated
2. [VERIFIED] Inter-coder reliability: κ = 0.84 (substantial agreement)
3. [EXECUTED] Theme hierarchy: 6 themes, 18 subthemes
4. [GENERATED] Codebook exported to themes_codebook.xlsx
5. [DOCUMENTED] Reflexivity notes in analysis_memo.md

Next step: Member checking with 3 participants."
```

## 🧠 VS-Research Methodology (v3.0)

**Verbalized Sampling (VS)** prevents AI "mode collapse" - the tendency to always recommend the same obvious options.

### Dynamic T-Score (Typicality Score)

All recommendations include 0-1 typicality scores:

| T-Score | Interpretation | Recommendation |
|---------|----------------|----------------|
| `T > 0.8` | Modal (most common) | ⚠️ Avoid for differentiation |
| `T 0.5-0.8` | Established alternative | ✅ Safe choice |
| `T 0.3-0.5` | Emerging approach | ✅ Innovative, justifiable |
| `T < 0.3` | Creative/novel | ⚠️ Requires strong rationale |

### 5 Creativity Mechanisms

| Mechanism | Description | Example |
|-----------|-------------|---------|
| **Forced Analogy** | Borrow concepts from distant fields | "TAM → Ecosystem Theory" |
| **Iterative Loop** | 3-5 refinement cycles | "Initial → Improved → Optimized" |
| **Semantic Distance** | Explore conceptually distant ideas | "Learning effect → Neuroplasticity" |
| **Temporal Reframing** | Shift temporal perspective | "10-year retrospective view" |
| **Community Simulation** | Simulate scholarly debate | "Conservative vs. Innovative scholars" |

### 14 User Checkpoints

| Code | Checkpoint | Purpose |
|------|-----------|---------|
| CP-INIT-001 | Initial context confirmation | Research field/experience level |
| CP-INIT-002 | Goal clarification | Research objectives/expected outcomes |
| CP-VS-001 | Modal awareness check | Acknowledge modal options |
| CP-VS-003 | Final choice confirmation | Approve recommendation |
| CP-FA-001 | Forced analogy validation | Check analogy appropriateness |
| CP-IL-001 | Iteration loop gate | Continue refinement? |
| CP-SD-001 | Semantic distance validation | Confirm concept expansion |

### VS Application Levels

| Level | Agents | Description | Mechanisms |
|-------|--------|-------------|------------|
| **FULL** | 02, 03, 05, 10, 16 | Complete VS process | All 5 |
| **ENHANCED** | 01, 04, 06, 07, 08, 09 | Streamlined VS | FA, IL, SD |
| **LIGHT** | 11-15, 17-20 | Modal awareness + alternatives | None |

### Example: Avoiding Mode Collapse in Theory Selection

```
❌ Before VS (Mode Collapse):
   "For AI adoption research, I recommend TAM." (every time)

✅ After VS v3.0:
   [CP-INIT-001] Context check: Learning motivation study, prefers innovation

   Phase 1 - Modal Identification:
   "TAM (T=0.92) and UTAUT (T=0.85) are the most predictable choices."
   [CP-VS-001] Modal awareness confirmed

   Phase 2 - Creativity Mechanisms:
   [Forced Analogy] "Adaptive Learning Ecosystem" from ecological theory
   [Semantic Distance] "Plasticity" from neuroscience applied to learning

   Options:
   - Direction A (T≈0.6): Self-Determination Theory × TAM integration
   - Direction B (T≈0.4): Cognitive Load Theory + Adaptive Ecosystem
   - Direction C (T≈0.2): Neuroplasticity-based learning framework
   [CP-FA-001] Analogy appropriateness validated

   Phase 3 - Contextual Recommendation:
   [CP-VS-003] "For your context, Direction B (T=0.4) is recommended. Proceed?"
```

## 🔧 Core Principle: Human-AI Division of Labor

> **"Human decisions remain with humans. AI handles what's beyond human scope."**
> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**

### What Humans Decide
- Research direction and theoretical stance
- Inclusion/exclusion criteria for studies
- Interpretation of findings
- Ethical trade-offs
- Publication strategy

### What AI Handles
- Searching 20,000+ papers across databases
- Calculating inter-rater reliability
- Generating PRISMA flow diagrams
- Extracting effect sizes from tables
- Formatting references to journal style

**All AI recommendations include checkpoints for human validation.**

## 📦 Complete Skill List (27 Skills + Master)

### Category A: Research Foundation
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/research-question-refiner` | Enhanced | FINER/PICO/SPIDER framework |
| `/theoretical-framework-architect` | **Full** | Theory selection |
| `/hypothesis-generator` | Enhanced | Testable hypotheses |
| `/devils-advocate` | **Full** | Critical evaluation |
| `/paradigm-advisor` | Enhanced | Paradigm guidance (NEW) |

### Category B: Literature & Evidence
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/systematic-literature-scout` | **Full** | PRISMA/qualitative search |
| `/evidence-quality-appraiser` | Enhanced | Quality assessment |
| `/effect-size-extractor` | Enhanced | Effect sizes/themes |
| `/research-radar` | Enhanced | Trend monitoring |

### Category C: Study Design
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/research-design-consultant` | Enhanced | Design optimization |
| `/sample-size-calculator` | Light | Power analysis (NEW) |
| `/measurement-validator` | Enhanced | Scale validation (NEW) |
| `/research-ethics-advisor` | Enhanced | IRB protocols (NEW) |

### Category D: Data Collection
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/interview-protocol-designer` | Enhanced | Interview guides (NEW) |
| `/survey-instrument-designer` | Enhanced | Questionnaires (NEW) |
| `/observation-framework-builder` | Enhanced | Fieldwork protocols (NEW) |
| `/data-quality-monitor` | Light | Quality checks (NEW) |

### Category E: Analysis
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/statistical-analysis-guide` | **Full** | Quantitative analysis |
| `/qualitative-coding-assistant` | Enhanced | Thematic analysis (NEW) |
| `/mixed-methods-integrator` | **Full** | Joint displays (NEW) |
| `/analysis-code-generator` | Light | R/Python/NVivo code |

### Category F: Quality & Validation
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/internal-consistency-checker` | Light | Logical consistency |
| `/checklist-manager` | Light | PRISMA/CONSORT/COREQ |
| `/reproducibility-auditor` | Light | Reproducibility check |
| `/bias-detector` | **Full** | Bias identification |

### Category G: Publication & Communication
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/journal-matcher` | Light | Journal targeting |
| `/academic-communicator` | Light | Audience adaptation |
| `/peer-review-strategist` | Light | Review response |
| `/preregistration-composer` | Light | OSF/AsPredicted |

### Category H: Specialized Approaches
| Skill Command | VS Level | Description |
|---------------|----------|-------------|
| `/action-research-facilitator` | **Full** | PDSA cycles (NEW) |
| `/community-based-research-advisor` | **Full** | Participatory methods (NEW) |

### Master Coordinator
| Skill Command | Description |
|---------------|-------------|
| `/research-coordinator` | Auto-dispatch, paradigm detection, workflow orchestration |

## 🔗 Integration Hub

### No Setup Required (Built-in)
| Tool | Use Case | Paradigm | Trigger |
|------|----------|----------|---------|
| **Excel** | Data extraction, coding sheets | All | "Create extraction spreadsheet" |
| **PowerPoint** | Conference presentations | All | "Generate conference slides" |
| **Word** | Manuscripts, method sections | All | "Export method section" |
| **Python** | Quantitative/qualitative analysis | All | Built-in |
| **Mermaid** | Flow diagrams (PRISMA, process maps) | All | "Create PRISMA diagram" |

### Requires Setup (External APIs)
| Tool | Purpose | Paradigm | Setup Command |
|------|---------|----------|---------------|
| **Semantic Scholar** | Literature retrieval | All | Add API key to `.env` |
| **OpenAlex** | Open access search | All | Add email for polite pool |
| **Zotero MCP** | Reference management | All | `/oh-my-claudecode:mcp-setup` |
| **Nanobanana** | Gemini-powered visualization | Quantitative | Add Gemini API key |
| **R Scripts** | Statistical analysis | Quantitative/Mixed | Install R locally |
| **NVivo API** | Qualitative coding (if available) | Qualitative/Mixed | License required |
| **MAXQDA** | Qualitative analysis (manual) | Qualitative/Mixed | License required |
| **ATLAS.ti** | Grounded theory support | Qualitative | License required |

### Paradigm-Specific Tool Recommendations

| Paradigm | Recommended Tools | Auto-Generated Outputs |
|----------|-------------------|------------------------|
| **Quantitative** | R/Python, Excel, Mermaid | - Power analysis tables<br>- Forest plots (meta-analysis)<br>- Regression tables<br>- Diagnostic plots |
| **Qualitative** | Python (text analysis), Excel, Word | - Codebook spreadsheets<br>- Theme hierarchy diagrams<br>- Inter-coder reliability tables<br>- Audit trail documents |
| **Mixed Methods** | All of the above | - Joint display tables<br>- Integration matrices<br>- Meta-inference summaries<br>- Side-by-side comparison charts |

## 🌐 Multilingual Support

Research Coordinator fully supports **Korean and English** input:

```
English: "I want to conduct a systematic review"
Korean: "체계적 문헌고찰을 하고 싶어요"
Mixed: "메타분석을 하려는데, can you help?"
```

All agents understand both languages and respond appropriately.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](docs/QUICKSTART.md) | Get started in 5 minutes |
| [Installation](docs/SETUP.md) | Full setup instructions |
| [Usage Examples](docs/USAGE-EXAMPLES.md) | Common use cases |
| [Agent Reference](docs/AGENT-REFERENCE.md) | 27 agents detailed reference |
| [OMC Integration](docs/OMC-INTEGRATION.md) | oh-my-claudecode integration |
| [Roadmap](docs/ROADMAP.md) | Future development plans |
| [Changelog](docs/CHANGELOG.md) | Version history |
| [한국어 문서](docs/i18n/ko/README-ko.md) | Korean documentation |

## 🔧 Requirements

- [Claude Code CLI](https://claude.ai/code)
- Bash shell (macOS/Linux, WSL for Windows)
- Optional: R (for statistical code generation), Python 3.8+ (for data analysis)

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Claude Code](https://claude.ai/code) by Anthropic - AI-powered coding assistant
- [Verbalized Sampling (arXiv:2510.01171)](https://arxiv.org/abs/2510.01171) - VS methodology foundation
- Social science research community for feedback and validation

## 📖 Citation

If you use Research Coordinator in your research, please cite:

```bibtex
@software{research_coordinator,
  author = {You, Hosung},
  title = {Research Coordinator: AI Research Assistant for the Complete Research Lifecycle},
  year = {2025},
  version = {5.0.0},
  url = {https://github.com/HosungYou/research-coordinator},
  note = {27 agents with Sisyphus Protocol enforcement. Supports quantitative, qualitative, and mixed methods research. Integrates Verbalized Sampling methodology from arXiv:2510.01171}
}
```

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=HosungYou/research-coordinator&type=Date)](https://star-history.com/#HosungYou/research-coordinator&Date)

---

**Made with ❤️ for Social Science Researchers**

*Empowering human researchers with AI assistance that respects human judgment.*
