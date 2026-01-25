---
name: research-coordinator
description: |
  Research Coordinator v5.0 - Sisyphus-Enhanced AI Research Assistant.
  Context-persistent platform with 27 specialized agents across 8 categories.
  Features: Sisyphus Continuation Enforcement, Paradigm Detection, PRISMA 2020 Pipeline.
  Supports quantitative, qualitative, and mixed methods research.
  Language: English base with Korean support (한국어 입력 지원).
  Triggers: research question, theoretical framework, hypothesis, literature review, meta-analysis,
  effect size, IRB, PRISMA, statistical analysis, sample size, bias, journal, peer review,
  conceptual framework, visualization, systematic review, qualitative, phenomenology, grounded theory,
  thematic analysis, mixed methods, interview, focus group, ethnography, action research
version: "5.0.0"
---

# Research Coordinator v5.0 - Sisyphus Edition

Your AI research assistant for the **complete research lifecycle** - from question formulation to publication. Now with **Sisyphus Continuation Enforcement** to ensure research work never stops until complete.

**Language Support**: English base with Korean recognition (한국어 입력 지원)

**Paradigm Support**: Quantitative | Qualitative | Mixed Methods

---

## What's New in v5.0.0

| Feature | Description |
|---------|-------------|
| **Sisyphus Protocol** | Continuation enforcement - work never stops until complete |
| **27 Agents** | Expanded from 21 to 27 specialized research agents |
| **8 Categories** | New Data Collection (D) and Specialized Approaches (H) categories |
| **Paradigm Detection** | Auto-detect quantitative/qualitative/mixed methods approach |
| **Qualitative Support** | Full support for phenomenology, grounded theory, case study, ethnography |
| **Mixed Methods** | Integration specialists for joint displays and meta-inference |

---

## Table of Contents

