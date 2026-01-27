# Universal Meta-Analysis Codebook v2: AI-Human Collaboration Plan

## Revision Summary

**Based on Codex Review (NEEDS REVISION)**

| Issue | Resolution |
|-------|------------|
| 100% accuracy unrealistic | Changed to "100% human-verified" with mandatory review |
| Core fields too thin | Added metadata block (10 fields) |
| No conflict resolution | Added extraction hierarchy + reconciliation rules |
| Static confidence thresholds | Made configurable per-field/source |
| Derived fields lack provenance | Added provenance tracking |

**v2.1 Minor Fixes (Codex Review APPROVE WITH MINOR CHANGES):**
- Fixed metadata field count (7→10)
- Added pre/post and cluster design fields
- Fixed reconciliation divide-by-zero edge case
- Extended thresholds to hedges_g/se_g
- Clarified derived value verification scope

---

## Revised Architecture

### Four-Layer Design (Expanded from Three)

```
┌─────────────────────────────────────────────────────────────────────┐
│              UNIVERSAL META-ANALYSIS CODEBOOK v2                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  LAYER 1: IDENTIFIERS + METADATA (10 fields)                        │
│  ─────────────────────────────────────────────────────────────────  │
│  study_id, es_id, citation, doi, year, design_type,                │
│  timepoint, arm_label_treat, arm_label_control, unit_of_analysis   │
│                                                                     │
│  LAYER 2: CORE STATISTICAL VALUES (12 fields)                       │
│  ─────────────────────────────────────────────────────────────────  │
│  outcome_name, outcome_unit, es_type, analysis_type,               │
│  n_treatment, n_control, m_treatment, sd_treatment,                │
│  m_control, sd_control, hedges_g, se_g                             │
│                                                                     │
│  LAYER 3: AI EXTRACTION PROVENANCE (per value: 5 fields)           │
│  ─────────────────────────────────────────────────────────────────  │
│  {field}_ai_value, {field}_source, {field}_method,                 │
│  {field}_confidence, {field}_derived_from                          │
│                                                                     │
│  LAYER 4: HUMAN VERIFICATION (8 fields)                             │
│  ─────────────────────────────────────────────────────────────────  │
│  verified_status, verified_by, verified_date,                      │
│  corrections_json, disagreement_resolved, final_value,             │
│  verification_notes, sign_off                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Identifiers + Metadata (10 fields)

| # | Field | Type | Description | Example |
|---|-------|------|-------------|---------|
| 1 | `study_id` | str | Unique study identifier | "CHEN_2024" |
| 2 | `es_id` | str | Effect size ID | "CHEN_2024_01" |
| 3 | `citation` | str | Full APA citation | "Chen et al. (2024)..." |
| 4 | `doi` | str | Digital Object Identifier | "10.1000/xyz" |
| 5 | `year` | int | Publication year | 2024 |
| 6 | `design_type` | str | Study design | RCT\|QUASI\|PRE_POST |
| 7 | `timepoint` | str | Measurement timing | post\|follow_up_3m |
| 8 | `arm_label_treat` | str | Treatment group label | "ChatGPT group" |
| 9 | `arm_label_control` | str | Control group label | "Traditional" |
| 10 | `unit_of_analysis` | str | Analysis unit | individual\|cluster |

---

## Layer 2: Core Statistical Values (18 fields)

### Primary Statistics (12 fields)

| # | Field | Type | Description | Required |
|---|-------|------|-------------|----------|
| 11 | `outcome_name` | str | Measured outcome | "Critical thinking" |
| 12 | `outcome_unit` | str | Measurement unit | "score (0-100)" |
| 13 | `es_type` | str | Effect size type | POST_BETWEEN\|ANCOVA\|CHANGE\|PRE_POST |
| 14 | `analysis_type` | str | Adjusted/unadjusted | adjusted\|unadjusted |
| 15 | `n_treatment` | int | Treatment n | 43 |
| 16 | `n_control` | int | Control n | 45 |
| 17 | `m_treatment` | float | Treatment mean | 75.3 |
| 18 | `sd_treatment` | float | Treatment SD | 12.5 |
| 19 | `m_control` | float | Control mean | 68.7 |
| 20 | `sd_control` | float | Control SD | 14.2 |
| 21 | `hedges_g` | float | Effect size | 0.48 |
| 22 | `se_g` | float | Standard error | 0.21 |

### Change-Score Design Fields (3 fields, conditional)

| # | Field | Type | Description | When Used |
|---|-------|------|-------------|-----------|
| 23 | `pre_mean_treat` | float | Pre-test mean (treatment) | es_type = CHANGE |
| 24 | `pre_sd_treat` | float | Pre-test SD (treatment) | es_type = CHANGE |
| 25 | `pre_post_corr` | float | Pre-post correlation (0-1) | es_type = CHANGE |

### Cluster Design Fields (3 fields, conditional)

| # | Field | Type | Description | When Used |
|---|-------|------|-------------|-----------|
| 26 | `cluster_size` | float | Avg cluster size | unit_of_analysis = cluster |
| 27 | `icc` | float | Intra-class correlation | unit_of_analysis = cluster |
| 28 | `n_clusters` | int | Number of clusters | unit_of_analysis = cluster |

---

## Layer 3: AI Extraction Provenance

### Per-Value Tracking (5 fields per extractable value)

For each statistical value (n, M, SD × 2 groups = 6 values):

| Field | Description | Example |
|-------|-------------|---------|
| `{field}_ai_value` | AI-extracted value | 43 |
| `{field}_source` | PDF location | "Table 2, p.8, Row 3" |
| `{field}_method` | Extraction method | RAG\|OCR\|TEXT |
| `{field}_confidence` | Confidence (0-100) | 85 |
| `{field}_derived_from` | If calculated | "CI_95" or null |

**Example for `sd_treatment`:**
```yaml
sd_treatment_ai_value: 12.5
sd_treatment_source: "Table 3, p.12"
sd_treatment_method: "OCR"
sd_treatment_confidence: 78
sd_treatment_derived_from: null  # Direct extraction

