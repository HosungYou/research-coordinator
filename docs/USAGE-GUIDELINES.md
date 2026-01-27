# Diverga Usage Guidelines

**Version**: 6.1.0 (Human-Centered Edition + Humanization Pipeline)
**Last Updated**: 2026-01-26
**Platform**: Claude Code v1.0+

---

## Table of Contents

1. [Introduction](#introduction)
2. [Core Principles](#core-principles)
3. [Ethical Use Guidelines](#ethical-use-guidelines)
4. [Recommended Workflows](#recommended-workflows)
5. [Agent Selection Guide](#agent-selection-guide)
6. [Checkpoint Navigation](#checkpoint-navigation)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Version Compatibility](#version-compatibility)

---

## Introduction

### Purpose of This Document

Diverga Usage Guidelines provides comprehensive instruction for researchers, students, and academics on effectively using the Diverga system. This document bridges the gap between technical capability and practical research application.

### Target Audience

- **Researchers** conducting systematic reviews, meta-analyses, and empirical studies
- **Students** writing theses, dissertations, and research papers
- **Academics** seeking methodological rigor and innovative research approaches
- **Research Teams** coordinating complex, multi-phase research projects

### How to Use This Guide

- **New Users**: Start with [Core Principles](#core-principles) and [Recommended Workflows](#recommended-workflows)
- **Agent Reference**: Jump to [Agent Selection Guide](#agent-selection-guide) for specific tasks
- **Ethical Questions**: See [Ethical Use Guidelines](#ethical-use-guidelines)
- **Humanization Concerns**: Refer to [Ethical Use Guidelines - G6 Humanization](#g6-humanization-guidelines)
- **Problem Solving**: Navigate to [Troubleshooting](#troubleshooting)

---

## Core Principles

### Principle 1: Human-Centered Design

**Philosophy**: "AI assists, humans decide."

Diverga operates on the principle that critical research decisions must remain with human researchers. AI handles analysis, synthesis, and pattern detection—but humans make the final calls on research direction, methodology, and conclusions.

**What This Means**:
- ✅ AI generates options; you choose
- ✅ AI identifies alternatives; you evaluate
- ✅ AI checks quality; you make changes
- ❌ AI doesn't make final decisions for you
- ❌ AI doesn't bypass your approval

### Principle 2: AI as Assistant, Not Replacement

**Philosophy**: "Extend human capability, don't replace it."

Diverga supplements human expertise by:
- Automating routine analytical tasks
- Providing fresh perspectives through VS methodology
- Catching inconsistencies and gaps
- Generating options researchers hadn't considered
- Accelerating tedious but important verification steps

**What This Means**:
- ✅ Use AI to explore more options faster
- ✅ Use AI to verify your thinking
- ✅ Use AI to ensure methodological rigor
- ❌ Don't use AI to avoid learning
- ❌ Don't use AI to bypass your expertise

### Principle 3: Transparency Requirements

**Philosophy**: "Honesty builds trust."

Using AI in your research comes with transparency obligations:

**You Should Know**:
- When and how you used AI
- What capabilities and limitations AI has
- How AI-assisted writing differs from your own
- Your discipline's and institution's AI policies

**You Should Disclose**:
- To your institution (if required)
- To your target journal (if required)
- To your advisor/committee (always)
- To yourself (keep accurate records)

---

## Ethical Use Guidelines

### 3.1 Academic Integrity

#### What Constitutes Ethical Use

Ethical use of Diverga means:

| Action | Status | Example |
|--------|--------|---------|
| Using AI to develop research questions | ✅ **Ethical** | "Help me refine my research question about AI in education" |
| Using AI to brainstorm theoretical frameworks | ✅ **Ethical** | "Generate 3 theoretical framework options for my study" |
| Using AI to check methodology rigor | ✅ **Ethical** | "Review my design for validity threats" |
| Using AI to draft discussion sections | ✅ **Ethical** | "Draft a discussion based on my findings (which I'll revise)" |
| Using AI to humanize AI-written text | ✅ **Ethical** | "Check this section for AI patterns and help make it sound natural" |
| Using AI to design data analysis approaches | ✅ **Ethical** | "What analysis methods work for my research questions?" |
| Using AI to verify statistical calculations | ✅ **Ethical** | "Check my sample size calculation for errors" |

#### What to Avoid

**Do NOT use Diverga to**:

| Action | Why It's Wrong | Consequence |
|--------|----------------|-------------|
| Fabricate data or citations | Academic fraud | Retraction, expulsion, career damage |
| Plagiarize text without attribution | Intellectual dishonesty | Plagiarism detection flags |
| Misrepresent methodology | False claims | Study invalidation, retraction |
| Bypass human analysis steps | Avoiding learning | Undetected errors |
| Create fake participant data | Research fraud | Criminal liability |
| Deceive reviewers about AI use | Dishonesty | Retraction if discovered |
| Violate explicit institutional policies | Policy violation | Disciplinary action |

#### Disclosure Practices

**Best Practice: Proactive Disclosure**

The safest approach is transparent disclosure of AI use. Use these templates:

**For Journal Submissions**:

```markdown
## AI Use Statement

This manuscript was prepared with AI writing assistance (Anthropic Claude)
for conceptual development, methodology refinement, and drafting purposes.
All AI-generated content was reviewed, verified, and substantially edited by
the authors. The research conception, design, data collection, analysis, and
interpretation represent original work by the authors. The authors take full
responsibility for the accuracy and integrity of the work.

[If using humanization]
Portions of the manuscript were reviewed and edited for natural language
expression using AI-assisted humanization tools.
```

**For Theses/Dissertations**:

```markdown
## Declaration

I declare that this [thesis/dissertation] represents my original scholarly
work. AI writing assistance tools (Anthropic Claude) were used for
conceptual development, methodology consultation, and drafting support
under my direction. All intellectual contributions—including research
design, analysis interpretation, and conclusions—represent my original work.
I have read all generated content and take full responsibility for its
accuracy and appropriateness.

[Signature]  [Date]
```

**For Conference Presentations**:

```markdown
## Methodology Statement

This research was conducted with AI-assisted tools for literature synthesis,
methodology development, and presentation preparation. All findings, analysis,
and interpretations are original work of the researchers.
```

**For Institutional Requirements**:

```markdown
## AI Tool Usage Report

Research tools used: Diverga Research Assistant (Anthropic Claude)
Purpose: Methodology consultation, literature organization, writing support
Disclosure: [Full disclosure of specific uses]
```

---

### 3.2 G6 Humanization Guidelines

#### When Humanization Is Appropriate

Use the Humanization Pipeline (G5-G6) when:

| Scenario | Recommendation | Rationale |
|----------|-----------------|-----------|
| Your AI-generated text feels "robotic" | ✅ **Use humanization** | Improves readability and scholarly flow |
| Reviewing AI-drafted sections before submission | ✅ **Use humanization** | Ensures natural academic prose |
| Your institution permits AI writing with refinement | ✅ **Use humanization** | Demonstrates thoughtful AI use |
| Preparing final draft for publication | ✅ **Use humanization (conservative mode)** | Professional polish |
| Working with draft content you've substantially revised | ✅ **Use humanization** | Smooths your own revisions |
| Academic writing where disclosure is welcome | ✅ **Use humanization** | Transparency-supported approach |

#### When to Avoid Humanization

Do NOT use humanization to:

| Action | Why It's Wrong |
|--------|----------------|
| Hide AI use from reviewers | Deceptive practice |
| Make AI-generated content "undetectable" | Against AI ethics principles |
| Submit AI text claiming it's your original writing | Academic dishonesty |
| Avoid learning to write well | Undermines education |
| Bypass institutional AI policies | Policy violation |
| Create misleading submission | Integrity violation |

#### Disclosure Requirements for Humanization

**When using G5 (AI Pattern Detection) or G6 (Humanization)**:

**You MUST disclose**:
- ✅ That you used humanization tools
- ✅ What portions of your work were affected
- ✅ That AI was used in the writing process
- ✅ That you reviewed and edited all content

**You should explain**:
- That humanization improves readability without changing meaning
- That all statistics, citations, and data are unchanged
- That you verified accuracy of all transformed content

**Example Disclosure Statement for Humanization**:

```markdown
## AI Use and Humanization Statement

This manuscript incorporates AI-assisted writing tools (Anthropic Claude)
for initial drafting and conceptual development. Portions of the draft were
refined using an AI-assisted humanization tool (Diverga G5-G6 pipeline) to
improve prose quality and readability. The humanization tool only modified
expression and style—all data, statistics, citations, and substantive claims
remain unchanged from the author-verified draft.

Specifically:
- [Section] was initially AI-drafted, then substantially revised by authors
- [Section] was humanized to improve readability
- All figures, tables, and statistics [remain unchanged]
- All citations [verified for accuracy]

The authors take full responsibility for all content accuracy and
methodological integrity. [Date and signature]
```

---

## Recommended Workflows

### 4.1 Systematic Literature Review Workflow

**Duration**: 4-6 months | **Agents Used**: 12 | **Paradigm**: Quantitative

#### Phase 1: Foundation (Weeks 1-2)

**Step 1.1: Develop Research Question**
```
Diverga Agent: A1-Research-Question-Refiner
User Action: Describe your research topic
Expected Output: 3 PICO-based question options with T-Scores
Checkpoint: 🔴 CP_RESEARCH_DIRECTION (Choose your direction)
```

**Action Items**:
- [ ] Describe research topic to A1
- [ ] Review PICO framework analysis
- [ ] Choose research direction
- [ ] Approve CP_RESEARCH_DIRECTION

**Step 1.2: Build Theoretical Framework**
```
Diverga Agent: A2-Theoretical-Framework-Architect
User Action: Provide research question
Expected Output: Theory map with alternatives (VS methodology)
Checkpoint: 🔴 CP_THEORY_SELECTION (Select framework)
```

**Action Items**:
- [ ] Review framework options
- [ ] Consider T-Scores and novelty implications
- [ ] Select framework supporting your question
- [ ] Approve CP_THEORY_SELECTION

#### Phase 2: Search Strategy (Weeks 3-4)

**Step 2.1: Design PRISMA-Compliant Search**
```
Diverga Agents: B1-Systematic-Literature-Scout (parallel with B4-Research-Radar)
User Action: Confirm research question
Expected Output: Database-specific search strategies
Checkpoint: None (informational)
```

**Action Items**:
- [ ] Review database recommendations
- [ ] Customize search terms for your topic
- [ ] Finalize inclusion/exclusion criteria
- [ ] Document search strategy

**Step 2.2: Identify Papers**
```
Execute searches in:
- Semantic Scholar
- OpenAlex
- PubMed / ERIC (if applicable)
- PsycINFO (if applicable)
```

**Expected Result**: 1,000-10,000 identified papers (before screening)

#### Phase 3: Screening (Weeks 5-8)

**Step 3.1: Process PDF Batch**
```
Diverga Agent: B5-Parallel-Document-Processor (NEW in v6.1+)
User Action: Upload PDF folder
Expected Output: Extracted text, metadata, searchable database
Checkpoint: None (processing)
```

**Benefits**:
- Processes 100+ PDFs efficiently
- No memory overflow issues
- Organized for next step

**Step 3.2: Quality Assessment**
```
Diverga Agents: B2-Evidence-Quality-Appraiser (parallel with B3-Effect-Size-Extractor)
User Action: Provide full texts
Expected Output: RoB 2.0 ratings + effect size extractions
Checkpoint: None (informational)
```

**Action Items**:
- [ ] Review quality appraisal criteria
- [ ] Verify quality assessments (spot-check)
- [ ] Extract effect sizes
- [ ] Document any disagreements

#### Phase 4: Meta-Analysis (Weeks 9-12)

**Step 4.1: Statistical Analysis**
```
Diverga Agents: E1-Quantitative-Analysis-Guide → E5-Sensitivity-Analysis-Designer
User Action: Provide cleaned data
Expected Output: Analysis plan + sensitivity checks
Checkpoint: 🟠 CP_ANALYSIS_PLAN (Review and approve)
```

**Action Items**:
- [ ] Review analysis method options
- [ ] Verify assumptions checking procedure
- [ ] Approve analysis approach
- [ ] Prepare for analysis

**Step 4.2: Generate Code**
```
Diverga Agent: E4-Analysis-Code-Generator
User Action: Confirm analysis plan
Expected Output: Reproducible R/Python/SPSS code
Checkpoint: None (implementation)
```

**Step 4.3: Run Analysis**
```
You execute the generated code
Expected Output: Meta-analysis results + figures
```

#### Phase 5: Manuscript Preparation (Weeks 13-16)

**Step 5.1: Quality Review**
```
Diverga Agents: F2-Checklist-Manager (PRISMA 2020)
User Action: Provide draft manuscript
Expected Output: Item-by-item checklist
Checkpoint: None (verification)
```

**Step 5.2: Check AI Patterns** (NEW in v6.1)
```
Diverga Agent: G5-Academic-Style-Auditor
User Action: Submit manuscript sections
Expected Output: AI probability score + pattern report
Checkpoint: 🟠 CP_HUMANIZATION_REVIEW (if AI probability > 40%)
```

**Step 5.3: Humanize if Needed** (NEW in v6.1)
```
Diverga Agent: G6-Academic-Style-Humanizer
User Action: Approve humanization mode
Expected Output: Humanized text + transformation log
Checkpoint: 🟡 CP_HUMANIZATION_VERIFY (Approve result)
```

**Transformation Modes** (Choose one):
- **Conservative**: HIGH-risk patterns only, 5-15% text change
- **Balanced** (Recommended): HIGH + MEDIUM patterns, 15-30% text change
- **Aggressive**: ALL patterns, 30-50% text change

#### Phase 6: Publication (Weeks 17-20)

**Step 6.1: Select Journal**
```
Diverga Agent: G1-Journal-Matcher
User Action: Provide manuscript type and focus
Expected Output: Ranked journal recommendations
Checkpoint: None (decision point)
```

**Step 6.2: Prepare Response Strategy**
```
Diverga Agent: G3-Peer-Review-Strategist
User Action: Plan for potential reviewer comments
Expected Output: Response templates + mitigation strategies
Checkpoint: None (planning)
```

**Verification Checklist** (Before Submission):

- [ ] All citations: 100% accurate
- [ ] All statistics: 100% preserved
- [ ] Meaning: 95%+ preserved
- [ ] AI patterns: Reduced appropriately
- [ ] Academic tone: Maintained
- [ ] PRISMA checklist: Complete (27/27 items)

---

### 4.2 Meta-Analysis Workflow

**Duration**: 8-12 weeks | **Agents Used**: 14 | **Paradigm**: Quantitative

**Similar to Systematic Review but focuses on quantitative synthesis**

**Key Differences**:

1. **Start with Literature Review** (not systematic review)
2. **Heavy emphasis on effect size extraction** (B3 focus)
3. **Statistical modeling** (random-effects, moderators)
4. **Publication bias assessment** (E5 focus)

**Additional Checkpoints**:
- 🟠 CP_EFFECT_SIZE_STRATEGY: How to handle heterogeneous effects?
- 🟠 CP_MODERATOR_ANALYSIS: Which moderators to test?

---

### 4.3 Research Design Workflows

#### 4.3.1 Quantitative Research Workflow

**Duration**: 8-12 weeks | **Agents Used**: 10

```
A1 (Question) → A2 (Theory) → 🔴 CP_THEORY_SELECTION
                                ↓
                         C1 (Quant Design) → 🔴 CP_METHODOLOGY_APPROVAL
                                ↓
                    D1 (Sampling) → D4 (Measurement)
                                ↓
            D1 sampling strategy + D4 instrument validation plan
                                ↓
            Execute data collection
                                ↓
            E1 (Analysis) → 🟠 CP_ANALYSIS_PLAN → E4 (Code)
                                ↓
                        Run analysis + E5 (Sensitivity)
```

**Key Checkpoints**:
- 🔴 CP_RESEARCH_DIRECTION: Question focus
- 🔴 CP_THEORY_SELECTION: Framework choice
- 🔴 CP_METHODOLOGY_APPROVAL: Design rigor
- 🟠 CP_ANALYSIS_PLAN: Statistical approach

#### 4.3.2 Qualitative Research Workflow

**Duration**: 12-18 weeks | **Agents Used**: 9

```
A5 (Paradigm) → 🔴 CP_PARADIGM_SELECTION
                        ↓
        A1 (Question) → A2 (Theory) → 🔴 CP_THEORY_SELECTION
                        ↓
                C2 (Qual Design) → 🔴 CP_METHODOLOGY_APPROVAL
                        ↓
            D1 (Sampling) → D2 (Interview)
                        ↓
            Conduct interviews (with D3 observation protocols)
                        ↓
            B5 (Parallel Document Processing) - Process transcripts
                        ↓
            E2 (Qual Coding) → F4 (Trustworthiness) → F2 (COREQ)
```

**Key Checkpoints**:
- 🔴 CP_PARADIGM_SELECTION: Methodology approach (phenomenology, grounded theory, case study, ethnography, action research)
- 🔴 CP_THEORY_SELECTION: Theoretical lens
- 🔴 CP_METHODOLOGY_APPROVAL: Design rigor (saturation targets, sampling logic)

#### 4.3.3 Mixed Methods Workflow

**Duration**: 16-24 weeks | **Agents Used**: 13

```
PHASE 1: PLANNING
─────────────────
A1 (Question) → A2 (Theory) → C3 (Mixed Design)
                                ↓
                    🔴 CP_METHODOLOGY_APPROVAL

PHASE 2: QUANTITATIVE
─────────────────────
C1 (Quant) → E1 (Analysis) → Results inform QUAL

PHASE 3: QUALITATIVE
────────────────────
C2 (Qual) → E2 (Coding) → Findings

PHASE 4: INTEGRATION
────────────────────
E3 (Mixed Integration) → 🟠 CP_INTEGRATION_STRATEGY
        ↓
A6 (Visual Framework) → Joint Display + Meta-Inferences
```

**Key Checkpoints**:
- 🔴 CP_PARADIGM_SELECTION: Mixed methods approach (sequential explanatory, sequential exploratory, convergent parallel)
- 🔴 CP_METHODOLOGY_APPROVAL: Both QUAN and QUAL design
- 🟠 CP_INTEGRATION_STRATEGY: How to integrate findings

---

## Agent Selection Guide

### Understanding Agent Tiers

Diverga uses three model tiers for agents:

| Tier | Model | Speed | Cost | Best For |
|------|-------|-------|------|----------|
| **LOW** | Haiku | Fast (< 10 sec) | Low | Simple tasks, information lookup, verification |
| **MEDIUM** | Sonnet | Standard (15-30 sec) | Moderate | Most research tasks, moderate complexity |
| **HIGH** | Opus | Slower (30-60 sec) | Higher | Complex reasoning, theory, design decisions |

### When to Use Each Agent

#### Foundation Agents (Category A: 6 agents)

| Agent | Use When | Model | Checkpoint |
|-------|----------|-------|-----------|
| **A1** Research Question Refiner | Starting a research project | HIGH (Opus) | 🔴 REQUIRED |
| **A2** Theoretical Framework Architect | Building theoretical foundation | HIGH (Opus) | 🔴 REQUIRED |
| **A3** Devil's Advocate | Vetting your research design | HIGH (Opus) | - |
| **A4** Research Ethics Advisor | Planning IRB application | MEDIUM (Sonnet) | 🔴 REQUIRED |
| **A5** Paradigm & Worldview Advisor | Choosing research approach | HIGH (Opus) | 🔴 REQUIRED |
| **A6** Conceptual Framework Visualizer | Creating framework diagrams | MEDIUM (Sonnet) | 🟡 OPTIONAL |

#### Evidence Agents (Category B: 5 agents)

| Agent | Use When | Model | Checkpoint |
|--------|----------|-------|-----------|
| **B1** Systematic Literature Scout | Planning systematic review | MEDIUM (Sonnet) | - |
| **B2** Evidence Quality Appraiser | Assessing paper quality (RoB, GRADE) | MEDIUM (Sonnet) | - |
| **B3** Effect Size Extractor | Converting statistics to effect sizes | LOW (Haiku) | - |
| **B4** Research Radar | Monitoring research trends | LOW (Haiku) | - |
| **B5** Parallel Document Processor | Processing 50+ PDFs efficiently | HIGH (Opus) coordinator + Haiku workers | - |

#### Design Agents (Category C: 4 agents)

| Agent | Use When | Model | Checkpoint |
|--------|----------|-------|-----------|
| **C1** Quantitative Design Consultant | Designing quantitative study | HIGH (Opus) | 🔴 REQUIRED |
| **C2** Qualitative Design Consultant | Designing qualitative study | HIGH (Opus) | 🔴 REQUIRED |
| **C3** Mixed Methods Design Consultant | Integrating QUAN + QUAL | HIGH (Opus) | 🔴 REQUIRED |
| **C4** Experimental Materials Developer | Creating intervention materials | MEDIUM (Sonnet) | - |

#### Data Collection Agents (Category D: 4 agents)

| Agent | Use When | Model | Checkpoint |
|--------|----------|-------|-----------|
| **D1** Sampling Strategy Advisor | Planning sample recruitment | MEDIUM (Sonnet) | - |
| **D2** Interview/Focus Group Specialist | Creating interview guides | MEDIUM (Sonnet) | - |
| **D3** Observation Protocol Designer | Planning observation studies | LOW (Haiku) | - |
| **D4** Measurement Instrument Developer | Building scales/surveys | HIGH (Opus) | 🔴 REQUIRED |

#### Analysis Agents (Category E: 5 agents)

| Agent | Use When | Model | Checkpoint |
|--------|----------|-------|-----------|
| **E1** Quantitative Analysis Guide | Planning statistical analysis | HIGH (Opus) | 🟠 RECOMMENDED |
| **E2** Qualitative Coding Specialist | Analyzing interview transcripts | HIGH (Opus) | - |
| **E3** Mixed Methods Integration | Integrating QUAN + QUAL findings | HIGH (Opus) | 🟠 RECOMMENDED |
| **E4** Analysis Code Generator | Need R/Python/SPSS code | LOW (Haiku) | - |
| **E5** Sensitivity Analysis Designer | Planning robustness checks | MEDIUM (Sonnet) | - |

#### Quality Agents (Category F: 5 agents)

| Agent | Use When | Model | Checkpoint |
|--------|----------|-------|-----------|
| **F1** Internal Consistency Checker | Verifying numerical accuracy | LOW (Haiku) | - |
| **F2** Checklist Manager | PRISMA/CONSORT/STROBE compliance | LOW (Haiku) | - |
| **F3** Reproducibility Auditor | OSF/Open Science assessment | MEDIUM (Sonnet) | - |
| **F4** Bias & Trustworthiness Detector | Identifying bias/quality issues | MEDIUM (Sonnet) | - |
| **F5** Humanization Verifier | Verifying humanization quality | LOW (Haiku) | - |

#### Communication Agents (Category G: 6 agents)

| Agent | Use When | Model | Checkpoint |
|--------|----------|-------|-----------|
| **G1** Journal Matcher | Selecting target journals | MEDIUM (Sonnet) | - |
| **G2** Academic Communicator | Writing abstracts/summaries | MEDIUM (Sonnet) | - |
| **G3** Peer Review Strategist | Responding to reviewer comments | HIGH (Opus) | 🟠 RECOMMENDED |
| **G4** Preregistration Composer | Creating OSF preregistration | MEDIUM (Sonnet) | 🟠 RECOMMENDED |
| **G5** Academic Style Auditor | Detecting AI patterns | MEDIUM (Sonnet) | - |
| **G6** Academic Style Humanizer | Transforming AI patterns | HIGH (Opus) | 🟠 RECOMMENDED |

#### Specialized Agents (Category H: 2 agents)

| Agent | Use When | Model | Checkpoint |
|--------|----------|-------|-----------|
| **H1** Ethnographic Research Advisor | Planning ethnographic study | HIGH (Opus) | 🔴 REQUIRED |
| **H2** Action Research Facilitator | Planning PAR/CBPR project | HIGH (Opus) | 🔴 REQUIRED |

### Agent Selection by Task

| Research Task | Primary Agent | Supporting Agents | Complexity |
|---|---|---|---|
| Refine vague research idea | A1 | A5, A3 | Complex |
| Build theoretical framework | A2 | A1, A3, A6 | Complex |
| Critique research design | A3 | A1, A2, A4 | Complex |
| IRB preparation | A4 | A1, D4 | Moderate |
| Choose methodology approach | A5 | A1, C1/C2/C3 | Complex |
| Visualize framework | A6 | A2, E3 | Simple |
| Systematic review strategy | B1 | B4, D1 | Moderate |
| Assess paper quality | B2 | B1 | Simple |
| Extract effect sizes | B3 | B2 | Simple |
| Literature trends | B4 | B1 | Simple |
| Process PDFs (50+) | B5 | B2, B3 | Complex |
| Design quantitative study | C1 | D1, D4, E1 | Complex |
| Design qualitative study | C2 | D2, D3, E2 | Complex |
| Design mixed methods | C3 | C1, C2, E3 | Complex |
| Create experimental materials | C4 | C1 | Moderate |
| Determine sample size | D1 | C1, E1 | Moderate |
| Create interview guide | D2 | C2, D1 | Moderate |
| Design observations | D3 | C2 | Simple |
| Develop scale/instrument | D4 | D1, E1 | Complex |
| Plan statistical analysis | E1 | E4, E5 | Complex |
| Qualitative coding | E2 | D2, D3 | Moderate |
| Mix QUAN + QUAL findings | E3 | E1, E2, A6 | Complex |
| Generate analysis code | E4 | E1 | Simple |
| Design sensitivity analysis | E5 | E1 | Moderate |
| Verify numerical accuracy | F1 | E1, E4 | Simple |
| Reporting compliance check | F2 | C1/C2/C3 | Simple |
| Open Science audit | F3 | F2 | Moderate |
| Identify biases | F4 | C1/C2/C3 | Moderate |
| Verify humanization | F5 | G5, G6 | Simple |
| Find target journals | G1 | G2 | Simple |
| Write abstract/summary | G2 | G1 | Moderate |
| Respond to reviewers | G3 | A3, F4 | Moderate |
| Create preregistration | G4 | A1, C1/C2/C3 | Moderate |
| Check AI patterns | G5 | G2 | Moderate |
| Humanize text | G6 | G5, F5 | Moderate |
| Design ethnography | H1 | C2, D3, E2 | Complex |
| Plan action research | H2 | C2, D1, D2 | Complex |

---

## Checkpoint Navigation

### Understanding Checkpoint Types

Diverga uses three checkpoint levels. Understanding what each means and how to respond is critical.

#### 🔴 REQUIRED Checkpoints (Mandatory)

**What it means**: The system **STOPS** and **CANNOT proceed** without your explicit approval.

**When triggered**: Critical research decisions that fundamentally shape your study

**Examples**:
- `CP_RESEARCH_DIRECTION`: Choosing between 3 research question options
- `CP_THEORY_SELECTION`: Approving theoretical framework
- `CP_METHODOLOGY_APPROVAL`: Finalizing research design
- `CP_PARADIGM_SELECTION`: Choosing quantitative/qualitative/mixed approach

**How to Respond**:

```
🔴 CHECKPOINT: CP_RESEARCH_DIRECTION

I've analyzed your research topic. Here are three directions:

Direction A (T≈0.8): Traditional AI effectiveness on test scores
Direction B (T≈0.5): AI-supported self-regulated learning ⭐
Direction C (T≈0.2): Neuroplasticity-enhanced AI systems

T-Score: 0 (novel) to 1.0 (common)
⭐ = Recommended for differentiation

YOUR RESPONSE REQUIRED:
Enter: "A", "B", "C", or describe preferred direction
```

**Your Response**:
```
"Direction B, please. The self-regulated learning angle
is more relevant to my institution's focus."
```

**After Your Response**: System proceeds to next stage

---

#### 🟠 RECOMMENDED Checkpoints (Suggested)

**What it means**: The system **PAUSES** and **strongly suggests** your review before proceeding.

**When triggered**: Important decisions where alternatives exist but defaults are available

**Examples**:
- `CP_ANALYSIS_PLAN`: Reviewing statistical approach options
- `CP_INTEGRATION_STRATEGY`: Deciding how to combine QUAN + QUAL findings
- `CP_HUMANIZATION_REVIEW`: Choosing humanization intensity level
- `CP_RESPONSE_APPROVAL`: Reviewing draft response to reviewers

**How to Respond**:

```
🟠 CHECKPOINT: CP_ANALYSIS_PLAN

Here are three analysis approaches:

Approach A (Standard): Independent t-tests per outcome
Approach B (Recommended): MANOVA with follow-up univariates ⭐
Approach C (Advanced): Multilevel modeling with random intercepts

Recommendation: B - Balances power, interpretability,
                  and accounts for outcome correlation

SUGGESTED ACTION:
[A] Proceed with Approach A (skip to code generation)
[B] Proceed with Approach B (recommended)
[C] Proceed with Approach C (will take longer to set up)
[D] Enter different analysis approach
[SKIP] Use default (Approach B) and continue
```

**Your Response**:
```
"B - Approach B makes sense for my study.
I have correlated outcomes that should be analyzed together."
```

**After Your Response**: System proceeds with your choice

---

#### 🟡 OPTIONAL Checkpoints (Informational)

**What it means**: The system **ASKS** for your input but has sensible defaults if you skip.

**When triggered**: Preferences or refinements where the system has good defaults

**Examples**:
- `CP_VISUALIZATION_PREFERENCE`: Visual style preferences
- `CP_HUMANIZATION_VERIFY`: Final review of humanized text (can approve/skip)

**How to Respond**:

```
🟡 CHECKPOINT: CP_HUMANIZATION_VERIFY

Humanization Complete ✅

Before/After Comparison:

BEFORE: "This groundbreaking research delves into the crucial
role of AI in fostering student learning outcomes."

AFTER:  "This research examines how AI affects student learning
outcomes."

Statistics:
- AI Probability: 67% → 28% (reduced by 39%)
- Patterns Fixed: 18 → 4
- Text Changed: 22%

Citation Accuracy: ✅ 100%
Statistical Values: ✅ 100% unchanged

YOUR OPTIONS:
[A] Approve and use humanized version
[B] Review specific transformations
[C] Revert to original version
[SKIP] Approve and continue (default)
```

**Your Response** (any of these work):
```
"Approve and use it"
or "Skip" (auto-approves)
or just hit Enter
```

### Required vs Optional Information

When a checkpoint asks for information, know what's mandatory vs optional:

#### 🔴 REQUIRED Information:

Must provide complete answer. System cannot proceed otherwise.

```
Which research paradigm?
(Required field - cannot skip)

[1] Quantitative (experimental, survey, correlational)
[2] Qualitative (phenomenology, grounded theory, case study)
[3] Mixed Methods (sequential, convergent, embedded)

>>> _
```

**What to do**:
- Choose one option clearly
- If unsure, ask for explanation first: "Explain the differences"

#### 🟠 RECOMMENDED Information:

Should provide but defaults available:

```
Analysis power target?
(Recommended: affects sample size calculations)

[A] Conservative (.90 power) - More participants
[B] Standard (.80 power) ← Default ⭐
[C] Exploratory (.70 power) - Fewer participants

>>> _
```

**What to do**:
- If confident, choose option
- If unsure, accept default: "Use default (B)"

#### 🟡 OPTIONAL Information:

Can skip entirely if you want:

```
Color preference for framework diagram?
(Optional: affects visualization only)

[1] Academic Blue-Gray
[2] Nature Publication Style
[3] Conference Presentation Style

>>> Skip (use default)
```

**What to do**:
- Skip if it doesn't matter
- Or choose if you have a preference

### How to Respond to Checkpoints

#### Format 1: Direct Selection
```
"Option B"
or
"B"
or
"[B]"
```

#### Format 2: Explanation with Selection
```
"Direction B - the self-regulated learning angle aligns
with my institution's learning sciences focus"
```

#### Format 3: Ask for Clarification First
```
"Can you explain the difference between Option A and Option B?"
[Wait for explanation]
"After that explanation, I choose Option B"
```

#### Format 4: Skip (For 🟠 and 🟡 only)
```
"Skip"
or
"Use default"
or
"Continue with default"
```

#### Format 5: Modify Default
```
"None of the options work. I want to use ANCOVA instead of MANOVA."
[Diverga adapts to your specification]
```

### Common Checkpoint Responses

| Scenario | How to Respond |
|----------|----------------|
| **Uncertain between options** | "Explain the pros/cons of each" (ask first) |
| **All options seem reasonable** | "Which is your recommendation?" |
| **Want custom option** | "I prefer [custom approach]" |
| **Need to change earlier choice** | "Can we go back and reconsider the theory selection?" |
| **Time pressure** | "Use your recommendation" or "Skip if possible" |
| **Too technical** | "Explain this for a non-statistician" |
| **Want to move forward** | "Skip" or "Use default" |

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "I chose an option at a checkpoint, but the system ignored it"

**Cause**: System didn't recognize your response format

**Solution**:
```
✗ Wrong: "I like option B the best because..."
✓ Correct: "Option B" (clear answer first, explain after)
```

**How to Fix**:
- Restate your choice clearly: "My choice is B"
- Rephrase if needed: "I want to proceed with Direction B"
- If still unclear, ask: "How should I format my response?"

---

#### Issue 2: "The system reached a checkpoint I didn't want"

**Cause**: Checkpoint is mandatory (🔴) and cannot be skipped

**Solution**:
- Understand this is a **required decision point**
- If you need time: "I need to think about this. Can I pause here?"
- If you want to change earlier decision: "Can we revisit the research question?"

**Prevention**:
- Know checkpoints in your workflow (see workflows section)
- Prepare answers before starting if time is limited

---

#### Issue 3: "I'm not getting the agent I need"

**Cause 1**: Wrong trigger keywords
```
✗ "I need help with my research"
✓ "I need to develop a systematic review search strategy"
```

**Cause 2**: Agent has prerequisites
- B3 (Effect Size Extractor) needs specific statistics
- E1 (Analysis Guide) needs research design first

**Solution**:
1. Check Agent Selection Guide (this document)
2. Use specific agent name: "Activate A2-Theoretical-Framework-Architect"
3. Provide complete context (agent will ask for info if missing)

---

#### Issue 4: "I don't understand the checkpoint options"

**Solution**: Ask for clarification

```
"Can you explain what these T-Scores mean for my research?"
or
"Why is Option B recommended over A?"
or
"What are the practical differences between these designs?"
```

**Diverga will**:
- Explain each option in plain language
- Clarify what T-Score means
- Show implications for your research
- Help you make informed decision

---

#### Issue 5: "I want to go back to an earlier checkpoint"

**Cause**: You realized an earlier decision was wrong

**Solution**:
```
"Can we revisit the research question checkpoint?"
or
"I want to reconsider the methodology I chose"
```

**What happens**:
- Diverga returns to that checkpoint
- You can change your choice
- Subsequent decisions adjust accordingly

---

#### Issue 6: "The humanization checkpoint is confusing"

**Cause**: Three new agents in v6.1.0 (G5, G6, F5) are unfamiliar

**Solution**: Understand the pipeline

```
Step 1: G5 (Academic Style Auditor)
        ↓
        Analyzes your text for AI patterns
        ↓
        Reports: AI probability + pattern list

Step 2: 🟠 CP_HUMANIZATION_REVIEW
        ↓
        You decide: humanize or skip?
        You choose: conservative/balanced/aggressive mode?

Step 3: G6 (Academic Style Humanizer)
        ↓
        Transforms patterns to natural prose
        ↓
        Preserves: 100% citations, statistics, meaning

Step 4: F5 (Humanization Verifier)
        ↓
        Checks quality of transformation
        ↓
        Approves or flags for review

Step 5: 🟡 CP_HUMANIZATION_VERIFY
        ↓
        You approve final result
```

**Best Response**:
- Trust the process initially
- Review transformation log
- If satisfied: approve
- If not: ask for specific changes

---

#### Issue 7: "How do I disclose humanization in my submission?"

**Solution**: Use disclosure statement (provided in Ethical Use section)

Quick answer:
```
"I used Diverga with humanization for prose refinement.
All facts, citations, and data are unchanged.
I reviewed and approved all changes."
```

Then use full template from Section 3.2

---

#### Issue 8: "The checkpoint system feels slow. Can I skip checkpoints?"

**Cause**: 🔴 checkpoints are mandatory for a reason

**Understanding**:
- 🔴 REQUIRED: Cannot skip (research integrity checkpoints)
- 🟠 RECOMMENDED: Can skip but not advised
- 🟡 OPTIONAL: Safe to skip

**Speed tips**:
1. **Prepare in advance**: Know what you'll choose before checkpoint
2. **Use defaults**: Say "skip" on 🟠 and 🟡 checkpoints
3. **Trust recommendations**: Marked with ⭐
4. **Parallel execution**: Some agents run simultaneously

---

#### Issue 9: "What if I disagree with an agent's recommendation?"

**Solution**: You're in control

```
Diverga: "I recommend MANOVA analysis"
You: "I prefer independent t-tests because..."
Result: System adapts to your choice
```

**Diverga is advisory, not authoritative**

---

#### Issue 10: "I want different output format"

**Solution**: Ask for format you need

```
"Can you present the effect size extraction in a table format?"
or
"Generate code in Python instead of R"
or
"Create a step-by-step checklist I can check off"
```

**Diverga will reformat**

---

### How to Reset or Start Over

#### Reset Checkpoint Decisions

```
"Can we start over from the beginning?"
or
"Reset all checkpoint decisions"
```

**Effect**: Returns to initial research question, clears all downstream decisions

#### Reset Specific Checkpoint

```
"I want to reconsider the methodology checkpoint"
```

**Effect**: Returns to that checkpoint, keeps earlier decisions

#### Clear Project State

```
"Start a completely new research project"
```

**Effect**: Clears all project state, begins fresh

---

### Getting Help

**For Technical Issues**:
- GitHub Issues: https://github.com/HosungYou/Diverga/issues
- Check CHANGELOG.md for version-specific issues

**For Conceptual Questions**:
- Reference this guide (USAGE-GUIDELINES.md)
- Read AGENT-REFERENCE.md for agent-specific details
- Check QUICKSTART.md for fast overview

**For Research Method Questions**:
- Ask the appropriate agent directly
- Use A3-Devil's Advocate to critique your approach
- Request explanation before committing

---

## Best Practices

### DO's and DON'Ts

#### DO ✅

| Practice | Why | Example |
|----------|-----|---------|
| **Use Diverga early** | Shapes better research | Start in research question phase |
| **Engage with checkpoints** | Your decisions matter | Carefully review each option |
| **Review agent outputs** | Verify accuracy | Spot-check effect size conversions |
| **Disclose AI use** | Maintains integrity | Include AI statement in submissions |
| **Iterate with agents** | Refine through dialogue | Ask for alternatives, explanations |
| **Use parallel processing** | Save time on large tasks | Submit 100 PDFs to B5 at once |
| **Preserve criticism** | Strengthen work | Use A3-Devil's Advocate regularly |
| **Document decisions** | Create audit trail | Save checkpoint choices |

#### DON'T ❌

| Practice | Why | Example |
|----------|-----|---------|
| **Blindly accept defaults** | You may want alternatives | Always review 3 options at checkpoints |
| **Skip research question development** | Weak foundation ruins study | Never skip A1 step |
| **Submit without disclosure** | Academic integrity issues | Always include AI use statement |
| **Use humanization to hide AI** | Unethical practice | Be transparent about humanization |
| **Ignore quality checkpoints** | Errors propagate | Always run F2 checklist before submission |
| **Assume one agent is enough** | Misses integrated perspective | Use complementary agents (e.g., A2 + A3) |
| **Override ethical guidelines** | Legal and career risk | Never fabricate data or citations |
| **Skip checkpoint decisions** | Lose opportunity to steer research | Engage at every 🔴 checkpoint |

---

### Tips for Effective Use

#### 1. Provide Rich Context

**Weak**: "Help me with statistics"

**Better**: "I have N=145 participants in a 2×3 experiment
(AI intervention vs. control, across 3 grade levels).
My outcome is a standardized test.
What analysis should I use?"

**Why**: Agents tailor recommendations to your specific situation

#### 2. Engage with Alternatives

**Avoid**: Accepting first suggestion

**Better**:
```
"Show me 3 theoretical frameworks for this study"
[Review all 3]
"Why is framework B recommended?"
[Understand rationale]
"I'm going to choose framework C because..."
[Explain your reasoning]
```

**Why**: You learn more and make better decisions

#### 3. Use Agents in Sequence

**Workflow matters**:
```
A1 (Question) → A2 (Theory) → C1/C2/C3 (Design)
```

**Not**: Jump directly to data analysis

**Why**: Earlier agents set up later steps correctly

#### 4. Verify Critical Numbers

**Always verify**:
- Sample size calculations (affects entire study)
- Effect size extractions (for meta-analysis)
- Statistical results (run code yourself)

**Tools**:
- F1-Internal Consistency Checker
- E4-Code Generator + your own execution

#### 5. Use B5 for Scale

**For 50+ documents**:
- Use B5-Parallel-Document-Processor
- Saves time (processes in parallel)
- Maintains quality (no memory issues)

**For < 20 documents**:
- Individual agents can handle it

#### 6. Leverage Parallel Execution

**These can run simultaneously** (in same message):
```
B1 (Literature Scout) + B2 (Quality) + B4 (Radar) = Parallel
```

**These must run sequentially** (in order):
```
A1 → A2 → C1 → E1 (each depends on previous)
```

#### 7. Humanization Best Practices

**DO humanize**:
- Sections with high AI probability (> 50%)
- Content you're disclosing as AI-assisted
- Drafts that need natural prose for publication

**DON'T humanize**:
- Content claiming to be entirely your own
- Situations where disclosure isn't possible
- Material that should preserve original voice

**Use conservative mode** for academic writing

**Use balanced mode** for most situations

**Use aggressive mode** only for informal content

---

### Common Success Patterns

#### Pattern 1: The Careful Planner

1. Develops research question thoroughly (A1)
2. Builds theoretical framework deliberately (A2)
3. Critiques design multiple times (A3)
4. Plans every step before execution
5. **Result**: Highly rigorous, well-planned study

**Best for**: Doctoral dissertations, high-stakes research

#### Pattern 2: The Agile Researcher

1. Quick research question development (A1)
2. Rapid literature search (B1)
3. Parallel document processing (B5)
4. Fast analysis and revision cycles
5. **Result**: Quick turnaround, adaptable approach

**Best for**: Time-sensitive projects, exploratory research

#### Pattern 3: The Quality-First Scholar

1. Thorough foundation setup (A1-A6)
2. Heavy use of critique agent (A3)
3. Multiple quality checkpoints (F1-F4)
4. Humanization before submission (G5-G6)
5. **Result**: Publication-ready manuscripts

**Best for**: Top-tier journal targeting, major publications

#### Pattern 4: The Methodological Expert

1. Paradigm selection emphasis (A5)
2. Specialized methodology agents (C2, C3, H1, H2)
3. Multiple design iterations
4. Detailed reproducibility focus (F3)
5. **Result**: Methodologically exemplary work

**Best for**: Methodology-focused papers, methodology workshops

---

### Integration with Your Workflow

#### With Your Literature Manager

```
Step 1: Export collection from Zotero/Mendeley
Step 2: Convert to PDF folder
Step 3: Use B5-Parallel-Document-Processor
Step 4: Re-import extracted data to your manager
```

#### With Your Data Analysis

```
Step 1: Run analysis in R/Python/SPSS
Step 2: Get code from E4-Code-Generator
Step 3: Compare your results with generated code
Step 4: Document discrepancies
```

#### With Your Writing Process

```
Step 1: Draft your own section
Step 2: Use G5 to analyze for AI patterns
Step 3: If patterns found, use G6 for humanization
Step 4: Review transformed version
Step 5: Use G2 for final prose refinement
```

#### With Your Submission Process

```
Step 1: Complete manuscript
Step 2: Use F2 (Checklist) for reporting compliance
Step 3: Use G1 (Journal Matcher) for target selection
Step 4: Use G3 (Peer Review Strategist) to prep for reviews
Step 5: Submit with AI use statement (from ethical guidelines)
```

---

## Version Compatibility

### Current Version Information

| Component | Version | Release Date |
|-----------|---------|--------------|
| **Diverga System** | 6.1.0 | 2026-01-26 |
| **Core Agents** | 37 total | 2026-01-26 |
| **Humanization Pipeline** | v1.0 (NEW) | 2026-01-26 |
| **Claude Code CLI** | 1.0+ | Required |

### Claude Code Requirements

| Feature | Claude Code Version |
|---------|-------------------|
| Basic agents | 1.0+ |
| Parallel execution | 1.0+ |
| Humanization (v6.1) | 1.0+ |
| Checkpoints | 1.0+ |

### Version Migration Guide

#### From v6.0.1 to v6.1.0

**New in v6.1.0**:
- G5-Academic-Style-Auditor (AI pattern detection)
- G6-Academic-Style-Humanizer (AI pattern transformation)
- F5-Humanization-Verifier (transformation quality assurance)
- 2 new checkpoints: CP_HUMANIZATION_REVIEW, CP_HUMANIZATION_VERIFY
- 24 AI pattern categories for detection

**No breaking changes**:
- All existing workflows continue to work
- Humanization is opt-in
- Existing agents unchanged

**To upgrade**:
```bash
# Update Claude Code
claude upgrade

# Verify Diverga update
diverga --version
# Should show v6.1.0

# No additional steps needed
```

**To enable humanization**:
- Use new commands automatically detected
- Or configure in `.research/humanization-config.yaml`

#### From v5.0 to v6.0+

**What changed**:
- Removed: OMC modes (ralph, ultrawork, autopilot, ecomode)
- Removed: Sisyphus protocol
- Added: Mandatory human checkpoints
- Added: Restructured agents (A1-H2 naming)
- Migration guide available in CHANGELOG.md

**Key difference**:
- v5.0: AI could work autonomously until completion
- v6.0+: AI stops at every checkpoint for your approval

---

## Quick Reference Card

### Checkpoint Summary

```
🔴 REQUIRED - System STOPS
   • CP_RESEARCH_DIRECTION
   • CP_PARADIGM_SELECTION
   • CP_THEORY_SELECTION
   • CP_METHODOLOGY_APPROVAL

🟠 RECOMMENDED - System PAUSES
   • CP_ANALYSIS_PLAN
   • CP_INTEGRATION_STRATEGY
   • CP_HUMANIZATION_REVIEW
   • CP_RESPONSE_APPROVAL

🟡 OPTIONAL - System ASKS
   • CP_VISUALIZATION_PREFERENCE
   • CP_HUMANIZATION_VERIFY
```

### Most-Used Agents

```
Foundation:  A1 (Question) → A2 (Theory)
Evidence:    B1 (Literature) → B5 (PDFs)
Design:      C1/C2/C3 (based on paradigm)
Analysis:    E1/E2/E3 (based on paradigm)
Quality:     F2 (Checklist) → G5 (AI Check)
Publication: G1 (Journal) → G6 (Humanize)
```

### Response Format

```
REQUIRED Checkpoint:
"Option B"

RECOMMENDED Checkpoint:
"Use default" or "Option B"

OPTIONAL Checkpoint:
"Skip" or provide input
```

### When to Use Humanization

```
✅ High probability (>50%) AI text for publication
✅ Content you're disclosing as AI-assisted
✅ Drafts needing natural academic prose

❌ Content claiming full original authorship
❌ Situations where disclosure impossible
❌ To hide AI use
```

---

## Appendix: Key Definitions

### T-Score (Typicality Score)

Measures how "typical" or "novel" an option is:

| Score | Meaning | Recommendation |
|-------|---------|-----------------|
| 0.8-1.0 | Very common | ⚠️ Consider alternatives |
| 0.5-0.8 | Established option | ✅ Safe choice |
| 0.3-0.5 | Less common | ✅ Innovative |
| 0.0-0.3 | Novel/rare | ⚠️ Needs justification |

### Paradigm

Research approach (quantitative, qualitative, or mixed methods):

- **Quantitative**: Numbers, statistics, experiments
- **Qualitative**: Words, meanings, interviews
- **Mixed Methods**: Both quantitative and qualitative

### Checkpoint

Decision point where system waits for your approval. Three types: Required (🔴), Recommended (🟠), Optional (🟡)

### Agent

Specialized AI component handling specific research tasks

### Humanization

Process of transforming AI-detected patterns to natural prose while preserving meaning, facts, and accuracy

### Effect Size

Measure of magnitude of difference or relationship (Cohen's d, correlation r, odds ratio, etc.)

---

## Summary

Diverga empowers researchers with:
- **33 specialized agents** across 8 research domains
- **Human-centered checkpoints** keeping you in control
- **Parallel processing** for efficiency
- **Ethical guidelines** for responsible use
- **Humanization tools** for natural prose

**Remember**: You're in command. AI assists.

**Get started**: Describe your research need and follow the checkpoints.

**Questions**: Reference this guide, the agent-specific documentation, or ask Diverga directly.

---

**Document Version**: 6.1.0
**Last Updated**: 2026-01-26
**For Support**: https://github.com/HosungYou/Diverga/issues
