# VS Methodology Tests - 2026-01-29

## Overview

Tests verifying Verbalized Sampling (VS) methodology implementation - ensuring creative alternatives are presented with T-Scores.

## VS Methodology Core Concepts

### T-Score (Typicality Score)

| T-Score | Label | Meaning |
|---------|-------|---------|
| >= 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, requires strong justification |
| < 0.2 | Experimental | Highly novel, high risk/reward |

### VS Process Stages

```
Stage 1: Context & Modal Identification
  └─ Identify "obvious" recommendations

Stage 2: Divergent Exploration
  ├─ Direction A (T~0.6): Safe but differentiated
  ├─ Direction B (T~0.4): Balanced novelty ⭐
  └─ Direction C (T<0.3): Innovative/experimental

Stage 3: Human Selection (🔴 CHECKPOINT)
  ├─ Present ALL options with T-Scores
  ├─ WAIT for human decision
  └─ Execute ONLY selected direction
```

## Test Results Summary

| Scenario | VS Options | T-Score Range | Modal Avoided | Result |
|----------|------------|---------------|---------------|--------|
| META-001 | 3 | 0.25 - 0.65 | ✅ | ✅ PASS |
| QUAL-001 | 3-4 | 0.30 - 0.60 | ✅ | ✅ PASS |
| MIXED-001 | 3-4 | 0.30 - 0.55 | ✅ | ✅ PASS |
| HUMAN-001 | 3 | 0.25 - 0.65 | ✅ | ✅ PASS |

## VS Quality Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| Option Diversity | ≥ 0.3 T-Score spread | ✅ 0.30-0.40 |
| Modal Avoidance | No T≥0.8 as primary | ✅ 100% |
| Creative Options | ≥ 1 option T≤0.4 | ✅ Present |

## Example VS Alternatives Presented

### META-001: Research Direction
```
[A] Overall effect analysis (T=0.65)
    Traditional meta-analysis examining overall AI tutor effectiveness

[B] Subject-specific effects (T=0.40) ⭐
    Subgroup analysis by subject area (STEM vs humanities)

[C] Moderator analysis (T=0.25)
    Comprehensive moderator analysis including individual differences
```

### QUAL-001: Phenomenological Approach
```
[A] Descriptive Phenomenology (Husserl) (T=0.60)
    Bracketing and eidetic reduction

[B] Interpretive Phenomenology (Heidegger/van Manen) (T=0.45) ⭐
    Hermeneutic circle and interpretation

[C] IPA (Interpretative Phenomenological Analysis) (T=0.35)
    Idiographic focus with systematic analysis
```

## Key Findings

### ✅ Working Correctly
- T-Scores displayed for all options
- Modal (T≥0.8) options avoided as primary recommendation
- Creative/innovative options included
- Balanced recommendations marked with ⭐

### ⚠️ Areas for Improvement
- VS Quality score shows 20% in automated tests (pattern matching needs refinement)
- Real T-Score calculation needs semantic analysis
- Dynamic T-Score adjustment based on context not yet validated

## Related Reports

- [SIMULATION_TRANSCRIPTS.md](../reports/SIMULATION_TRANSCRIPTS.md)
- Individual YAML reports in [reports/individual/](../reports/individual/)