# OR if calculated from CI:
sd_treatment_ai_value: 12.5
sd_treatment_source: "Text p.11, 95% CI [10.2, 14.8]"
sd_treatment_method: "CALCULATED"
sd_treatment_confidence: 92  # High because formula-based
sd_treatment_derived_from: "CI_95: SE = (14.8-10.2)/3.92 = 1.17; SD = SE × √n"
```

### Derived Value Provenance

When values are calculated (not directly extracted):

| Field | Description |
|-------|-------------|
| `formula_used` | Calculation formula |
| `source_statistics` | Original stats used |
| `assumptions` | Any assumptions made |
| `conversion_confidence` | Confidence in conversion |

**Example:**
```yaml
# SD calculated from 95% CI
formula_used: "SD = SE × √n; SE = (CI_upper - CI_lower) / 3.92"
source_statistics: "CI_lower: 10.2, CI_upper: 14.8, n: 43"
assumptions: "Normal distribution, two-tailed CI"
conversion_confidence: 95
```

---

## Layer 4: Human Verification (8 fields)

| # | Field | Type | Description |
|---|-------|------|-------------|
| 29 | `verified_status` | str | PENDING\|PROVISIONAL\|VERIFIED\|REJECTED |
| 30 | `verified_by` | str | Reviewer initials |
| 31 | `verified_date` | date | Review date |
| 32 | `corrections_json` | json | Any corrections made |
| 33 | `disagreement_resolved` | bool | Multi-extraction conflict resolved |
| 34 | `final_values_json` | json | Human-confirmed values (consistent naming) |
| 35 | `verification_notes` | str | Review notes |
| 36 | `sign_off` | bool | Final approval |

### Derived Value Verification Scope

**What counts as "human-verified" for derived values (hedges_g, se_g)?**

| Verification Level | What to Check | When Required |
|--------------------|---------------|---------------|
| **Source Verification** | Confirm source values (M, SD, n) match PDF | Always |
| **Formula Verification** | Confirm correct formula applied | If confidence < 90% |
| **Input Chain Verification** | Trace back to original extracted values | If ANY source was corrected |
| **Calculation Re-run** | Re-run Hedges' g calculation | If corrections made to inputs |

**Human verification of derived values means:**
1. ✅ All source values (M, SD, n) have been verified
2. ✅ Formula used is appropriate for the es_type
3. ✅ If change-score: pre_post_corr verified or reasonable default (r=0.5) documented
4. ✅ If cluster: ICC and cluster_size verified or design effect applied
5. ✅ Final hedges_g and se_g values are recalculated from verified inputs

### Verification Status Flow

```
PENDING → PROVISIONAL → VERIFIED
    ↓          ↓
 REJECTED   REJECTED

