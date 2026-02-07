# Diverga Upgrade Roadmap: v8.1.0 to v9.x

**Document Version**: 1.0.0
**Created**: 2026-02-07
**Status**: Strategic Planning

---

## Executive Summary

This roadmap outlines the evolution of Diverga from v8.0.1 (current) through v9.x, organized into four priority tiers. Each tier builds on the previous, with P0 addressing foundation issues and P3 targeting ambitious collaboration features.

---

## Current State Assessment (v8.0.1-patch4)

### What Works Well
- 44 specialized agents across 9 categories (A-I)
- VS methodology prevents mode collapse with T-Score alternatives
- Human checkpoint system (REQUIRED/RECOMMENDED/OPTIONAL)
- Category I systematic review automation (I0-I3) with real API calls
- Memory system with 3-layer context and cross-session persistence
- Multi-paradigm support (quantitative, qualitative, mixed methods)

### Architecture Issues to Address

| Issue | Impact | Effort |
|-------|--------|--------|
| lib/ vs src/ dual TypeScript registries | Confusion, maintenance burden | Medium |
| 6 state management systems | No unified state interface | High |
| lib/ is effectively legacy code | Dead code, not compiled | Low (remove/archive) |

### Paper Retrieval Status (I1)

I1 makes real API calls — papers are genuinely fetched, not simulated.

| Database | API Type | Status | PDF Coverage |
|----------|----------|--------|--------------|
| Semantic Scholar | REST API | Working | ~40% |
| OpenAlex | REST API | Working | ~50% |
| arXiv | OAI-PMH | Working | 100% |
| Scopus | REST API | Placeholder only | Requires SCOPUS_API_KEY |
| Web of Science | REST API | Placeholder only | Requires WOS_API_KEY |
| KCI/RISS (Korean) | Web-based | Docs only | No API |

---

## P0: Foundation (v8.1.0) — Fix What's Broken

**Goal**: Stabilize the platform and clean up technical debt.

| # | Feature | Description | Effort |
|---|---------|-------------|--------|
| 1 | English-first UI | All UI text defaults to English. Done in v8.0.1-patch4. | Done |
| 2 | Unified state interface | Single API for reading/writing .research/, config, checkpoint, and decision state. Eliminates 6 competing state systems. | High |
| 3 | lib/ cleanup | Archive or remove the unused lib/ TypeScript registry. One source of truth (src/ + skills/). | Low |

### Unified State Interface Design

Currently, state is scattered across:
1. `.research/` YAML files (project state, decisions)
2. `lib/memory/` SQLite + Python (memory system)
3. `lib/hud/` (HUD state)
4. `.omc/` JSON files (OMC integration)
5. `config/` JSON files (configuration)
6. `checkpoints.yaml` (checkpoint states)

**Proposed**: Single `DivergaState` interface that reads/writes all systems through one API.

---

## P1: Research Pipeline Enhancement (v8.2.0)

**Goal**: Make the systematic review pipeline production-ready for publication-quality research.

| # | Feature | Description | Effort |
|---|---------|-------------|--------|
| 4 | Enhanced database selection | Equal-weight presentation of open-access, institutional, and combined approaches at SCH_DATABASE_SELECTION checkpoint | Medium |
| 5 | Browser-assisted institutional DB access | When researcher selects institutional databases, generate optimized queries per database, guide browser automation for search + export | Medium |
| 5.5 | LLM provider selection at screening | Present all configured LLM providers with cost estimates at SCH_SCREENING_CRITERIA checkpoint. Add OpenAI (gpt-4o-mini) as 4th provider. | Medium |
| 6 | Persistent screening state | Save screening progress to .research/screening-state.yaml. Resume across sessions. | Medium |
| 7 | Auto-populated PRISMA diagrams | Connect paper_lineage.py stage tracking to Mermaid template generation | Low |
| 8 | Zotero MCP conditional integration | Detect Zotero MCP -> offer sync at retrieval, screening, and export stages. Never mentioned if not configured. | Medium |
| 9 | Timeline/milestone tracking | Research project deadlines, Gantt charts in HUD | Medium |

### Enhanced Database Selection (Feature #4)

The SCH_DATABASE_SELECTION checkpoint should present equal-weight choices:

```
Paper Source Selection (SCH_DATABASE_SELECTION)

For your systematic review on "{topic}", select your paper sources:

[A] Open-Access Databases (automated via API)
    Semantic Scholar, OpenAlex, arXiv
    -> Fully automated retrieval, deduplication, and screening
    -> Best for: preprints, CS/AI/STEM, broad coverage

[B] Institutional Databases (guided via Claude Code Browser)
    Web of Science, Scopus, ERIC, PubMed, ProQuest
    -> Semi-automated: Diverga builds your queries, you export from your institution
    -> Best for: peer-reviewed journals, discipline-specific, comprehensive SLR

[C] Both - Comprehensive (recommended for publication-quality SLR)
    -> Phase 1: Institutional database export (guided)
    -> Phase 2: Open-access API supplement (automated)
    -> Phase 3: Cross-database deduplication
    -> Best for: meta-analysis, systematic reviews targeting journals

[D] Korean Academic Databases (KCI/RISS)
    -> Guided via Claude Code Browser
    -> Best for: Korean-language research, KCI-indexed journals
```

