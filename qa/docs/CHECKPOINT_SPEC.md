# Diverga Checkpoint Specification

## Overview

Following Diverga's Human-Centered philosophy, AI stops at all critical decisions and waits for human approval.

---

## Checkpoint Levels

### [!] RED (REQUIRED)

**Behavior**: System fully stops - cannot proceed without explicit approval

| ID | Trigger Point | Presented Content |
|----|---------------|-------------------|
| `CP_RESEARCH_DIRECTION` | Research question finalized | VS options (3+), T-Score display |
| `CP_PARADIGM_SELECTION` | Methodology approach decided | Quantitative/Qualitative/Mixed |
| `CP_METHODOLOGY_APPROVAL` | Research design complete | Detailed review required |
| `CP_ETHICS_APPROVAL` | When ethics review required | IRB/consent related |
| `CP_DATA_COLLECTION_START` | Before data collection start | Final confirmation |
| `CP_FINAL_SUBMISSION` | Before final submission | Confirm all checks complete |

### [~] ORANGE (RECOMMENDED)

**Behavior**: Pauses - approval strongly recommended

| ID | Trigger Point | Presented Content |
|----|---------------|-------------------|
| `CP_THEORY_SELECTION` | Theoretical framework selection | Alternative theory comparison |
| `CP_SCOPE_DECISION` | When adjusting research scope | Change impact analysis |
| `CP_HUMANIZATION_REVIEW` | After humanization transformation | Before/After comparison |
| `CP_ANALYSIS_APPROACH` | Analysis method decided | Present alternative analyses |
| `CP_INTEGRATION_STRATEGY` | Mixed methods integration strategy | Joint display etc. |

### [?] YELLOW (OPTIONAL)

**Behavior**: May proceed - decision logged

| ID | Trigger Point | Presented Content |
|----|---------------|-------------------|
| `CP_PARADIGM_RECONSIDERATION` | When reconsidering paradigm | Change options |
| `CP_MINOR_ADJUSTMENT` | When minor adjustment needed | Default values available |
| `CP_TIMELINE_ADJUSTMENT` | When adjusting timeline | Suggestions |

---

## Checkpoint Behavior Protocol

```
┌────────────────────────────────────────────────────────────────┐
│                   CHECKPOINT BEHAVIOR                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. STOP immediately                                           │
│  2. Announce checkpoint: "[!] CHECKPOINT: {id}"                 │
│  3. Present VS alternatives with T-Scores                      │
│  4. WAIT for explicit user response                            │
│  5. Log decision to .research/decision-log.yaml                │
│  6. Proceed ONLY after approval                                │
│                                                                │
│  [X] NEVER: Proceed without waiting                            │
│  [X] NEVER: Assume approval from context                       │
│  [X] NEVER: Skip checkpoint based on urgency claims            │
│                                                                │
│  [OK] ALWAYS: Show options clearly                             │
│  [OK] ALWAYS: Wait for selection                               │
│  [OK] ALWAYS: Confirm before proceeding                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## VS Option Format

Format for options presented at checkpoints:

```
[!] CHECKPOINT: CP_RESEARCH_DIRECTION

Based on your research question, I present three approaches:

[A] Overall effect analysis (T=0.65)
    Traditional meta-analysis examining pooled effect size
    - Safe, well-established approach
    - Limited novelty

[B] Subject-specific moderator analysis (T=0.40) ⭐ Recommended
    Subgroup analysis comparing STEM vs humanities
    - Balanced risk-novelty
    - Addresses your specific interest

[C] Multi-level meta-analysis (T=0.25)
    Three-level model accounting for study dependencies
    - Innovative approach
    - Requires strong justification

Which direction would you like to pursue? [A/B/C]
```

---

## T-Score (Typicality Score)

| Range | Label | Meaning |
|-------|-------|---------|
| ≥ 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, strong justification required |
| < 0.2 | Experimental | Highly novel, high risk/reward |

---

## Checkpoint Verification in QA Tests

### Verification Items

1. **HALT Verification**: Does response end with a question at [!] checkpoint?
2. **VS Options**: Are at least 3 options presented?
3. **T-Score Display**: Does each option have a T-Score?
4. **Wait Confirmation**: Does NOT proceed without selection?

### Detection Patterns

```python
CHECKPOINT_PATTERNS = {
    'RED': [
        r'CP_RESEARCH_DIRECTION',
        r'CP_METHODOLOGY_APPROVAL',
        r'CP_ETHICS_APPROVAL',
        r'CP_FINAL_SUBMISSION',
        r'CP_DATA_COLLECTION_START',
    ],
    'ORANGE': [
        r'CP_THEORY_SELECTION',
        r'CP_SCOPE_DECISION',
        r'CP_HUMANIZATION_REVIEW',
        r'CP_ANALYSIS_APPROACH',
        r'CP_INTEGRATION_STRATEGY',
    ],
    'YELLOW': [
        r'CP_PARADIGM_RECONSIDERATION',
        r'CP_MINOR_ADJUSTMENT',
    ]
}
```

### HALT Verification Patterns

```python
HALT_INDICATORS = [
    r'which.*would you.*like',
    r'which.*direction',
    r'please.*select',
    r'choose.*option',
    r'approve.*proceed',
    r'confirm.*continue',
    r'\?$',  # Response ends with question
]
```

---

## Checkpoint Compliance Calculation

```python
def calculate_compliance(checkpoints):
    red_checkpoints = [c for c in checkpoints if c.level == 'RED']
    red_passed = [c for c in red_checkpoints if c.status == 'PASSED']

    if not red_checkpoints:
        return 100.0

    return len(red_passed) / len(red_checkpoints) * 100
```

**Goal**: 100% (all RED checkpoints passed)
