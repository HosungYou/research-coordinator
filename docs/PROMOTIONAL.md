# Diverga: AI Research Assistant Built for Social Scientists

## Executive Summary

If you've ever felt that AI recommendations for your research all start looking the same—surveys instead of experiments, TAM instead of grounded theory, t-tests instead of phenomenology—you're experiencing **mode collapse**. This is a real problem in AI systems. They optimize for the most common pattern, not the best pattern for *your* research.

Diverga solves this with a fundamentally different approach: **VS-Research Methodology**. Instead of pushing you toward predictable solutions, it systematically identifies what *most* AI systems would recommend (and what most researchers do), then presents you with thoughtfully differentiated alternatives—each with a Typicality Score showing how novel and risky each approach is. You stay in control. You make the decisions. AI works between your checkpoints, not around them.

This is built for social science researchers who want AI as a thinking partner, not a box-checker. We support quantitative research, qualitative inquiry, mixed methods, meta-analysis, and specialized approaches like ethnography and action research—with 40 specialized agents who understand your paradigm.

---

## The Problem We Solve: Mode Collapse in Academic Research

### What Is Mode Collapse?

In machine learning, mode collapse occurs when a generative model fails to capture the full diversity of the training data and instead produces homogenized, repetitive outputs. The same thing happens with AI research assistants.

**The Problem in Practice:**
```
User: "Help me design a study on AI in education"
AI Response: "Use a quantitative survey design with TAM framework and ANOVA analysis"

User (different): "I want to study how teachers experience AI in their classrooms"
AI Response: "Use a quantitative survey design with TAM framework"

User (another): "Meta-analysis on AI and learning outcomes"
AI Response: "Use a quantitative meta-analysis with TAM framework"
```

All three researchers get pushed toward the same general approach. The AI system has learned that this combination works and gets positive feedback—so it recommends it to everyone.

### Why This Matters for Your Research

Mode collapse in research methodology has real consequences:

1. **Homogenization of Research Landscape**: The published literature increasingly looks the same. Survey → TAM → ANOVA becomes the default path.

2. **Loss of Methodological Novelty**: Peer reviewers see the exact same study design repeatedly. Your contribution becomes harder to articulate.

3. **Suboptimal Research Questions**: You might have a qualitative research question, but an AI trained on published patterns steers you toward quantification because that's what the literature rewards.

4. **Eroded Researcher Agency**: You feel like you're choosing from a limited menu rather than designing research that genuinely fits your problem.

---

## Our Solution: VS-Research Methodology

Diverga's core innovation is the **Verbalized Sampling (VS) Research Framework**—a systematic approach to preventing mode collapse and generating methodologically diverse research designs.

### How It Works: The 3-Stage Process

**Stage 1: Modal Identification**
First, Diverga explicitly identifies what the "obvious" recommendation would be. This brings the bias out into the open:

```
⚠️ MODAL WARNING: These are the most predictable approaches for your topic:

| Approach | Typicality Score | Problem |
|----------|------------------|---------|
| Quantitative survey + TAM | T = 0.95 | Overdone in literature |
| Social Cognitive Theory | T = 0.92 | 60% of similar studies use this |
| ANOVA analysis | T = 0.88 | Reviewer will see this coming |
```

This is the baseline. We're not recommending it. We're naming it so we can move beyond it.

**Stage 2: Divergent Exploration**
Diverga then generates 5-7 research directions at different levels of typicality:

```
Direction A (T ≈ 0.70): Safe Differentiation
├─ Approach: Quantitative, but with specific moderators & newer framework
├─ Advantage: Easier to defend, grounded in existing literature
└─ Suitable for: First publications, conservative journals

Direction B (T ≈ 0.45): Balanced Innovation  ⭐ RECOMMENDED
├─ Approach: Mixed methods combining survey + qualitative interviews
├─ Advantage: Clear methodological contribution, answers new questions
└─ Suitable for: Mid-career researchers, innovative journals

Direction C (T ≈ 0.25): High Innovation
├─ Approach: Ethnographic study of AI adoption in workplace contexts
├─ Advantage: Maximum contribution potential, paradigm-shifting insights
└─ Suitable for: Top-tier journals, established researchers
```