PENDING: Not yet reviewed
PROVISIONAL: AI auto-accepted (HIGH confidence), awaiting final sign-off
VERIFIED: Human reviewed and confirmed
REJECTED: Excluded from analysis
```

### Corrections JSON Format

```json
{
  "n_treatment": {
    "ai_value": 43,
    "final_value": 45,
    "reason": "OCR error: '43' was actually '45'",
    "source_verified": "Table 2, p.8"
  },
  "sd_treatment": {
    "ai_value": null,
    "final_value": 12.5,
    "reason": "Found in Supplementary Table S2",
    "source_verified": "Appendix, Table S2"
  }
}
```

---

## Multi-Extraction Conflict Resolution

### Extraction Hierarchy (Deterministic)

When multiple methods extract different values:

| Priority | Source Type | Weight |
|----------|-------------|--------|
| 1 (Highest) | Table cell | 1.0 |
| 2 | Figure data point | 0.9 |
| 3 | In-text statistics | 0.8 |
| 4 | Abstract/narrative | 0.5 |

### Reconciliation Rules

```python
# Epsilon for numerical stability (avoid divide-by-zero)
EPSILON = 0.001
ABSOLUTE_TOLERANCE = {"n": 2, "m": 0.5, "sd": 0.5}  # Absolute thresholds for small values

def reconcile_extractions(extractions: list, field_type: str) -> dict:
    """
    Reconcile when multiple extractions disagree.

    Args:
        extractions: List of {value, source_type, confidence, method}
        field_type: "n", "m", or "sd" for appropriate tolerance

    Returns:
        {final_value, confidence, needs_human_review}
    """
    if len(extractions) == 1:
        return extractions[0]

    # Sort by hierarchy weight × confidence
    scored = [(e, HIERARCHY_WEIGHT[e.source_type] * e.confidence) for e in extractions]
    scored.sort(key=lambda x: x[1], reverse=True)

    best = scored[0][0]
    second = scored[1][0] if len(scored) > 1 else None

    if second:
        # Use max(|best|, |second|, ε) to avoid divide-by-zero
        denominator = max(abs(best.value), abs(second.value), EPSILON)
        relative_diff = abs(best.value - second.value) / denominator
        absolute_diff = abs(best.value - second.value)

        # Check BOTH relative and absolute tolerance (either triggers review)
        exceeds_relative = relative_diff > TOLERANCE[field_type]
        exceeds_absolute = absolute_diff > ABSOLUTE_TOLERANCE[field_type]

        if exceeds_relative or exceeds_absolute:
            # Significant disagreement → human review required
            return {
                "final_value": best.value,
                "confidence": best.confidence * 0.7,  # Penalize confidence
                "needs_human_review": True,
                "candidates": extractions,
                "disagreement_detail": {
                    "relative_diff": round(relative_diff, 3),
                    "absolute_diff": round(absolute_diff, 2)
                }
            }

    return {
        "final_value": best.value,
        "confidence": best.confidence,
        "needs_human_review": False
    }