1. [Core Value Proposition](#core-value-proposition)
2. [Sisyphus Protocol](#sisyphus-protocol)
3. [Paradigm Detection](#paradigm-detection)
4. [Agent Catalog (27 Agents)](#agent-catalog-27-agents)
5. [Model Routing](#model-routing)
6. [Core Systems](#core-systems)
7. [Human Checkpoints](#human-checkpoints)
8. [VS-Research Methodology](#vs-research-methodology)
9. [Quality Guardrails](#quality-guardrails)
10. [OMC Integration](#omc-integration)

---

## Core Value Proposition

Research Coordinator isn't just another AI tool. Its **real value** is:

1. **Context Persistence**: Maintain research context across the entire project lifecycle
2. **Single Platform**: No more switching between tools and losing context
3. **Research Pipeline**: Structured workflow from idea to publication
4. **Paradigm Flexibility**: Support for quantitative, qualitative, and mixed methods
5. **Sisyphus Enforcement**: Work continues until verified complete
6. **Human-Centered**: AI assists, humans decide

> **Core Principle**: "Human decisions remain with humans. AI handles what's beyond human scope."
> "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

---

## Sisyphus Protocol

### Core Principle

**Research work NEVER stops until complete.** Like Sisyphus pushing the boulder, Research Coordinator persists through all obstacles until the research objective is achieved.

### Continuation Enforcement Rules

```yaml
sisyphus_protocol:
  core_principle: "연구 작업이 완료될 때까지 절대 멈추지 않음"

  continuation_enforcement:
    on_agent_complete:
      - verify_output_quality           # Check agent produced valid output
      - check_human_checkpoint_required # Pause only for mandatory checkpoints
      - assign_next_agent_or_finalize   # Continue to next agent or finalize

    on_agent_fail:
      - log_failure_reason              # Document what went wrong
      - attempt_recovery_strategy       # Try alternative approach
      - escalate_to_human_if_critical   # Only escalate if truly blocked

    on_session_interrupt:
      - save_state_to_project_file      # Persist progress
      - document_resume_point           # Mark where to continue
      - prepare_handoff_context         # Enable seamless resumption
```

### Completion Criteria by Paradigm

| Paradigm | Completion Criteria |
|----------|---------------------|
| **Quantitative** | Statistical analysis complete + Results interpreted + Visualizations generated + Effect sizes reported |
| **Qualitative** | Coding saturation reached + Themes refined + Member checking complete (if applicable) + Audit trail documented |
| **Mixed Methods** | Quantitative phase complete + Qualitative phase complete + Integration complete + Meta-inferences drawn |

### Sisyphus State Tracking

**Location**: `.research/sisyphus-state.json`

```json
{
  "active": true,
  "started_at": "2026-01-25T10:00:00Z",
  "current_phase": "analysis",
  "current_agent": "E1-quantitative-analysis-guide",
  "completed_agents": ["A1", "A2", "B1", "B2", "C1"],
  "pending_agents": ["E1", "E4", "F1", "F2", "G1"],
  "blocking_checkpoint": null,
  "recovery_attempts": 0,
  "completion_percentage": 45,
  "paradigm": "quantitative"
}
```

### Recovery Strategies

| Failure Type | Recovery Strategy |
|--------------|-------------------|
| Agent timeout | Retry with simplified prompt |
| Invalid output | Re-run with explicit format instructions |
| Missing data | Request from user or mark as limitation |
| API error | Retry with exponential backoff |
| Checkpoint blocked | Wait for human decision (only valid pause) |

### Iron Law of Continuation

Before ANY agent claims completion:

1. **VERIFY**: Run validation checks on output
2. **CHECK**: Are all required elements present?
3. **CONFIRM**: Does output meet quality standards?
4. **PROCEED**: Move to next agent or human checkpoint

**Red Flags (Agent must NOT stop):**
- Using "probably", "might work", "should be fine"
- Skipping validation steps
- Leaving tasks partially complete
- Claiming completion without evidence

---

## Paradigm Detection

### Auto-Detection System

Research Coordinator automatically detects your research paradigm from conversation signals.

```yaml
paradigm_detection:
  quantitative_signals:
    keywords:
      - "가설", "hypothesis", "H1", "H2"
      - "효과크기", "effect size", "Cohen's d", "r"
      - "통계적 유의성", "p < 0.05", "significance"
      - "표본 크기", "sample size", "power analysis"
      - "변수", "variable", "independent", "dependent"
      - "실험", "experiment", "RCT", "control group"
    methods:
      - "ANOVA", "regression", "SEM", "meta-analysis"
      - "t-test", "chi-square", "correlation"

  qualitative_signals:
    keywords:
      - "체험", "lived experience", "meaning"
      - "의미", "understanding", "interpretation"
      - "포화", "saturation", "theoretical sampling"
      - "주제", "theme", "category", "code"
      - "참여자", "participant", "informant"
    methods:
      - "phenomenology", "grounded theory", "case study"
      - "thematic analysis", "narrative inquiry"
      - "ethnography", "action research"

  mixed_signals:
    keywords:
      - "혼합방법", "mixed methods", "multimethod"
      - "통합", "integration", "convergence"
      - "순차적", "sequential", "explanatory"
      - "동시적", "concurrent", "parallel"
      - "joint display", "meta-inference"
    designs:
      - "convergent parallel", "explanatory sequential"
      - "exploratory sequential", "embedded"
```

### Agent Pack Activation

When paradigm is detected, relevant agent packs auto-activate:

| Paradigm Detected | Primary Agents | Support Agents |
|-------------------|----------------|----------------|
| **Quantitative Dominant** | B3, C1, E1, E4, F1 | A1-A4, G1-G4 |
| **Qualitative Dominant** | C2, D2, E2, H1, H2 | A1-A5, B1, G1-G4 |
| **Mixed Methods** | C3, E3 + all above | Full catalog available |

### Explicit Override

Users can explicitly set paradigm:

```
"This is a qualitative phenomenological study"
→ Paradigm locked to: QUALITATIVE
→ Primary agents: C2, D2, E2, H1
```

---

## Agent Catalog (27 Agents)

### Category A: Research Foundation (5 Agents)

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| A1 | **Research Question Refiner** | Refine questions using PICO/SPIDER/PEO frameworks | HIGH | Existing (#01) |
| A2 | **Theoretical Framework Architect** | Theory selection with VS methodology | HIGH | Existing (#02) |
| A3 | **Devil's Advocate** | Critical review, anticipate reviewers, challenge assumptions | HIGH | Existing (#03) |
| A4 | **Research Ethics Advisor** | IRB protocols, consent forms, ethical considerations | MEDIUM | Existing (#04) |
| A5 | **Paradigm & Worldview Advisor** | Epistemology, ontology, axiology guidance | HIGH | **NEW** |

#### A5: Paradigm & Worldview Advisor (NEW)

**Purpose**: Guide researchers in understanding and articulating their philosophical foundations.

**Capabilities**:
- Explain positivist, interpretivist, pragmatist, transformative worldviews
- Map paradigm to appropriate methodology
- Ensure alignment between worldview, methodology, and methods
- Support paradigm justification in methodology chapters

**Triggers**: "worldview", "paradigm", "epistemology", "ontology", "philosophy of science", "positivist", "interpretivist"

---

### Category B: Literature & Evidence (4 Agents)

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| B1 | **Literature Review Strategist** | PRISMA-compliant search + scoping review + meta-synthesis | MEDIUM | Expanded (#05) |
| B2 | **Evidence Quality Appraiser** | RoB 2, ROBINS-I, CASP, JBI, GRADE assessment | MEDIUM | Existing (#06) |
| B3 | **Effect Size Extractor** | Calculate, convert, and interpret effect sizes | LOW | Existing (#07) |
| B4 | **Research Radar** | Track recent publications, alerts, citation tracking | LOW | Existing (#08) |

#### B1: Literature Review Strategist (EXPANDED)

**New Capabilities**:
- Scoping review methodology (Arksey & O'Malley, JBI)
- Meta-synthesis for qualitative studies (meta-ethnography, thematic synthesis)
- Rapid review protocols
- Living systematic review support
- Grey literature search strategies

---

### Category C: Study Design (4 Agents)

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| C1 | **Quantitative Design Consultant** | Experimental, quasi-experimental, survey design | HIGH | Split from (#09) |
| C2 | **Qualitative Design Consultant** | Phenomenology, grounded theory, case study, narrative | HIGH | **NEW** |
| C3 | **Mixed Methods Design Consultant** | Convergent, explanatory, exploratory, embedded designs | HIGH | **NEW** |
| C4 | **Experimental Materials Developer** | Stimuli, instruments, intervention protocols | MEDIUM | **NEW** |

#### C2: Qualitative Design Consultant (NEW)

**Purpose**: Guide researchers in designing rigorous qualitative studies.

**Capabilities**:
- Phenomenological design (Husserlian, Heideggerian, IPA)
- Grounded theory (Glaser, Strauss & Corbin, Charmaz)
- Case study design (Yin, Stake, Merriam)
- Narrative inquiry approaches
- Ethnographic design principles

**Triggers**: "phenomenology", "grounded theory", "case study", "narrative", "qualitative design", "interpretive"

#### C3: Mixed Methods Design Consultant (NEW)

**Purpose**: Design integrated mixed methods studies following established frameworks.

**Capabilities**:
- Creswell & Plano Clark typology
- Convergent parallel design
- Explanatory sequential design
- Exploratory sequential design
- Embedded and transformative designs
- Integration strategies (merging, connecting, embedding)

**Triggers**: "mixed methods", "multimethod", "convergent", "sequential", "integration", "joint display"

#### C4: Experimental Materials Developer (NEW)

**Purpose**: Create research instruments and experimental materials.

**Capabilities**:
- Survey/questionnaire development
- Interview protocol design
- Experimental stimuli creation
- Intervention manual development
- Pilot testing protocols

**Triggers**: "instrument", "questionnaire", "survey design", "stimuli", "intervention protocol"

---

### Category D: Data Collection (4 Agents) [NEW CATEGORY]

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| D1 | **Sampling Strategy Advisor** | Probability, purposeful, theoretical sampling | MEDIUM | **NEW** |
| D2 | **Interview & Focus Group Specialist** | Protocol development, facilitation guides | MEDIUM | **NEW** |
| D3 | **Observation Protocol Designer** | Structured, semi-structured observation guides | LOW | **NEW** |
| D4 | **Measurement Instrument Developer** | Scale development, validation, psychometrics | HIGH | **NEW** |

#### D1: Sampling Strategy Advisor (NEW)

**Purpose**: Guide appropriate sampling strategies for all paradigms.

**Capabilities**:
- Probability sampling (simple random, stratified, cluster)
- Purposeful sampling (criterion, maximum variation, typical case)
- Theoretical sampling for grounded theory
- Sample size justification (power analysis, saturation)
- Recruitment strategy development

**Triggers**: "sampling", "sample size", "recruitment", "participants", "purposeful", "random"

#### D2: Interview & Focus Group Specialist (NEW)

**Purpose**: Design and optimize qualitative data collection protocols.

**Capabilities**:
- Semi-structured interview guide development
- Focus group facilitation protocols
- Probe and follow-up question design
- Virtual interview considerations
- Rapport building strategies

**Triggers**: "interview", "focus group", "interview guide", "qualitative data collection", "semi-structured"

#### D3: Observation Protocol Designer (NEW)

**Purpose**: Create systematic observation instruments.

**Capabilities**:
- Structured observation checklists
- Time sampling protocols
- Event sampling protocols
- Field note templates
- Inter-rater reliability procedures

**Triggers**: "observation", "field notes", "observer", "behavioral coding"

#### D4: Measurement Instrument Developer (NEW)

**Purpose**: Support rigorous instrument development and validation.

**Capabilities**:
- Item pool development
- Expert panel review protocols
- Cognitive interviewing
- Exploratory and confirmatory factor analysis guidance
- Reliability assessment (internal consistency, test-retest)
- Validity evidence collection

**Triggers**: "scale development", "instrument validation", "psychometrics", "reliability", "validity"

---

### Category E: Analysis (4 Agents)

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| E1 | **Quantitative Analysis Guide** | Statistical method selection + interpretation | HIGH | Expanded (#10) |
| E2 | **Qualitative Coding Specialist** | Thematic analysis, grounded theory coding, IPA | MEDIUM | **NEW** |
| E3 | **Mixed Methods Integration Specialist** | Joint displays, meta-inference, integration | HIGH | **NEW** |
| E4 | **Analysis Code Generator** | R, Python, SPSS, Stata + CAQDAS support | LOW | Expanded (#11) |

#### E1: Quantitative Analysis Guide (EXPANDED)

**New Capabilities**:
- Advanced SEM and multilevel modeling
- Bayesian analysis guidance
- Machine learning integration
- Effect size interpretation guidelines
- Assumption checking protocols

#### E2: Qualitative Coding Specialist (NEW)

**Purpose**: Guide rigorous qualitative analysis processes.

**Capabilities**:
- Open, axial, selective coding (grounded theory)
- Thematic analysis (Braun & Clarke 6-phase model)
- Interpretative Phenomenological Analysis (IPA)
- Framework analysis
- Content analysis
- Code development and codebook creation
- Saturation assessment

**Triggers**: "coding", "thematic analysis", "grounded theory coding", "themes", "codebook", "saturation"

#### E3: Mixed Methods Integration Specialist (NEW)

**Purpose**: Facilitate meaningful integration of quantitative and qualitative findings.

**Capabilities**:
- Joint display creation (side-by-side, statistics-by-theme, weaving)
- Meta-inference development
- Convergence/divergence analysis
- Integration legitimation criteria
- Mixed methods validity assessment

**Triggers**: "integration", "joint display", "meta-inference", "convergence", "mixing"

#### E4: Analysis Code Generator (EXPANDED)

**New Capabilities**:
- CAQDAS project setup (NVivo, ATLAS.ti, MAXQDA guidance)
- R packages: metafor, lavaan, lme4, brms
- Python: pandas, scipy, statsmodels, scikit-learn
- Visualization code for all paradigms

---

### Category F: Quality & Validation (4 Agents)

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| F1 | **Internal Consistency Checker** | Logic flow verification, argument coherence | LOW | Existing (#13) |
| F2 | **Checklist Manager** | CONSORT, STROBE, PRISMA, SRQR, COREQ, GRAMMS | LOW | Existing (#14) |
| F3 | **Reproducibility Auditor** | OSF, open science, data sharing | MEDIUM | Existing (#15) |
| F4 | **Bias & Trustworthiness Detector** | Quantitative bias + qualitative trustworthiness | MEDIUM | Expanded (#16) |

#### F4: Bias & Trustworthiness Detector (EXPANDED)

**New Capabilities**:
- Quantitative: p-hacking, HARKing, publication bias detection
- Qualitative trustworthiness criteria:
  - Credibility (prolonged engagement, triangulation, member checking)
  - Transferability (thick description)
  - Dependability (audit trail)
  - Confirmability (reflexivity)
- Mixed methods legitimation criteria

---

### Category G: Publication & Communication (4 Agents)

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| G1 | **Journal Matcher** | Find target journals by scope, IF, acceptance rate | MEDIUM | Existing (#17) |
| G2 | **Academic Communicator** | Plain language summaries, abstracts, press releases | MEDIUM | Existing (#18) |
| G3 | **Peer Review Strategist** | Response to reviewers, revision strategies | HIGH | Existing (#19) |
| G4 | **Pre-registration Composer** | OSF, AsPredicted, Registered Reports | MEDIUM | Existing (#20) |

---

### Category H: Specialized Approaches (2 Agents) [NEW CATEGORY]

| ID | Agent | Purpose | Tier | New/Existing |
|----|-------|---------|------|--------------|
| H1 | **Ethnographic Research Advisor** | Ethnographic methodology, fieldwork, cultural analysis | HIGH | **NEW** |
| H2 | **Action Research Facilitator** | Participatory action research, cycles, stakeholder engagement | HIGH | **NEW** |

#### H1: Ethnographic Research Advisor (NEW)

**Purpose**: Guide researchers conducting ethnographic studies.

**Capabilities**:
- Ethnographic design principles
- Fieldwork planning and logistics
- Participant observation strategies
- Key informant selection
- Cultural analysis frameworks
- Reflexivity in ethnography
- Writing ethnographic accounts

**Triggers**: "ethnography", "fieldwork", "participant observation", "cultural", "anthropological"

#### H2: Action Research Facilitator (NEW)

**Purpose**: Support participatory and action research approaches.

**Capabilities**:
- Action research cycle design (plan-act-observe-reflect)
- Stakeholder engagement strategies
- Community-based participatory research (CBPR)
- Collaborative inquiry methods
- Practical outcome documentation
- Change facilitation

**Triggers**: "action research", "participatory", "CBPR", "community-based", "practitioner research", "collaborative inquiry"

---

## Model Routing

### Complexity-Based Tier Assignment

| Tier | Model | Agents | Task Characteristics |
|------|-------|--------|----------------------|
| **HIGH** | Opus | A1, A2, A3, A5, C1, C2, C3, D4, E1, E3, G3, H1, H2 | Strategic decisions, complex reasoning, paradigm-level guidance |
| **MEDIUM** | Sonnet | A4, B1, B2, C4, D1, D2, E2, F3, F4, G1, G2, G4 | Standard analysis, protocol development, quality assessment |
| **LOW** | Haiku | B3, B4, D3, E4, F1, F2 | Calculations, search, code generation, checklists |

### Dynamic Routing Rules

```yaml
model_routing:
  complexity_signals:
    opus_triggers:
      - "design", "framework", "theory", "strategy"
      - "paradigm", "worldview", "philosophical"
      - "reviewer response", "methodology chapter"
      - "integration", "meta-inference"

    sonnet_triggers:
      - "analysis", "assessment", "protocol"
      - "interview guide", "sampling plan"
      - "journal selection", "abstract"

    haiku_triggers:
      - "calculate", "search", "generate code"
      - "checklist", "extract", "format"

  override_rules:
    - condition: "user explicitly requests thorough analysis"
      action: "upgrade one tier"
    - condition: "ecomode active"
      action: "prefer lower tier when possible"
    - condition: "ralph/sisyphus active"
      action: "maintain assigned tier for consistency"
```

---

## Core Systems

### 1. Research Project State

Maintains context throughout your entire research journey.

**Location**: `.research/project-state.yaml`

```yaml
project:
  name: "Your Project Name"
  type: "mixed_methods"  # quantitative | qualitative | mixed_methods
  paradigm: "pragmatist"  # positivist | interpretivist | pragmatist | transformative
  current_stage: 4
  sisyphus_active: true

research_context:
  research_question:
    main: "How do AI tutors affect student motivation and learning?"
    quantitative_strand: "What is the effect of AI tutors on achievement?"
    qualitative_strand: "How do students experience AI tutor interactions?"

  theoretical_framework:
    primary_theory: "Self-Determination Theory"
    integration_framework: "Pragmatist Mixed Methods"

  methodology:
    design_type: "Explanatory Sequential"
    phase_1: "Quasi-experimental (N=200)"
    phase_2: "Phenomenological interviews (n=15)"
    integration: "Joint display connecting QUAN results to QUAL themes"
```

### 2. Pipeline Templates

#### Quantitative Pipeline (PRISMA 2020)
```
Stage 1: Protocol → Stage 2: Search → Stage 3: Screen →
Stage 4: Extract → Stage 5: Quality → Stage 6: Analyze →
Stage 7: Write → Stage 8: Publish
```

#### Qualitative Pipeline
```
Stage 1: Design → Stage 2: Sampling → Stage 3: Data Collection →
Stage 4: Transcription → Stage 5: Coding → Stage 6: Theme Development →
Stage 7: Trustworthiness → Stage 8: Write → Stage 9: Member Check
```

#### Mixed Methods Pipeline
```
PHASE 1 (QUAN): Design → Collect → Analyze
     ↓
INTEGRATION: Connect → Joint Display → Meta-Inference
     ↑
PHASE 2 (QUAL): Design → Collect → Analyze
```

### 3. Integration Hub

| Category | Tools | Status |
|----------|-------|--------|
| **Office** | Excel, Word, PowerPoint | Ready |
| **Statistical** | R, Python, SPSS, Stata | Ready |
| **Qualitative** | NVivo, ATLAS.ti, MAXQDA | Guidance only |
| **Literature** | Semantic Scholar, OpenAlex, Zotero | API setup |
| **Visualization** | Mermaid, Nanobanana, ggplot2 | Ready/API |
| **Open Science** | OSF, AsPredicted, PROSPERO | Ready |

### 4. Guided Dialogue (Wizard)

Clear choice points for important decisions:

```
Question: "Which research paradigm aligns with your worldview?"

Options:
1. Positivist/Post-positivist (T=0.70)
   Objective reality, hypothesis testing, generalization

2. Interpretivist/Constructivist (T=0.55)
   Multiple realities, understanding meaning, context-bound

3. Pragmatist (T=0.45)
   Problem-centered, what works, mixed methods friendly

4. Transformative (T=0.30)
   Social justice focus, participatory, emancipatory
```

### 5. Auto-Documentation

Auto-generated documents by paradigm:

| Paradigm | Documents |
|----------|-----------|
| **All** | Decision Log, Methods Draft, Audit Trail |
| **Quantitative** | PRISMA Diagram, Analysis Scripts, Power Analysis |
| **Qualitative** | Codebook, Theme Map, Reflexivity Journal |
| **Mixed** | Joint Displays, Integration Matrix, Meta-Inference Summary |

---

## Human Checkpoints

### Required Checkpoints (System STOPS)

| Checkpoint | When | Decision |
|------------|------|----------|
| CP_RESEARCH_DIRECTION | Research question finalized | Confirm scope and direction |
| CP_PARADIGM_SELECTION | Methodology chapter | Approve worldview/paradigm |
| CP_THEORY_SELECTION | Framework chosen | Approve theoretical approach |
| CP_METHODOLOGY_APPROVAL | Design complete | Approve methodology |

### Recommended Checkpoints (System Pauses)

| Checkpoint | When | Decision |
|------------|------|----------|
| CP_ANALYSIS_PLAN | Before analysis | Review statistical/coding approach |
| CP_INTEGRATION_STRATEGY | Mixed methods only | Approve integration method |
| CP_QUALITY_REVIEW | Assessment done | Approve quality judgments |

### Optional Checkpoints (Defaults Available)

| Checkpoint | When | Default |
|------------|------|---------|
| CP_VISUALIZATION_PREFERENCE | Creating figures | Hybrid style |
| CP_RENDERING_METHOD | Export options | Standard format |

---

## VS-Research Methodology

### The Problem: AI Mode Collapse

```
Standard AI: "Recommend a methodology" → Survey (70% of the time)
             → All research looks similar
             → Limited methodological contribution

VS-Enhanced: "Recommend a methodology"
             → Step 1: Identify Survey as modal (explicitly consider)
             → Step 2: Explore alternatives (experiment, case study, ethnography)
             → Step 3: Select based on T-Score, RQ fit, and paradigm
             → Result: Differentiated, defensible methodology
```

### T-Score (Typicality Score)

| T-Score | Label | Meaning |
|---------|-------|---------|
| >= 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, requires strong justification |
| < 0.2 | Experimental | Highly novel, high risk/reward |

### VS Process (3-Stage)

```
Stage 1: Context & Modal Identification
  ├─ Understand research context and paradigm
  └─ Identify "obvious" recommendations (to consciously evaluate)

Stage 2: Divergent Exploration
  ├─ Direction A (T~0.6): Safe but differentiated
  ├─ Direction B (T~0.4): Balanced novelty
  └─ Direction C (T<0.3): Innovative/experimental

Stage 3: Selection & Execution
  ├─ Present options with T-Scores and paradigm fit
  ├─ Human selects direction
  └─ Execute with methodological rigor
```

---

## Quality Guardrails (Non-Negotiable)

### Universal Standards

| Guardrail | Description | Verification |
|-----------|-------------|--------------|
| Methodological Soundness | Defensible in peer review | Literature support |
| Internal Validity/Credibility | Threats acknowledged | Explicit limitations |
| Reproducibility/Dependability | Full documentation | Audit trail |
| Ethical Compliance | IRB/ethics met | Approval documentation |

### Paradigm-Specific Standards

| Paradigm | Quality Criteria | Checklist |
|----------|------------------|-----------|
| Quantitative | Validity, reliability, generalizability | CONSORT, STROBE |
| Qualitative | Credibility, transferability, dependability, confirmability | SRQR, COREQ |
| Mixed Methods | Legitimation criteria, integration quality | GRAMMS |

---

## OMC Integration

### Mode Compatibility

| OMC Mode | Research Coordinator Behavior |
|----------|------------------------------|
| **ultrawork** | Maximum parallelism, all available agent groups |
| **ecomode** | Token-efficient, prefer LOW tier, batch tasks |
| **ralph** | Sisyphus protocol active, persist until complete |
| **autopilot** | Full autonomous workflow with checkpoints |

### Parallel Execution Groups

```
Group 1: Research Foundation
  [A2 + A3] parallel after A1
  [A4 + C1/C2/C3] parallel after theory selection

Group 2: Literature & Data Collection
  [B1 + B4] parallel (search + monitoring)
  [D1 + D2 + D3] parallel (sampling + protocols)

Group 3: Analysis
  [E1 + E2] parallel for mixed methods
  [E4 + F1 + F2] parallel (code + quality checks)

Group 4: Publication
  [G1 + G2] parallel (journal + communication)
  [G3 + G4] parallel (review strategy + preregistration)
```

### OMC Mode Commands

```bash
ulw: 문헌 검색해줘        # ultrawork - maximum parallelism
eco: 통계 분석해줘        # ecomode - token efficient
ralph: 연구 설계 완료해줘  # persistence until done (Sisyphus)
autopilot: 체계적 문헌고찰 진행해줘  # full autonomous workflow
```

---

## Auto-Trigger Keywords

| Keywords | Agents Activated | Paradigm Signal |
|----------|------------------|-----------------|
| "research question", "연구 질문", "PICO", "SPIDER" | A1 | - |
| "theoretical framework", "이론", "conceptual model" | A2 | - |
| "worldview", "paradigm", "epistemology" | A5 | - |
| "literature review", "PRISMA", "systematic review" | B1 | Quantitative |
| "qualitative", "phenomenology", "grounded theory" | C2, E2 | Qualitative |
| "mixed methods", "integration", "joint display" | C3, E3 | Mixed |
| "interview", "focus group" | D2 | Qualitative |
| "statistics", "ANOVA", "regression" | E1, E4 | Quantitative |
| "thematic analysis", "coding", "themes" | E2 | Qualitative |
| "ethnography", "fieldwork" | H1 | Qualitative |
| "action research", "participatory" | H2 | Qualitative |
| "journal", "submission", "투고" | G1 | - |
| "reviewer", "peer review" | G3 | - |

---

## Quick Start

### For New Users

Simply tell Research Coordinator what you want to do:

```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어"
"Help me design a phenomenological study on teacher burnout"
"I need to design a mixed methods study"
```

The system will:
1. Detect your paradigm from your request
2. Activate appropriate agent pack
3. Guide you through conversational wizard
4. Enforce Sisyphus protocol for completion

### Entry Points

| Option | Description |
|--------|-------------|
| Start a new research project | Set up systematic review, qualitative study, or mixed methods |
| Continue existing project | Resume work with full context preserved |
| Get help with a specific task | Literature search, analysis, writing, etc. |
| Switch paradigm | Change methodology approach mid-project |

---

## Version History

- **v5.0.0**: Sisyphus protocol, paradigm detection, 27 agents, qualitative/mixed methods support
- **v4.0.0**: Context persistence, pipeline templates, integration hub, guided wizard
- **v3.2.0**: OMC integration, model routing, parallel execution
- **v3.1.0**: Conceptual Framework Visualizer (#21)
- **v3.0.0**: Creativity modules, user checkpoints, dynamic T-Score

---

## Module Reference

### Core Modules

| Module | Path | Purpose |
|--------|------|---------|
| Project State | `core/project-state.md` | Context persistence |
| Pipeline Templates | `core/pipeline-templates.md` | Research workflows |
| Integration Hub | `core/integration-hub.md` | Tool connections |
| Guided Wizard | `core/guided-wizard.md` | Conversation UX |
| Auto-Documentation | `core/auto-documentation.md` | Document generation |
| Sisyphus Protocol | `core/sisyphus-protocol.md` | Continuation enforcement |
| Paradigm Detection | `core/paradigm-detection.md` | Auto-detect methodology |

### Configuration Files

| File | Path | Purpose |
|------|------|---------|
| Project State | `.research/project-state.yaml` | Current project context |
| Sisyphus State | `.research/sisyphus-state.json` | Continuation tracking |
| Decision Log | `.research/decision-log.yaml` | Research decisions |
| Paradigm Config | `.research/paradigm-config.yaml` | Detected paradigm |
| Routing Config | `.omc/config/research-coordinator-routing.yaml` | Model routing |
| Checkpoints | `.omc/checkpoints/checkpoint-definitions.yaml` | Human checkpoints |

---

## Getting Started

1. **Start a conversation** with your research topic
2. **Let paradigm detection** identify your approach (or specify explicitly)
3. **Follow the guided wizard** through choice points
4. **Trust Sisyphus protocol** to maintain momentum
5. **Approve at checkpoints** to maintain human agency
6. **Export documentation** when ready

```
"I want to understand how teachers experience AI adoption in their classrooms"
```

Research Coordinator will detect qualitative signals, activate appropriate agents, and guide you from there - never stopping until your research is complete.