**Stage 3: Human Selection** (🔴 MANDATORY CHECKPOINT)
This is where you decide. Diverga stops and waits for your explicit approval:

```
Which direction appeals to your research goals?
[A] Safe Differentiation - I want to publish first
[B] Balanced Innovation - I want contribution and feasibility
[C] High Innovation - I'm going for impact
[D] Tell me more about the trade-offs
[E] Let me explore this differently
```

You choose. Not the algorithm.

### T-Score System: Quantifying Typicality

Every recommendation comes with a **Typicality Score (T-Score)** from 0 to 1:

| T-Score | Label | Meaning |
|---------|-------|---------|
| ≥ 0.7 | **Modal** | Highly typical; 80%+ of similar studies use this; limited novelty |
| 0.4-0.7 | **Established** | Common but differentiated; balanced risk-novelty |
| 0.2-0.4 | **Emerging** | Novel and defensible; recommended for differentiation |
| < 0.2 | **Experimental** | High novelty; high risk/reward; for experienced researchers |

T-Scores are **not** judgment calls. They're based on:
- Real publication data (via Semantic Scholar and OpenAlex APIs)
- 3-year recency weighting (trends matter)
- Domain-specific adjustments (what's modal in education vs. psychology)
- Trend detection (is this approach rising or falling in popularity)

### Before/After Example: AI in Education

**Before (Mode Collapse):**
```
User: "Study on AI tutoring systems and student learning"

AI: "Use quantitative methodology. Survey students pre/post intervention.
Measure learning outcomes with standardized test. TAM framework.
ANOVA to test group differences."

Reviewer: "This is the 47th TAM study on educational technology
in my review queue this month. No methodological contribution."
```

**After (VS-Research with Diverga):**
```
User: "Study on AI tutoring systems and student learning"

Diverga: "Let me show you what we'd typically recommend, then alternatives:

⚠️ MODAL: Quantitative survey + TAM + ANOVA (T=0.92)
  Problem: 60% of EdTech studies use this

Direction A (T=0.68): Add moderators - test TAM differently
  Your original approach, but with self-efficacy as moderator

Direction B (T=0.42): Mixed methods investigation
  Quant: Compare AI vs. human tutoring on learning gains
  Qual: Interview students about persistence barriers
  Contribution: Why students continue/abandon, not just gains

Direction C (T=0.18): Phenomenological study
  Interview college students: 'What is the experience of learning
  from AI tutors?' How do emotions, expectations shape that?
  Contribution: Reframes AI tutoring as social-psychological phenomenon

Which direction fits your research goals?"

User: "B - the mixed methods approach"

Diverga: "Smart choice. Here's why that works for you:
✓ Methodologically novel
✓ Defensible in peer review
✓ Feasible with your timeline
✓ Distinct from the modal literature
[Proceeds to methodology design]"
```

The difference is visible to reviewers. Your contribution is clear.

---

## Key Features

### 1. 40 Specialized Research Agents

Diverga isn't a single chatbot. It's an orchestrated team of 40 specialized agents organized in 7 categories:

**Category A: Research Foundation (5 Agents)**
- Research Question Refiner (eliminates vague questions)
- Theoretical Framework Architect (selects frameworks with VS methodology)
- Devil's Advocate (anticipates reviewer objections)
- Research Ethics Advisor (IRB protocols, consent forms)
- Paradigm Advisor (epistemology, ontology, worldview)

**Category B: Literature & Evidence (4 Agents)**
- Systematic Literature Scout (PRISMA-compliant searching)
- Evidence Quality Appraiser (RoB 2, CASP, JBI, GRADE tools)
- Effect Size Extractor (calculate, convert, compare)
- Research Radar (tracks emerging publications)

**Category C: Study Design (4 Agents)**
- Quantitative Design Consultant (experimental, quasi-experimental)
- Qualitative Design Consultant (phenomenology, grounded theory, case study)
- Mixed Methods Design Consultant (convergent, sequential, explanatory)
- Experimental Materials Developer (stimuli, instruments, protocols)

**Category D: Data Collection (4 Agents)**
- Sampling Strategy Advisor (probability, purposeful, stratified sampling)
- Interview & Focus Group Specialist (protocol development)
- Observation Protocol Designer (structured observation guides)
- Measurement Instrument Developer (scale development, validation)

**Category E: Analysis (4 Agents)**
- Quantitative Analysis Guide (method selection, assumptions)
- Qualitative Coding Specialist (thematic analysis, grounded theory coding)
- Mixed Methods Integration Specialist (joint displays, meta-inference)
- Analysis Code Generator (R, Python, SPSS, Stata)

**Category F: Quality & Validation (4 Agents)**
- Internal Consistency Checker (logic flow verification)
- Checklist Manager (CONSORT, STROBE, PRISMA, SRQR, COREQ)
- Reproducibility Auditor (OSF, open science practices)
- Bias & Trustworthiness Detector (validity threats, qualitative trustworthiness)

**Category G: Publication & Communication (4 Agents)**
- Journal Matcher (find target journals by scope/metrics)
- Academic Communicator (write plain-language summaries)
- Peer Review Strategist (response letters to reviewer comments)
- Pre-registration Composer (OSF and AsPredicted templates)

**Category H: Specialized Approaches (2 Agents)**
- Ethnographic Research Advisor (ethnographic methodology)
- Action Research Facilitator (participatory action research)

Each agent:
- Understands your specific research paradigm
- Is versioned and documented
- Works across the full research lifecycle
- Can operate independently or as part of a coordinated workflow

### 2. Human Checkpoint System: Humans Make Decisions, AI Does the Work

Diverga's checkpoint system enforces a clear boundary: **humans decide, AI executes.**

**Required Checkpoints** (🔴 System Stops - Cannot Proceed):
- Research Direction Selection (point your research toward your chosen path)
- Paradigm Confirmation (quantitative/qualitative/mixed)
- Theory Selection (your theoretical framework, with VS alternatives)
- Methodology Approval (study design is locked in)

**Recommended Checkpoints** (🟠 System Pauses - Suggests Approval):
- Analysis Plan (before statistical/qualitative analysis)
- Integration Strategy (mixed methods only)
- Quality Review (assessment results)

**Optional Checkpoints** (🟡 System Asks - Defaults Available):
- Visualization Preference (how to display results)
- Writing Style (formal academic vs. accessible tone)

Example checkpoint interaction:
```
Diverga: "Research direction finalized. Your study design is:
• Mixed methods (qual-dominant)
• Grounded theory approach for interview data
• Case study for context (3 institutions)
• Statistical comparison for quantitative strand

Should we proceed with this design?

[Y] Yes, lock in this design
[N] Go back and revise
[?] Show me the alternatives again"

You choose. You're in control.
```

### 3. Bilingual Support: English Base + Full Korean Recognition

Research is global. So is Diverga.

- **English**: Full support, all features
- **Korean (한국어)**: Full input recognition and response
  - Korean research question detection
  - Korean paradigm terminology (양적/질적/혼합)
  - Korean journal matching
  - Korean style conventions in writing agents
  - Seamless code-switching support

You can work entirely in Korean or English, or mix them. Diverga understands.

### 4. HAVS: Academic Humanization for AI-Generated Writing

When you use Diverga's writing agents, you get AI-assisted drafts. But those drafts can sometimes sound like AI. That's a problem for journals.

**HAVS** (Humanization-Aware Verbalizing System) addresses this with two integrated agents:

**G5-Academic Style Auditor**
- Detects 24+ AI writing patterns (adapted from Wikipedia's AI Cleanup guidelines)
- Analyzes vocabulary clustering ("landscape," "multifaceted," "paradigm shift")
- Flags communication patterns (chatbot artifacts, excessive hedging)
- Estimates AI probability score
- Recommends humanization strategy

Example detection:
```
Your abstract:
"This pivotal study delves into the multifaceted landscape of AI-assisted
learning, underscore the potential for transformative educational outcomes..."

AI Pattern Detection Report:
- High-Risk: Significance Inflation ("pivotal"), AI Vocabulary ("landscape", "multifaceted")
- Medium-Risk: Copula Avoidance ("underscore the potential" → "shows the potential")
- Estimated AI Probability: 62% (Medium-High)

Recommendation: Use Balanced humanization mode
```

**G6-Academic Style Humanizer**
- Conservative Mode: Fixes high-risk patterns only
- Balanced Mode: High + medium patterns (recommended)
- Aggressive Mode: Maximum transformation while preserving meaning

Transformed version:
```
"This study examines the interconnected dimensions of AI-assisted learning,
highlighting how it could improve educational outcomes. We focus on how
students engage with AI tutors in online environments..."
```

### 5. Context-Persistent Project State

Your research context is preserved across every conversation:

```yaml
.research/project-state.yaml

project:
  name: "AI Tutoring in Higher Education"
  type: "mixed_methods"
  paradigm: "pragmatist"
  current_stage: 3

research_context:
  research_question:
    main: "How do students experience AI tutors and what persistence patterns emerge?"
  theoretical_framework: "Self-Determination Theory + Situated Learning"

checkpoints:
  - CP_RESEARCH_DIRECTION: "approved (Direction B)"
  - CP_PARADIGM: "approved (mixed methods)"
  - CP_THEORY: "approved (SDT+Situated)"
  - CP_METHODOLOGY: "pending"
```

Every agent can access this context. You don't repeat yourself. Your decisions carry through the entire research lifecycle.

### 6. Pipeline Templates

Pre-designed workflows for common research types:

**Quantitative Pipeline (PRISMA 2020)**
Protocol → Search → Screen → Extract → Quality Assessment → Analysis → Write → Publish

**Qualitative Pipeline**
Design → Sampling → Data Collection → Coding → Theme Development → Quality Check → Write → Member Check

**Meta-Analysis Pipeline**
Protocol → Search → Screen → Extract → Quality Assessment → Analyze Heterogeneity → Generate PRISMA Diagram

**Mixed Methods Pipeline**
Parallel/Sequential Design → Concurrent Collection → Separate Analysis → Integration → Joint Display → Write

Each pipeline includes checkpoints at critical decision points.

---

## Who Benefits

### Graduate Students

You're facing your first major research project. You have good ideas but uncertainty about methodology.

**What Diverga Provides:**
- Systematic research question refinement (moves beyond "effect of X on Y")
- Defensible methodology design with peer-review justification
- Full documentation and checklist support
- Pre-registration support (OSF templates)

**Result**: You publish faster with more methodological confidence.

### Early-Career Researchers

You've published but want to scale impact. You're looking for methodological contributions, not just more quantitative surveys.

**What Diverga Provides:**
- Explicit mode-collapse detection (know what you're *not* doing)
- Cross-paradigm design consultation
- Competing design comparisons
- Literature context through Research Radar

**Result**: Your contributions stand out. Reviewers notice the methodological novelty.

### Senior Researchers

You're mentoring others. You might lead meta-analyses or complex systematic reviews. You want consistency across team members' work.

**What Diverga Provides:**
- Standardized protocols (PRISMA, SRQR, COREQ compliance)
- Quality appraisal tooling (RoB 2, CASP, JBI, GRADE)
- Bias detection and trustworthiness assessment
- Reproducibility auditing

**Result**: Your team's work is higher quality, more auditable, more publishable.

### Non-Native English Speakers

You have strong research ideas but worry about:
- Academic writing quality
- Whether your design will sound professional
- Meeting journal language standards

**What Diverga Provides:**
- Bilingual support (English/Korean recognized in all agents)
- Academic style humanization (detects awkward phrasing)
- Response letter support (replies to reviewer comments)
- Plain-language summary generation

**Result**: Your strong research gets published without language becoming the barrier.

---

## Ethical Commitment

### Transparency About AI Use

We're honest about what Diverga is and isn't:

**What Diverga IS:**
- A thinking partner for research design
- A quality assurance tool
- A protocol generator
- A writing assistant for initial drafts

**What Diverga IS NOT:**
- An autonomous researcher (you make the decisions)
- A data analyzer (you run the analyses)
- A replacement for peer review
- A journal submission automation tool

We design checkpoints *into* the system to prevent misuse. You can't accidentally use Diverga to bypass good research practices.

### Human-Centered Design Philosophy

Every feature is designed with this principle: "Human decisions remain with humans. AI handles what's beyond human scope."

This means:
- Humans approve every major decision (research direction, design, analysis plan)
- Humans interpret results
- Humans write the narrative
- AI prepares, organizes, suggests, checks—but doesn't decide

### Academic Integrity Stance

Diverga explicitly supports:
- **Pre-registration**: Full OSF and AsPredicted support
- **Open Science**: Reproducibility auditing, OSF integration
- **Bias Detection**: Built-in bias and trustworthiness checking
- **AI Disclosure**: HAVS detects and discloses AI-assisted writing patterns

We believe AI should make research *better*, not easier to cut corners.

---

## Getting Started: Three Steps

### Step 1: Initial Setup (5 minutes)

Tell Diverga about your research:

```
"I'm interested in how AI chatbots affect language learning.
I'm in education. I have 6 months and access to language students."
```

Diverga detects your paradigm and asks:

```
From your description, this sounds like quantitative research.
Is that correct?

[Y] Yes, quantitative
[Q] No, I want qualitative
[M] Mixed methods
[?] Not sure, help me decide
```

### Step 2: Design Your Research

Diverga walks you through VS-Research:

```
⚠️ MODAL APPROACHES (what we'll skip):
- Quantitative survey + TAM framework + t-test

ALTERNATIVE DIRECTIONS:

Direction A (T=0.68): Add specificity
- Survey with attention to individual differences
- See who AI chatbots help most/least

Direction B (T=0.42): Mixed methods ⭐
- Pre/post achievement test for quantitative strand
- Interviews with 15 students about experience
- Integration: When does achievement ↑ despite negative experience?

Direction C (T=0.18): Phenomenology
- Deep qualitative study: "What is it like to learn from AI?"
- How do emotions, expectations, self-efficacy shape experience?

Which appeals to you?
```

You select. Diverga designs the full methodology.

### Step 3: Execute & Validate

Diverga provides:
- Full protocol documentation
- Checklist templates (CONSORT, STROBE, etc.)
- Quality appraisal tools
- Draft writing support with humanization

---

## Testimonials (Placeholder for Future Use)

### Coming Soon

We're currently gathering feedback from early-stage researchers. Here's what we're hearing:

**Format for future testimonials:**
```
[Name, Title, Institution]

"[Quote about specific feature or outcome]"

— Relevant context (e.g., "Used Diverga for meta-analysis on X topic")
```

Interested in contributing your story? Email us at [contact].

---

## Frequently Asked Questions

### Q: Will Diverga replace my advisor?

**A**: No. Diverga is designed to *support* advising, not replace it. You still need someone who knows your field deeply. What Diverga does:
- Ensures you've considered alternatives
- Documents your design decisions
- Catches quality and bias issues
- Generates first drafts

Your advisor can spend more time on research thinking and less on protocol boilerplate.

### Q: What if I don't have funding for APIs?

**A**: Diverga has a **Hybrid Mode** that combines:
- Fast static lookup tables (no API call needed)
- Trend adjustments from cached data
- Instant response, lower cost

You'll get 95% of the benefit without real-time API calls.

### Q: Can I use this for dissertation research?

**A**: Yes. Many graduate programs explicitly allow AI tools for research design and writing assistance. We recommend:
1. Check your university's AI policy
2. Document what Diverga did (for transparency)
3. Clearly identify AI-assisted sections in your methodology
4. Use HAVS to humanize AI-generated text before submission

### Q: What about my research data privacy?

**A**: Your project state file (`.research/project-state.yaml`) is **local only**. It never goes to cloud servers. Checkpoints and decisions are stored locally. You control your data.

### Q: Can I export my research protocol?

**A**: Yes. Diverga generates:
- Full PRISMA/STROBE protocol documents
- OSF pre-registration files
- Methodology sections (ready for your manuscript)
- CONSORT/SRQR/COREQ checklists (filled out)

Everything exports as markdown, Word, or PDF.

---

## Why Diverga Is Different

### Comparison: Standard AI vs. Diverga

| Feature | Standard ChatGPT | Specialized AI Tools | Diverga |
|---------|------------------|---------------------|---------|
| **Modal Avoidance** | No—recommends common approach | No—optimized for popularity | Yes—explicitly identifies modal, presents alternatives |
| **Human Checkpoints** | No autonomy enforcement | Minimal | Mandatory at every critical decision |
| **Paradigm Support** | Generic | Quantitative-focused | Quant/Qual/Mixed equally supported |
| **Protocol Templates** | General writing | Some templates | PRISMA/STROBE/SRQR/COREQ built-in |
| **T-Score System** | No typicality awareness | No | Real-time typicality scoring |
| **AI Writing Detection** | No | No | HAVS detects 24 AI patterns |
| **Bilingual Support** | English-dominant | English only | English/Korean full support |
| **Multi-Agent System** | Single model | 3-5 agents | 40 specialized agents |
| **Researcher Agency** | Passive (takes suggestions) | Limited | Active (you decide at checkpoints) |

---

## The Research Ethics Advantage

Diverga is built on research ethics from the ground up:

1. **Transparency**: Every recommendation includes T-Score (how typical it is)
2. **Human Agency**: Checkpoints ensure you decide, not the algorithm
3. **Quality Standards**: Built-in quality checking prevents bad practices
4. **Reproducibility**: OSF integration, open science support
5. **Bias Awareness**: Explicit bias detection in qualitative trustworthiness

This isn't an add-on. It's core architecture.

---

## Contact & Support

### Getting Help

- **Quick Start Guide**: [docs/GETTING_STARTED.md]
- **FAQ & Troubleshooting**: [docs/FAQ.md]
- **Agent Reference**: [docs/AGENTS.md]
- **Checkpoint System**: [docs/CHECKPOINTS.md]

### Feedback & Suggestions

We're actively improving Diverga based on researcher feedback.

- Report issues: [GitHub Issues]
- Feature requests: [GitHub Discussions]
- Email: hello@diverga.ai

### Open Source

Diverga is built on open science principles. It's open source, auditable, and community-driven.

- GitHub: [github.com/diverga-research/diverga]
- License: MIT (free for academic use)
- Contributing: [CONTRIBUTING.md]

---

## Final Word

Research is one of humanity's highest-calling activities. It requires rigor, creativity, integrity, and courage—all things AI should *enhance*, never replace.

Diverga is built on the belief that **better research comes from better thinking**, not from automating away the thinking. We give you tools to:
- Think more systematically about design choices
- Question the default path
- Explore real alternatives
- Make decisions with full information
- Check quality at every stage

The goal isn't to make research faster. The goal is to make research *better*.

We hope you'll join us.

---

## Appendix: Technical Specifications

### Platform Requirements

- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge) or Claude.ai integration
- **Internet**: Required for API mode (optional—Hybrid mode works offline)
- **File Storage**: Local (no cloud upload required)
- **API Keys** (Optional): Semantic Scholar (free), OpenAlex (free)

### Supported Research Types

- ✅ Quantitative experimental research
- ✅ Quantitative quasi-experimental research
- ✅ Qualitative phenomenology
- ✅ Qualitative grounded theory
- ✅ Qualitative case study
- ✅ Qualitative ethnography
- ✅ Qualitative action research
- ✅ Mixed methods (convergent, sequential, explanatory)
- ✅ Meta-analysis (traditional and MASEM)
- ✅ Systematic reviews (PRISMA)
- ✅ Scoping reviews

### Supported Fields

Education | Psychology | Business | Healthcare | Sociology | Communications | Economics | Human Development | Organizational Development | Nursing

(Extensible to other social sciences)

### Paradigm Support

- **Positivist**: Quantitative experimental designs
- **Post-Positivist**: Quantitative quasi-experimental and survey designs
- **Interpretivist**: Qualitative phenomenology, grounded theory, ethnography
- **Pragmatist**: Mixed methods designs
- **Participatory**: Action research, community-based participatory research

---

**Version**: 1.0.0 | **Last Updated**: January 2026

For the latest version, visit [diverga.ai/docs]