```

### Tolerance Thresholds

| Value Type | Tolerance | Trigger Human Review If |
|------------|-----------|------------------------|
| n (sample size) | 5% | n₁ differs from n₂ by >5% |
| M (mean) | 10% | M₁ differs from M₂ by >10% |
| SD | 15% | SD₁ differs from SD₂ by >15% |

---

## Configurable Confidence Thresholds

### Per-Field Thresholds

| Field | HIGH (Auto-provisional) | MEDIUM (Recommend review) | LOW (Require review) |
|-------|------------------------|--------------------------|---------------------|
| n (sample size) | ≥95% | 80-94% | <80% |
| M (mean) | ≥90% | 70-89% | <70% |
| SD | ≥85% | 65-84% | <65% |
| Calculated (from CI/SE) | ≥90% | 75-89% | <75% |
| hedges_g (derived) | ≥92% | 75-91% | <75% |
| se_g (derived) | ≥92% | 75-91% | <75% |
| pre_post_corr | ≥85% | 65-84% | <65% |
| icc | ≥80% | 60-79% | <60% |

### Derived Value Confidence Calculation

For calculated values (hedges_g, se_g), confidence is propagated from source values:

```python
# Derived value confidence = min(source confidences) × formula_reliability
hedges_g_confidence = min(m_treat_conf, m_ctrl_conf, sd_treat_conf, sd_ctrl_conf, n_treat_conf, n_ctrl_conf) * 0.95
se_g_confidence = hedges_g_confidence * 0.98
```

### Per-Source Calibration

| Source | Confidence Modifier |
|--------|---------------------|
| Structured table | +10% |
| Semi-structured figure | +5% |
| Unstructured text | 0% |
| Abstract only | -15% |
| OCR with artifacts | -20% |

**Formula:** `effective_confidence = base_confidence + source_modifier`

---

## Revised Workflow: "100% Human-Verified"

```
┌─────────────────────────────────────────────────────────────────────┐
│          AI-HUMAN COLLABORATION WORKFLOW (Revised)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  PHASE 1: AI EXTRACTION (Automated)                                 │
│  ───────────────────────────────────────────────────────────────── │
│  1. ScholaRAG builds RAG from PDFs                                  │
│  2. C6 queries for statistical values (RAG + OCR)                   │
│  3. Multiple extraction methods run in parallel                     │
│  4. Conflict resolution applied (hierarchy + tolerance)             │
│  5. Provenance recorded for all extractions                         │
│  6. Hedges' g calculated where possible                             │
│                                                                     │
│  Status: All rows → PENDING                                         │
│                                                                     │
│  PHASE 2: TRIAGE (Automated)                                        │
│  ───────────────────────────────────────────────────────────────── │
│  C7 categorizes rows based on effective_confidence:                 │
│    • HIGH confidence → PROVISIONAL (auto-accepted, awaits sign-off) │
│    • MEDIUM confidence → PENDING (recommended review)               │
│    • LOW confidence → PENDING (required review, prioritized)        │
│    • Conflict detected → PENDING (required review, top priority)    │
│                                                                     │
│  PHASE 3: HUMAN REVIEW (Mandatory for ALL rows)                     │
│  ───────────────────────────────────────────────────────────────── │
│  **Critical Change: ALL rows require human verification**           │
│                                                                     │
│  Priority Queue:                                                    │
│    1. Conflict detected (highest priority)                          │
│    2. LOW confidence                                                │
│    3. MEDIUM confidence                                             │
│    4. HIGH confidence (PROVISIONAL → spot check)                    │
│                                                                     │
│  Human actions:                                                     │
│    • Verify AI extraction against PDF                               │
│    • Correct errors and record reason                               │
│    • Mark as VERIFIED or REJECTED                                   │
│    • Resolve any conflicts                                          │
│                                                                     │
│  PHASE 4: FINAL SIGN-OFF (Human)                                    │
│  ───────────────────────────────────────────────────────────────── │
│  1. C5 validates all gates pass                                     │
│  2. Human reviews summary statistics                                │
│  3. Human approves final dataset                                    │
│  4. All rows must have sign_off = True                              │
│                                                                     │
│  Result: 100% HUMAN-VERIFIED dataset                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Simplified Excel Structure (Revised)

### Sheet 1: Codebook

One page, clear categories:

```markdown
## IDENTIFIERS & METADATA (10 fields)
study_id, es_id, citation, doi, year, design_type, timepoint,
arm_label_treat, arm_label_control, unit_of_analysis

## CORE STATISTICAL VALUES (12 fields)
outcome_name, outcome_unit, es_type, analysis_type,
n_treatment, n_control, m_treatment, sd_treatment,
m_control, sd_control, hedges_g, se_g

## AI EXTRACTION (stored as JSON in single column)
ai_extraction_json: Contains all provenance data

## HUMAN VERIFICATION (8 fields)
verified_status, verified_by, verified_date, corrections_json,
disagreement_resolved, final_value_json, verification_notes, sign_off
```

### Sheet 2: Data (Main)

**36 visible columns** + 2 JSON columns for complex provenance:

| Category | Columns | Count |
|----------|---------|-------|
| Identifiers & Metadata | study_id → unit_of_analysis | 10 |
| Primary Statistics | outcome_name → se_g | 12 |
| Change-Score Fields | pre_mean_treat, pre_sd_treat, pre_post_corr | 3 |
| Cluster Fields | cluster_size, icc, n_clusters | 3 |
| AI Extraction Summary | ai_confidence_avg, ai_method, ai_conflicts | 3 |
| AI Provenance (JSON) | ai_extraction_json | 1 |
| Human Verification | verified_status → sign_off | 8 |
| Final Values (JSON) | final_values_json | 1 |

**Total: 41 columns** (39 visible + 2 JSON)

*Note: Change-score and cluster fields are conditionally populated based on design type.*

### Sheet 3: Review Queue

| study_id | es_id | priority | issue | ai_confidence | status |
|----------|-------|----------|-------|---------------|--------|
| CHEN_2024 | 01 | 1 | CONFLICT | 72 | pending |
| LEE_2023 | 03 | 2 | LOW_CONF | 58 | pending |

### Sheet 4: Extraction Log

| timestamp | study_id | field | method | value | confidence | source |
|-----------|----------|-------|--------|-------|------------|--------|
| 2026-01-26 | CHEN_2024 | n_treatment | RAG | 43 | 85 | Table 2 |
| 2026-01-26 | CHEN_2024 | n_treatment | OCR | 45 | 78 | Table 2 |
| 2026-01-26 | CHEN_2024 | n_treatment | RESOLVED | 45 | 72 | CONFLICT |

