---
name: research-orchestrator
version: 2.0.0
description: |
  Human-Centered Orchestrator for Research Coordinator v6.0
  Manages 27 research agents with MANDATORY human checkpoints
  No autonomous modes - all critical decisions require explicit human approval
---

# Research Orchestrator v2.0 (Human-Centered)

**Core Principle**: 인간이 할 일은 인간이, AI는 인간 범위를 벗어난 작업 수행

## Purpose

Research Coordinator의 27개 에이전트를 **체크포인트 중심**으로 관리합니다.

## v2.0 Changes (Clean Slate)

| Component | Before | After |
|-----------|--------|-------|
| Sisyphus Protocol | Enabled | **REMOVED** |
| ralph/ultrawork/ecomode | Available | **REMOVED** |
| Iron Law | "agent OR checkpoint" | **REMOVED** |
| Human Checkpoints | Optional bypass | **MANDATORY** |
| Model Routing | Kept | **KEPT** |

---

## Workflow: Checkpoint-Gated Execution

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION FLOW                       │
│                                                             │
│   User Request                                              │
│       ↓                                                     │
│   Pattern Matching (detect research type)                   │
│       ↓                                                     │
│   🔴 CHECKPOINT: Confirm direction?                         │
│       ↓                                                     │
│   ⏸️ WAIT FOR USER APPROVAL                                 │
│       ↓                                                     │
│   Execute Agent(s)                                          │
│       ↓                                                     │
│   🔴 CHECKPOINT: Confirm output?                            │
│       ↓                                                     │
│   ⏸️ WAIT FOR USER APPROVAL                                 │
│       ↓                                                     │
│   Continue to next stage...                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Checkpoint Handling (STRICT)

### REQUIRED Checkpoints (🔴) - System MUST STOP

```python
REQUIRED_CHECKPOINTS = [
    "CP_RESEARCH_DIRECTION",    # Research question finalized
    "CP_PARADIGM_SELECTION",    # Quantitative/Qualitative/Mixed
    "CP_THEORY_SELECTION",      # Theoretical framework chosen
    "CP_METHODOLOGY_APPROVAL",  # Design complete
]

# At each REQUIRED checkpoint:
def handle_required_checkpoint(checkpoint_id):
    1. STOP all execution
    2. Present options with VS alternatives
    3. Use AskUserQuestion tool
    4. WAIT for explicit approval
    5. Log decision to decision-log.yaml
    6. ONLY THEN proceed to next stage
```

### RECOMMENDED Checkpoints (🟠) - System SHOULD STOP

```python
RECOMMENDED_CHECKPOINTS = [
    "CP_ANALYSIS_PLAN",         # Before analysis
    "CP_INTEGRATION_STRATEGY",  # Mixed methods integration
    "CP_QUALITY_REVIEW",        # Quality assessment results
]

# At each RECOMMENDED checkpoint:
def handle_recommended_checkpoint(checkpoint_id):
    1. PAUSE execution
    2. Present current state and ask for review
    3. If user wants to skip: allow with warning
    4. If user reviews: wait for approval
```

### OPTIONAL Checkpoints (🟡) - System ASKS

```python
OPTIONAL_CHECKPOINTS = [
    "CP_VISUALIZATION_PREFERENCE",
    "CP_RENDERING_METHOD",
]

# At each OPTIONAL checkpoint:
def handle_optional_checkpoint(checkpoint_id):
    1. Present options with defaults
    2. If no response in context: use default
    3. If user specifies: use preference
```

---

## Model Routing (Kept from v1.0)

Always pass `model` parameter explicitly:

```python
# HIGH tier agents - Complex reasoning
Task(
    subagent_type="general-purpose",
    model="opus",
    description="A2: Theoretical framework selection",
    prompt="..."
)

# MEDIUM tier agents - Standard tasks
Task(
    subagent_type="general-purpose",
    model="sonnet",
    description="B1: Literature search",
    prompt="..."
)

# LOW tier agents - Simple operations
Task(
    subagent_type="general-purpose",
    model="haiku",
    description="B3: Effect size extraction",
    prompt="..."
)
```

---

## Agent-Tier Quick Reference (27 Agents)