Key principle: Semantic Scholar is NOT called automatically just because it's configured. The researcher always chooses.

### Browser Automation for Institutional Databases (Feature #5)

When the researcher selects [B] or [C]:

1. I0 generates optimized Boolean queries for each database
   - Adapts syntax per database (WoS vs Scopus vs ERIC have different operators)
2. User opens institutional database in Chrome
   - Claude Code Browser navigates to the search interface
3. Diverga inputs the query via browser automation
   - Handles advanced search fields, date ranges, document types
4. User verifies results and clicks export
   - Claude Code Browser assists with export settings (RIS/BibTeX/CSV)
5. Exported files are imported into the pipeline
   - Automatic parsing, deduplication, and integration with I2 screening

### LLM Provider Selection (Feature #5.5)

At SCH_SCREENING_CRITERIA checkpoint, present all configured providers:

```
Select screening LLM provider:
[A] Groq (llama-3.3-70b)   - $0.01/100 papers, fast    [GROQ_API_KEY: set]
[B] OpenAI (gpt-4o-mini)   - $0.02/100 papers, good    [OPENAI_API_KEY: set]
[C] Anthropic (haiku-4-5)  - $0.15/100 papers, best    [ANTHROPIC_API_KEY: not set]
[D] Ollama (local)         - Free, private              [not detected]

For 743 papers: [A] ~$0.07  [B] ~$0.15  [C] ~$1.11  [D] Free
```

### Zotero MCP Integration (Feature #8)

If Zotero MCP is configured, Diverga can leverage it at these stages:

| Stage | Without Zotero | With Zotero MCP |
|-------|---------------|-----------------|
| After I1 retrieval | Papers stored as JSON | Papers auto-imported with tags |
| During I2 screening | Include/exclude in YAML | Zotero collections auto-updated |
| Deduplication | Python script dedup | Cross-reference with existing Zotero library |
| After screening | BibTeX export | Formatted bibliography in any citation style |
| Writing (G2/G3) | Manual citation | "Cite Smith 2024" -> formatted citation |

When Zotero is NOT configured: Diverga works fine with its built-in BibTeX/JSON pipeline. Zotero adds convenience, not dependency.

### MCP Integration Strategy

MCPs are external tools, not bundled inside Diverga. Approach: detect -> offer -> route (never force).

| MCP | Bundled? | How Diverga Uses It |
|-----|----------|---------------------|
| Zotero MCP | No (external) | Detects if configured, routes reference operations |
| Claude Code Browser | No (external) | Detects if available, offers institutional DB automation |

---

## P2: Intelligence Enhancement (v9.0.0)

**Goal**: Leverage Opus 4.6 capabilities for deeper research intelligence.

| # | Feature | Description | Why Opus 4.6 |
|---|---------|-------------|--------------|
| 10 | Extended thinking for C5 meta-analysis | Multi-step reasoning for complex gate decisions visible to researcher | Extended thinking enables transparent chain-of-thought for statistical decisions |
| 11 | Multi-step tool chains | Single agent turn: read 5 PDFs -> extract effect sizes -> calculate Hedges' g -> write to codebook -> flag anomalies | Improved tool chaining reduces pipeline latency |
| 12 | Agentic coding for E4 | E4 generates R/Python analysis code AND executes it, returning results + visualizations | Code generation + execution capabilities |
| 13 | Enhanced A3 Devil's Advocate | Deeper counterargument generation with extended thinking and severity-ranked rebuttals | Reasoning depth for nuanced critique |

### Opus 4.6 Specific Opportunities

| Capability | Diverga Application | Example |
|------------|---------------------|---------|
| Extended thinking | C5 meta-analysis gate decisions, A2 framework synthesis | "Given I-squared=78% and Q(df=22)=98.4, should we proceed with subgroup analysis or investigate moderators first?" |
| Improved tool use | Multi-step research pipelines in single agent turns | I1: fetch -> parse -> deduplicate -> store in one turn |
| 200K context | B5 parallel document processor | Process 15 full-text PDFs simultaneously instead of 3-5 |
| Better code generation | E4 analysis code | "Run meta-regression with publication year as moderator" -> R code + forest plot + interpretation |
| Enhanced reasoning | A3 Devil's Advocate | Simulate Reviewer 2 with specific methodological expertise |

