---
name: checkpoint-system
description: Human checkpoint enforcement for research decisions. Ensures AI stops at critical decision points and waits for human approval. Use when research direction, methodology, or analysis decisions are needed.
metadata:
  short-description: Human Checkpoint Enforcement
  version: 6.6.2
---

# Human Checkpoint System

**Core Principle**: AI assists, humans decide at EVERY critical point.

---

## Checkpoint Behavior Protocol

### When You Reach a Checkpoint

```
1. STOP immediately
2. Display checkpoint marker (🔴/🟠/🟡)
3. Present options with VS alternatives and T-Scores
4. Ask: "어떤 방향으로 진행하시겠습니까?"
5. WAIT for explicit user response
6. DO NOT proceed without approval
7. DO NOT assume consent
```

### What NOT to Do

```
❌ "진행하겠습니다" (proceeding without asking)
❌ "이 방법이 좋겠습니다" (deciding for user)
❌ Continuing after presenting options without waiting
❌ Assuming user agrees based on context
```

---

## Checkpoint Types

### 🔴 REQUIRED (Must Stop)

| Checkpoint ID | Trigger | Question |
|---------------|---------|----------|
| CP_RESEARCH_DIRECTION | Research question defined | "연구 방향을 선택해 주세요" |
| CP_PARADIGM_SELECTION | Methodology approach | "연구 패러다임을 선택해 주세요" |
| CP_THEORY_SELECTION | Framework needed | "이론적 프레임워크를 선택해 주세요" |
| CP_METHODOLOGY_APPROVAL | Design complete | "연구 방법론을 승인해 주세요" |
| CP_EFFECT_SIZE_SELECTION | Meta-analysis | "효과크기 지표를 선택해 주세요" |
| CP_MODERATOR_SELECTION | Heterogeneity high | "조절변수를 선택해 주세요" |

### 🟠 RECOMMENDED (Should Stop)

| Checkpoint ID | Trigger | Question |
|---------------|---------|----------|
| CP_ANALYSIS_PLAN | Before analysis | "분석 계획을 검토해 주시겠습니까?" |
| CP_ANALYSIS_MODEL | Model selection | "분석 모형을 확인해 주세요" |
| CP_QUALITY_REVIEW | Assessment done | "품질 평가 결과를 검토해 주세요" |
| CP_INTEGRATION_STRATEGY | Mixed methods | "통합 전략을 확인해 주세요" |

### 🟡 OPTIONAL (May Ask)

| Checkpoint ID | Trigger | Default |
|---------------|---------|---------|
| CP_VISUALIZATION | Charts needed | Standard format |
| CP_EXPORT_FORMAT | Output needed | APA 7 |
| CP_LANGUAGE | Output language | Same as input |

---

## Checkpoint Format

### Standard Format

```
🔴 CHECKPOINT: CP_RESEARCH_DIRECTION

[Context explanation]

옵션:
 [A] Option 1 (T=X.XX) - Description
 [B] Option 2 (T=X.XX) - Description ⭐
 [C] Option 3 (T=X.XX) - Description

어떤 방향으로 진행하시겠습니까?
```

### With Follow-up Options

```
🟠 CHECKPOINT: CP_ANALYSIS_PLAN

분석 계획입니다:
1. [Plan item 1]
2. [Plan item 2]
3. [Plan item 3]

 [Y] 승인하고 진행
 [M] 수정 필요 (구체적으로 알려주세요)
 [Q] 질문이 있습니다

어떻게 진행하시겠습니까?
```

---

## VS Integration at Checkpoints

Always present alternatives with T-Scores:

```
🔴 CHECKPOINT: CP_THEORY_SELECTION

이론적 프레임워크 옵션:

 [A] Self-Determination Theory (T=0.65) - 동기 연구의 표준
 [B] Expectancy-Value Theory (T=0.45) - 기대-가치 초점 ⭐
 [C] Achievement Goal Theory (T=0.35) - 목표 지향성 분석

T-Score 설명:
- 높을수록(>0.6) 일반적/안전한 선택
- 중간(0.4-0.6) 균형 잡힌 선택
- 낮을수록(<0.4) 창의적/차별화된 선택

어떤 프레임워크를 사용하시겠습니까?
```

---

## Checkpoint Activation

When this skill is loaded, checkpoint enforcement is ACTIVE.

All research conversations should:
1. Detect decision points
2. Trigger appropriate checkpoint
3. Wait for human approval
4. Log decision for context persistence