---

## Integration with Diverga C5/C6/C7

### C5-MetaAnalysisMaster Integration

```python
# Phase 1: Extraction with provenance
extraction_result = c5.extract_with_provenance(
    pdf_folder="./pdfs",
    methods=["rag", "ocr"],
    reconciliation="hierarchy",
    log_all_candidates=True
)

# Phase 2: Triage with configurable thresholds
triage_result = c5.triage(
    data=extraction_result,
    thresholds={
        "n": {"high": 95, "medium": 80},
        "m": {"high": 90, "medium": 70},
        "sd": {"high": 85, "medium": 65}
    }
)

# Phase 4: Final validation
validation = c5.validate_final(
    data=verified_data,
    require_all_verified=True,
    require_all_signed_off=True
)
```

### C6-DataIntegrityGuard Integration

```python
# Calculate with provenance tracking
result = c6.calculate_hedges_g_with_provenance(
    m1=75.3, sd1=12.5, n1=43,
    m2=68.7, sd2=14.2, n2=45,
    sources={
        "m1": "Table 2, p.8",
        "sd1": "Calculated from CI",
        "formula": "SD = SE × √n"
    }
)

# SD recovery with provenance
sd_result = c6.recover_sd(
    method="from_ci",
    ci_lower=10.2,
    ci_upper=14.8,
    n=43,
    assumptions="Normal distribution"
)
# Returns: {"value": 12.5, "confidence": 92, "formula": "...", "assumptions": [...]}
```

### C7-ErrorPreventionEngine Integration

```python
# Multi-extraction conflict detection
conflicts = c7.detect_extraction_conflicts(
    extractions=[
        {"method": "RAG", "value": 43, "confidence": 85},
        {"method": "OCR", "value": 45, "confidence": 78}
    ],
    tolerance=0.05
)
# Returns: {"has_conflict": True, "severity": "HIGH", "recommend": "HUMAN_REVIEW"}

# Configurable threshold validation
validation = c7.validate_confidence(
    field="sd_treatment",
    confidence=72,
    source_type="ocr_with_artifacts",
    thresholds=config.thresholds
)
# Returns: {"effective_confidence": 52, "category": "LOW", "action": "REQUIRE_REVIEW"}
```

---

## Success Metrics (Revised)

| Metric | Target | Measurement |
|--------|--------|-------------|
| AI initial extraction rate | ≥85% | Values extracted / Total values |
| AI confidence accuracy | ≥90% | HIGH conf values verified correct |
| Conflict detection rate | ≥95% | True conflicts detected / Actual conflicts |
| Human review completeness | 100% | All rows have verified_status ≠ PENDING |
| Final sign-off rate | 100% | All rows have sign_off = True |
| Data completeness | ≥95% | Rows with valid Hedges' g |

---

## Implementation Phases (Revised)

### Phase 1: Core Framework (Week 1)
- [ ] Create simplified Excel template (34 columns)
- [ ] Implement JSON-based provenance storage
- [ ] Create codebook with examples

### Phase 2: AI Extraction (Week 2)
- [ ] Integrate ScholaRAG RAG queries
- [ ] Implement OCR extraction
- [ ] Build multi-extraction reconciliation
- [ ] Implement configurable confidence thresholds

### Phase 3: Human Review UI (Week 3)
- [ ] Priority-based review queue
- [ ] Conflict resolution interface
- [ ] Correction tracking
- [ ] Sign-off workflow

### Phase 4: Integration & Testing (Week 4)
- [ ] Full C5/C6/C7 integration
- [ ] Test on V8 GenAI data
- [ ] Calibrate confidence thresholds
- [ ] Document in Diverga

---

## Comparison: V1 vs V2.1

| Aspect | V1 (Rejected) | V2.1 (Approved) |
|--------|---------------|-----------------|
| Columns | 26 | 41 (39 + 2 JSON) |
| Metadata | 2 (study_id, es_id) | 10 (full provenance) |
| Accuracy claim | "100% accuracy" | "100% human-verified" |
| Human review | Only LOW confidence | ALL rows (prioritized) |
| Conflict resolution | None | Hierarchy + tolerance + absolute |
| Thresholds | Static (90/70) | Per-field, per-source, derived values |
| Provenance | Minimal | Full tracking (JSON) |
| Design support | POST_BETWEEN only | Change-score + Cluster designs |
| Derived verification | Not defined | Explicit verification scope |

---

*Plan v2.1: 2026-01-26*
*Codex Review: APPROVE WITH MINOR CHANGES*
*Status: ✅ READY FOR IMPLEMENTATION*