---

## P3: Collaboration & Scale (v9.1.0)

**Goal**: Enable multi-researcher workflows and advanced discovery features.

| # | Feature | Description | Effort |
|---|---------|-------------|--------|
| 14 | Multi-researcher support | Shared .research/ state with CRDTs. Co-PI can review screening decisions. | High |
| 15 | Active learning screening (ASReview-inspired) | After human-screening 50 papers, I2 learns inclusion patterns and prioritizes remaining papers. Reduces effort by 50-80%. | High |
| 16 | Citation network analysis (Research Rabbit-inspired) | Given 20 included papers, discover related papers through citation analysis. | Medium |
| 17 | Smart citation context (Scite-inspired) | Show whether included studies have been supported or contrasted by subsequent research. | Medium |
| 18 | ORCID integration | Link researcher identity across projects. Auto-populate author info. | Low |

---

## Competitive Analysis

| Service | Key Feature | How Diverga Adapts | Priority |
|---------|------------|-------------------|----------|
| Elicit | Automated extraction tables | Enhance C6 with structured extraction templates per study design | P1 |
| Consensus | NL answers from papers | I3 RAGBuilder already builds vector DB. Add NL Q&A interface. | P1 |
| Research Rabbit | Citation network visualization | Add forward/backward citation crawling to I1 | P2 |
| Connected Papers | Graph-based discovery | Combine with Semantic Scholar citation API for graph traversal | P2 |
| Scite | Smart citation context | Use OpenAlex citation context to classify supporting/contrasting | P2 |
| ASReview | Active learning screening | Train lightweight classifier on initial screening decisions | P3 |
| Rayyan | Collaborative screening | Multi-user screening with conflict resolution | P3 |
| Covidence | Full SLR platform | Diverga already covers most of this. Focus on UX polish. | Reference |

**Diverga's unique advantage**: Integration. Each competitor solves ONE piece. Diverga orchestrates the entire pipeline in a single environment with persistent context.

---

## Researcher Experience: End-to-End Scenario

**Dr. Kim, Education Researcher conducting a systematic review on AI in K-12:**

| Step | Action | What Happens | Status |
|------|--------|--------------|--------|
| 1 | "Start a systematic review" | I0 orchestrator activates | Working |
| 2 | "Search for papers on AI in K-12" | SCH_DATABASE_SELECTION presents A/B/C/D | Checkpoint exists |
| 3a | Selects [A] Open-Access | I1 queries Semantic Scholar + OpenAlex + arXiv | Working |
| 3b | Selects [B] Institutional | Browser automation guides WoS/Scopus search | Gap (P1 #5) |
| 3c | Selects [C] Both | Combined phased workflow | Gap (P1 #4) |
| 4 | "Screen these 500 papers" | I2 screens via Groq, 6-dimension scoring | Working |
| 5 | "Resume tomorrow" | Screening state preserved | Gap (P1 #6) |
| 6 | "Show PRISMA diagram" | Mermaid template with auto-populated numbers | Partial (P1 #7) |
| 7 | "Export to Zotero" | Zotero MCP sync | Gap (P1 #8) |
| 8 | "What's my progress?" | HUD shows status | Partial (P1 #9) |
| 9 | "Co-PI wants to review" | Shared state | Gap (P3 #14) |

---

## Version Timeline

| Version | Focus | Key Deliverables |
|---------|-------|-----------------|
| v8.0.1-patch4 | English-first UI + branding cleanup | Done (2026-02-07) |
| v8.1.0 | Foundation fixes | Unified state, lib/ cleanup |
| v8.2.0 | Pipeline enhancement | Database selection, browser automation, screening persistence, Zotero |
| v9.0.0 | Intelligence enhancement | Opus 4.6 features, extended thinking, agentic coding |
| v9.1.0 | Collaboration & scale | Multi-researcher, active learning, citation networks |

---

## Implementation Notes

### MCP Detection Pattern

```
IF Zotero MCP available:
  "Would you like to sync retrieved papers with your Zotero library?"
ELSE:
  [skip - use built-in BibTeX pipeline, no mention of Zotero]
```

### State File Locations

| System | Current Location | Proposed (v8.1.0) |
|--------|-----------------|-------------------|
| Project state | .research/project-state.yaml | .research/project-state.yaml |
| Decisions | .research/decision-log.yaml | .research/decision-log.yaml |
| Checkpoints | .research/checkpoints.yaml | Unified state API |
| Config | config/diverga-config.json | Unified state API |
| Memory | lib/memory/ SQLite | Unified state API |
| HUD | lib/hud/ | Unified state API |

### Breaking Changes (v9.0.0)

1. Agent ID format may change to descriptive names
2. Checkpoint system may add AUTO level
3. Memory file format may migrate from YAML to SQLite
