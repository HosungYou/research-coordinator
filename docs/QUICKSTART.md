# Quick Start Guide

Get started with Diverga in under 5 minutes!

**Version**: 6.0.1 (Human-Centered Edition)

---

## What is Diverga?

Diverga is an AI research assistant that helps you make **creative, defensible research choices** while ensuring **human decisions remain with humans**.

Unlike other AI tools that always recommend the same obvious options (mode collapse), Diverga uses **Verbalized Sampling (VS)** methodology to present you with innovative alternatives.

---

## Installation (2 minutes)

### Option A: Clone and Install (Recommended)

```bash
git clone https://github.com/HosungYou/Diverga.git
cd Diverga
```

### Verify Installation

In Claude Code, simply describe your research need:

```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어요"
```

---

## Your First Research Session (3 minutes)

### Step 1: Describe Your Research

Simply tell Diverga what you want to research:

```
"AI 학습 시스템이 학생들에게 도움이 될 것 같은데, 연구 질문을 어떻게 만들어야 할까요?"
```

### Step 2: Wait for Checkpoint

Diverga will analyze your request and present options:

```
🔴 CHECKPOINT: CP_RESEARCH_DIRECTION

I've analyzed your research topic. Here are three directions:

Direction A (T≈0.6): AI tutoring effects on academic achievement
Direction B (T≈0.4): AI-enhanced self-regulated learning ⭐
Direction C (T≈0.2): Neuroplasticity-based AI learning systems

Which direction would you like to proceed?
```

### Step 3: Make Your Choice

Simply respond with your selection:

```
"Direction B, please"
```

### Step 4: Continue Through Checkpoints

Diverga will guide you through the research process, stopping at each checkpoint for your approval.

---

## How It Works

### VS-Research Methodology

Diverga uses **Verbalized Sampling (VS)** to prevent "Mode Collapse":

```
❌ Without VS:
   "이론 추천해줘" → "TAM 쓰세요" (always the same answer)

✅ With VS:
   "이론 추천해줘"
   → Phase 1: "TAM, UTAUT are predictable choices (T=0.9)"
   → Phase 2: "Exploring alternatives..."
   → Phase 3: "Differentiated theory: SDT × TAM integration (T=0.4)"
```

### T-Score System

Every recommendation comes with a **Typicality Score (T-Score)**:

| T-Score | Meaning | Recommendation |
|---------|---------|----------------|
| > 0.8 | Most common choice | ⚠️ Predictable - consider alternatives |
| 0.5-0.8 | Established alternative | ✅ Safe differentiation |
| 0.3-0.5 | Emerging approach | ✅ Innovative, well-justified |
| < 0.3 | Creative/Novel | ⚠️ Needs strong justification |

### Human Checkpoint System

Diverga stops at critical points and waits for your decision:

| Level | Icon | Behavior |
|-------|------|----------|
| **REQUIRED** | 🔴 | System STOPS - Cannot proceed without your approval |
| **RECOMMENDED** | 🟠 | System PAUSES - Strongly suggests your review |
| **OPTIONAL** | 🟡 | System ASKS - Defaults available if you skip |

---

## Agent Categories (33 Agents)

| Category | Count | Purpose |
|----------|-------|---------|
| A: Foundation | 6 | Research question, theory, ethics, paradigm |
| B: Evidence | 4 | Literature review, quality appraisal, effect sizes |
| C: Design | 4 | Quantitative, qualitative, mixed methods design |
| D: Data Collection | 4 | Sampling, interviews, observation, instruments |
| E: Analysis | 5 | Statistical analysis, coding, integration |
| F: Quality | 4 | Consistency, checklists, reproducibility, bias |
| G: Communication | 4 | Journal matching, communication, peer review |
| H: Specialized | 2 | Ethnography, action research |

---

## Common Use Cases

### Use Case 1: Planning a New Study

```
1. Describe your research topic
   → A1: Research Question Refiner activates
   → 🔴 CP_RESEARCH_DIRECTION: Choose your direction

2. Select theoretical framework
   → A2: Theoretical Framework Architect activates
   → 🔴 CP_THEORY_SELECTION: Approve framework

3. Design your methodology
   → C1/C2/C3: Design Consultant activates
   → 🔴 CP_METHODOLOGY_APPROVAL: Approve design
```

### Use Case 2: Literature Review

```
1. "I want to conduct a systematic review on [topic]"
   → B1: Systematic Literature Scout activates
   → Develops PRISMA-compliant search strategy

2. Quality assessment
   → B2: Evidence Quality Appraiser activates
   → Applies RoB, GRADE criteria

3. Effect size extraction
   → B3: Effect Size Extractor activates
   → Calculates and converts effect sizes
```

### Use Case 3: Data Analysis

```
1. "How should I analyze my data?"
   → E1: Quantitative Analysis Guide activates
   → 🟠 CP_ANALYSIS_PLAN: Review analysis plan

2. Code generation
   → E4: Analysis Code Generator activates
   → Generates R/Python/SPSS code

3. Sensitivity analysis
   → E5: Sensitivity Analysis Designer activates
   → Plans robustness checks
```

---

## Tips for Best Results

### 1. Provide Context

```
❌ "이론 추천해줘"

✅ "교육공학 분야에서 AI 기반 적응형 학습 시스템의
   학습 효과를 연구하려고 합니다.
   박사 학위 논문용으로 차별화된 이론을 추천해주세요."
```

### 2. Specify Your Goals

- First publication → Conservative approach (T > 0.5)
- Top-tier journal → Innovative approach (T < 0.5)
- Replication study → Standard approach (T > 0.6)

### 3. Take Time at Checkpoints

When you see 🔴 CHECKPOINT, carefully review the options before deciding. These are strategic research decisions that should be made thoughtfully.

### 4. Use Bilingual Input

```
English: "I want to conduct a systematic review"
Korean: "체계적 문헌고찰을 하고 싶어요"
Mixed: "메타분석을 하려는데, can you help?"
```

---

## Getting Help

### Documentation

- [Full Documentation](../README.md)
- [Agent Reference](./AGENT-REFERENCE.md)
- [CLAUDE.md](../CLAUDE.md) - System documentation
- [AGENTS.md](../AGENTS.md) - AI-readable documentation

### Issues

- [GitHub Issues](https://github.com/HosungYou/Diverga/issues)

---

## Key Differences from v5.0

| Feature | v5.0 (Sisyphus) | v6.0.1 (Human-Centered) |
|---------|-----------------|------------------------|
| Checkpoints | Could be bypassed | ✅ MANDATORY |
| OMC Modes | ralph/ultrawork/ecomode | ❌ Removed |
| Agent Naming | Numbered (01-21) | Category-based (A1-H2) |
| Agent Count | 27 | 33 |

---

## Next Steps

1. **Try it out**: Describe your research need and follow the checkpoints
2. **Explore agents**: Read the [Agent Reference](./AGENT-REFERENCE.md)
3. **Learn VS methodology**: Understand T-Scores and creative alternatives
4. **Join the community**: Star the repo on GitHub!

---

**Happy Researching!** 🧬

*Diverga: Where creativity meets rigor. Beyond the obvious, toward the innovative.*
