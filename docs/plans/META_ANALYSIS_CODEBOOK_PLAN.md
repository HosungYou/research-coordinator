# Universal Meta-Analysis Codebook: AI-Human Collaboration Plan

## Executive Summary

Design a **simplified, universal codebook** for meta-analysis that enables:
1. **AI extraction** from PDFs (OCR/RAG) with confidence tracking
2. **Human verification** of AI-extracted values
3. **100% accuracy** through iterative AI-Human collaboration
4. **Integration** with Diverga C5/C6/C7 agents and ScholaRAG

---

## Problem Statement

### Current Issues (V8_VERIFICATION.xlsx)
- **48 columns** - too complex for practical human review
- **No clear AI vs Human separation** - unclear who extracted what
- **No confidence tracking** - can't prioritize human review
- **No iteration support** - no workflow for AI re-extraction

### Goal
Create a **minimal, universal codebook** that:
- Works for ANY meta-analysis (not just GenAI-HE)
- Clearly separates AI extraction from human verification
- Prioritizes human effort on uncertain values
- Achieves 100% verified data through iteration

---

## Proposed Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL META-ANALYSIS CODEBOOK                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LAYER 1: CORE DATA (12 fields)                                     │
│  ─────────────────────────────────────────────────────────────────  │
│  Required for ANY meta-analysis calculation                         │
│                                                                     │
│  LAYER 2: AI EXTRACTION (8 fields per value)                        │
│  ─────────────────────────────────────────────────────────────────  │
│  Tracks AI extraction source, confidence, method                    │
│                                                                     │
│  LAYER 3: HUMAN VERIFICATION (6 fields)                             │
│  ─────────────────────────────────────────────────────────────────  │
│  Records human review decisions and corrections                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Core Data Fields (Universal)

**12 essential fields** required for Hedges' g calculation:

| # | Field | Type | Description | Required |
|---|-------|------|-------------|----------|
| 1 | `study_id` | str | Unique study identifier | Yes |
| 2 | `es_id` | str | Effect size identifier (study_id + sequence) | Yes |
| 3 | `outcome_name` | str | Measured outcome variable | Yes |
| 4 | `n_treatment` | int | Treatment group sample size | Yes |
| 5 | `n_control` | int | Control group sample size | Yes |
| 6 | `m_treatment` | float | Treatment group mean | Conditional |
| 7 | `sd_treatment` | float | Treatment group SD | Conditional |
| 8 | `m_control` | float | Control group mean | Conditional |
| 9 | `sd_control` | float | Control group SD | Conditional |
| 10 | `hedges_g` | float | Calculated effect size | Derived |
| 11 | `se_g` | float | Standard error of g | Derived |
| 12 | `es_type` | str | POST_BETWEEN\|ANCOVA\|CHANGE\|PRE_POST | Yes |

**Why these 12?**
- Minimum required for Hedges' g: M, SD, n for both groups
- `es_type` for ES hierarchy enforcement
- `hedges_g`, `se_g` are derived (calculated from raw data)

---

## Layer 2: AI Extraction Tracking

For **each extractable value** (n, M, SD), track:

| Field | Description | Example |
|-------|-------------|---------|
| `{field}_value` | Extracted value | 43 |
| `{field}_source` | PDF location | "Table 2, p.8" |
| `{field}_method` | Extraction method | OCR\|RAG\|MANUAL |
| `{field}_confidence` | AI confidence (0-100) | 85 |

**Example for `n_treatment`:**
```yaml
n_treatment_value: 43
n_treatment_source: "Table 2, Row 3, Column 2"
n_treatment_method: "OCR"
n_treatment_confidence: 92
```

### Confidence Thresholds

| Confidence | Label | Action |
|------------|-------|--------|
| ≥90% | HIGH | Auto-accept (spot check only) |
| 70-89% | MEDIUM | Human verification recommended |
| <70% | LOW | Human verification required |

---

## Layer 3: Human Verification

**6 fields** for human review workflow:

| Field | Type | Description |
|-------|------|-------------|
| `verified` | bool | Human has verified this row |
| `verified_by` | str | Reviewer initials |
| `verified_date` | date | Review date |
| `corrections` | json | Any corrections made |
| `confidence_override` | int | Human-adjusted confidence |
| `notes` | str | Review notes |