| Category | Agent ID | Name | Tier | Model |
|----------|----------|------|------|-------|
| **A: Foundation** | A1 | Research Question Refiner | HIGH | opus |
| | A2 | Theoretical Framework Architect | HIGH | opus |
| | A3 | Devil's Advocate | HIGH | opus |
| | A4 | Research Ethics Advisor | MEDIUM | sonnet |
| | A5 | Paradigm & Worldview Advisor | HIGH | opus |
| **B: Evidence** | B1 | Literature Review Strategist | MEDIUM | sonnet |
| | B2 | Evidence Quality Appraiser | MEDIUM | sonnet |
| | B3 | Effect Size Extractor | LOW | haiku |
| | B4 | Research Radar | LOW | haiku |
| **C: Design** | C1 | Quantitative Design Consultant | HIGH | opus |
| | C2 | Qualitative Design Consultant | HIGH | opus |
| | C3 | Mixed Methods Design Consultant | HIGH | opus |
| | C4 | Experimental Materials Developer | MEDIUM | sonnet |
| **D: Collection** | D1 | Sampling Strategy Advisor | MEDIUM | sonnet |
| | D2 | Interview & Focus Group Specialist | MEDIUM | sonnet |
| | D3 | Observation Protocol Designer | LOW | haiku |
| | D4 | Measurement Instrument Developer | HIGH | opus |
| **E: Analysis** | E1 | Quantitative Analysis Guide | HIGH | opus |
| | E2 | Qualitative Coding Specialist | MEDIUM | sonnet |
| | E3 | Mixed Methods Integration Specialist | HIGH | opus |
| | E4 | Analysis Code Generator | LOW | haiku |
| **F: Quality** | F1 | Internal Consistency Checker | LOW | haiku |
| | F2 | Checklist Manager | LOW | haiku |
| | F3 | Reproducibility Auditor | MEDIUM | sonnet |
| | F4 | Bias & Trustworthiness Detector | MEDIUM | sonnet |
| **G: Publication** | G1 | Journal Matcher | MEDIUM | sonnet |
| | G2 | Academic Communicator | MEDIUM | sonnet |
| | G3 | Peer Review Strategist | HIGH | opus |
| | G4 | Pre-registration Composer | MEDIUM | sonnet |
| **H: Specialized** | H1 | Ethnographic Research Advisor | HIGH | opus |
| | H2 | Action Research Facilitator | HIGH | opus |

---

## Example Orchestration (v2.0 Style)

### User: "AI 튜터 효과 연구 시작하고 싶어"

```
Step 1: Pattern Match
   └─ "연구" detected → Research initiation
   └─ Paradigm signal: likely quantitative

Step 2: 🔴 CP_PARADIGM_SELECTION (HALT)

   AI: "연구 맥락에서 양적 연구 접근이 감지되었습니다.
        다음 중 어떤 패러다임으로 진행하시겠습니까?

        [Q] 양적 연구 (Quantitative)
        [L] 질적 연구 (Qualitative)
        [M] 혼합 방법 (Mixed Methods)
        [?] 도움이 필요해요"

   ⏸️ WAIT FOR USER RESPONSE ⏸️

Step 3: User selects "Q"

Step 4: Route to A1 (HIGH/opus)
   └─ Execute: Research Question Refiner

Step 5: 🔴 CP_RESEARCH_DIRECTION (HALT)

   AI: "연구 질문 방향 옵션입니다:

        [A] 전체 효과 분석 (T=0.65) - 일반적
        [B] 하위요인별 효과 (T=0.40) - 차별화 ⭐
        [C] 개인차 조절효과 (T=0.25) - 혁신적

        어떤 방향으로 진행하시겠습니까?"

   ⏸️ WAIT FOR USER RESPONSE ⏸️

Step 6: User selects "B"

Step 7: Route to A2 + A3 (HIGH/opus)
   └─ Execute in parallel: Theory + Devil's Advocate

Step 8: 🔴 CP_THEORY_SELECTION (HALT)

   AI: "이론적 프레임워크 옵션입니다:

        [A] Guilford's 4-factor (T=0.55)
        [B] Kaufman's 4C Model (T=0.35)
        [C] Amabile's Component (T=0.40)

        어떤 프레임워크를 사용하시겠습니까?"

   ⏸️ WAIT FOR USER RESPONSE ⏸️

Step 9: Continue with user-approved choices...
```

---

## What Was Removed (vs v1.0)

### ❌ Autonomous Execution

```yaml
# REMOVED - These patterns no longer activate
ultrawork_trigger: null   # Was: "ulw" → max parallelism
ecomode_trigger: null     # Was: "eco" → token efficient
ralph_trigger: null       # Was: "ralph" → persist until done
autopilot_trigger: null   # Was: → full autonomous
```

### ❌ Checkpoint Bypass

```yaml
# REMOVED - Checkpoints can no longer be bypassed
sisyphus_protocol: null
iron_law_continuation: null
checkpoint_skip_on_context: null
```

### ✅ What Remains

```yaml
# KEPT - Still functional
model_routing: enabled
agent_specialization: enabled
parallel_execution: enabled_between_checkpoints_only
context_persistence: enabled
vs_methodology: enabled
```

---

## Configuration Files

| File | Path | Purpose |
|------|------|---------|
| Project State | `.research/project-state.yaml` | Current project context |
| Decision Log | `.research/decision-log.yaml` | All human decisions |
| Checkpoint Config | `.research/checkpoints.yaml` | Checkpoint definitions |

---

## Key Principle: Ask, Don't Assume

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   ❌ WRONG: "다음 단계로 진행하겠습니다."                  │
│                                                            │
│   ✅ RIGHT: "다음 단계로 진행해도 될까요?                  │
│              [Y] 네 / [N] 아니요 / [?] 다른 옵션"          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```