**Corrections JSON format:**
```json
{
  "n_treatment": {"original": 43, "corrected": 45, "reason": "OCR error"},
  "sd_treatment": {"original": null, "corrected": 6.3, "reason": "Found in appendix"}
}
```

---

## Simplified Excel Structure

### Sheet 1: Codebook (1 page)

| Variable | Type | AI Extracts | Human Verifies | Notes |
|----------|------|-------------|----------------|-------|
| study_id | str | No | No | Manual assignment |
| es_id | str | No | No | Auto-generated |
| outcome_name | str | Yes | Yes | From results section |
| n_treatment | int | Yes | If LOW confidence | Table/text |
| n_control | int | Yes | If LOW confidence | Table/text |
| m_treatment | float | Yes | If LOW confidence | Table/text |
| sd_treatment | float | Yes | If LOW confidence | Or calculate from CI/SE |
| m_control | float | Yes | If LOW confidence | Table/text |
| sd_control | float | Yes | If LOW confidence | Or calculate from CI/SE |
| hedges_g | float | Calculated | Verify formula | Auto-calculated |
| se_g | float | Calculated | Verify formula | Auto-calculated |
| es_type | str | Yes | Yes | POST_BETWEEN default |

### Sheet 2: Data (Main worksheet)

**26 columns total** (vs 48 in V8_VERIFICATION):

```
IDENTIFIERS (2):
  study_id, es_id

CORE VALUES (6):
  n_treatment, n_control, m_treatment, sd_treatment, m_control, sd_control

AI EXTRACTION TRACKING (12):
  {n,m,sd}_treatment_{source,method,confidence}
  {n,m,sd}_control_{source,method,confidence}

CALCULATED (2):
  hedges_g, se_g

VERIFICATION (4):
  verified, verified_by, verified_date, ai_confidence_avg
```

### Sheet 3: Review Queue

Only rows needing human review:

| study_id | es_id | issue | ai_confidence | priority | status |
|----------|-------|-------|---------------|----------|--------|
| 15 | 015_03 | sd_treatment missing | 0 | HIGH | pending |
| 22 | 022_01 | m_treatment LOW conf | 45 | MEDIUM | pending |

### Sheet 4: Extraction Log

AI extraction history:

| timestamp | study_id | field | method | value | confidence | pdf_page |
|-----------|----------|-------|--------|-------|------------|----------|
| 2026-01-26 | 15 | n_treatment | OCR | 43 | 92 | 8 |

---

## AI-Human Collaboration Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│              AI-HUMAN COLLABORATION WORKFLOW                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PHASE 1: AI EXTRACTION (Automated)                                 │
│  ───────────────────────────────────────────────────────────────── │
│  1. ScholaRAG builds RAG from PDFs                                  │
│  2. C6 agent queries RAG for statistical values                     │
│  3. OCR fallback for tables/figures                                 │
│  4. AI assigns confidence score to each value                       │
│  5. Calculate Hedges' g where possible                              │
│                                                                     │
│  Output: Initial data with confidence scores                        │
│                                                                     │
│  PHASE 2: TRIAGE (Automated)                                        │
│  ───────────────────────────────────────────────────────────────── │
│  C7 agent categorizes rows:                                         │
│    • GREEN (≥90%): Auto-accept                                      │
│    • YELLOW (70-89%): Human verification recommended                │
│    • RED (<70%): Human verification required                        │
│    • MISSING: AI re-extraction with different method               │
│                                                                     │
│  Output: Prioritized review queue                                   │
│                                                                     │
│  PHASE 3: HUMAN REVIEW (Manual)                                     │
│  ───────────────────────────────────────────────────────────────── │
│  Human reviews RED and YELLOW rows:                                 │
│    1. View AI extraction with source location                       │
│    2. Verify or correct value                                       │
│    3. Mark as verified                                              │
│    4. If correction needed → AI learns for similar patterns         │
│                                                                     │
│  Output: Verified data                                              │
│                                                                     │
│  PHASE 4: ITERATION (AI Re-extraction)                              │
│  ───────────────────────────────────────────────────────────────── │
│  For remaining MISSING values:                                      │
│    1. AI tries alternative extraction methods                       │
│    2. Calculate from related values (SE→SD, CI→SD)                  │
│    3. Flag for manual PDF review if still missing                   │
│                                                                     │
│  Output: Maximized data coverage                                    │
│                                                                     │
│  PHASE 5: FINAL VERIFICATION (Human)                                │
│  ───────────────────────────────────────────────────────────────── │
│  Human reviews any remaining issues                                 │
│  C5 validates all gates pass                                        │
│  Final approval → 100% verified dataset                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Integration with Diverga

### C5-MetaAnalysisMaster

Orchestrates the workflow:
```python
# Phase 1: AI Extraction
c5.extract_from_pdfs(pdf_folder, method="rag_then_ocr")

# Phase 2: Triage
c5.triage_by_confidence(threshold_high=90, threshold_low=70)

# Phase 3: Generate review queue
c5.generate_review_queue()

# Phase 5: Final validation
c5.validate_all_gates()
```

### C6-DataIntegrityGuard

Handles extraction and calculation:
```python
# Extract values with confidence
values = c6.extract_with_confidence(pdf, fields=["n", "m", "sd"])

# Calculate Hedges' g
g, se = c6.calculate_hedges_g(m1, sd1, n1, m2, sd2, n2)

# SD recovery strategies
sd = c6.recover_sd(method="from_ci", ci_lower=2.1, ci_upper=5.3, n=43)
```

### C7-ErrorPreventionEngine

Provides warnings and anomaly detection:
```python
# Check for pre-test patterns
warnings = c7.check_pretest_patterns(outcome_name)

# Detect anomalies
anomalies = c7.detect_anomalies(hedges_g, threshold=3.0)

# Generate human review recommendations
recommendations = c7.recommend_human_review(confidence_scores)
```

---

## Integration with ScholaRAG

### PDF → RAG → Extraction Pipeline

```python
# ScholaRAG Stage 5: Build RAG
scholarag build_rag --project my_project

# C6 Agent queries RAG
prompt = """
From the study results, extract:
1. Sample size for treatment group (n)
2. Sample size for control group (n)
3. Mean for treatment group (M)
4. Standard deviation for treatment group (SD)
5. Mean for control group (M)
6. Standard deviation for control group (SD)

If any value is not found, respond with "NOT_FOUND".
For each value found, provide:
- The extracted value
- The exact location (page, table, paragraph)
- Your confidence (0-100%)
"""

response = rag.query(prompt, pdf_id=study_id)
```

### OCR Fallback for Tables

```python
# If RAG returns LOW confidence for M/SD
if response.confidence < 70:
    # Use OCR on detected tables
    tables = ocr.extract_tables(pdf, pages=[results_page])
    values = parse_statistical_table(tables)
```

---

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Initial AI extraction rate | ≥80% | Values extracted / Total values |
| AI confidence accuracy | ≥85% | AI HIGH conf values verified correct |
| Human review efficiency | ≤20% | Values requiring human review |
| Final data completeness | 100% | All rows have Hedges' g |
| Final data accuracy | 100% | All values human-verified |

---

## Implementation Phases

### Phase 1: Core Codebook (Week 1)
- [ ] Create simplified Excel template
- [ ] Implement C6 extraction functions
- [ ] Test on V8 GenAI data

### Phase 2: AI Extraction (Week 2)
- [ ] Integrate with ScholaRAG RAG
- [ ] Implement OCR fallback
- [ ] Build confidence scoring

### Phase 3: Human Review UI (Week 3)
- [ ] Create interactive review workflow
- [ ] Implement correction tracking
- [ ] Build progress dashboard

### Phase 4: Integration (Week 4)
- [ ] Full C5/C6/C7 integration
- [ ] Diverga skill documentation
- [ ] Test on real meta-analysis project

---

## Questions for Review

1. **Column count**: Is 26 columns still too many? Could reduce to ~18 by combining source/method/confidence into JSON?

2. **Confidence thresholds**: Are 90/70 appropriate defaults, or should they be configurable?

3. **OCR integration**: Should OCR be automatic fallback or user-triggered?

4. **Multi-extraction**: When AI extracts different values from different methods, how to reconcile?

5. **Learning loop**: Should AI extraction improve from human corrections? (ML feedback loop)

---

## References

- Borenstein et al. (2021). Introduction to Meta-Analysis
- Cochrane Handbook Chapter 6: Extracting data
- PRISMA 2020 Statement
- ScholaRAG documentation
- Diverga C5/C6/C7 agent specifications

---

*Plan created: 2026-01-26*
*Author: Claude Code*
*Status: PENDING CODEX REVIEW*
