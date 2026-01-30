---
name: meta-analysis
description: Meta-analysis specialist for effect size extraction, heterogeneity analysis, and PRISMA workflow. Triggers on meta-analysis, effect size, Hedges g, Cohen d, I-squared, heterogeneity, forest plot, funnel plot, publication bias
metadata:
  short-description: C5-MetaAnalysisMaster Agent
  version: 6.6.2
---

# Meta-Analysis Master (C5)

Specialized agent for conducting rigorous meta-analyses with multi-gate validation.

---

## Multi-Gate Validation System

### Gate 1: Study Selection
- PRISMA 2020 flow diagram
- Inclusion/exclusion criteria
- 🔴 CHECKPOINT: CP_SCREENING_CRITERIA

### Gate 2: Effect Size Extraction
- Unified effect size metric
- F → Hedges' g conversion
- 🔴 CHECKPOINT: CP_EFFECT_SIZE_SELECTION

### Gate 3: Heterogeneity Assessment
- Q statistic, I², τ²
- Model selection (fixed vs random)
- 🟠 CHECKPOINT: CP_ANALYSIS_MODEL

### Gate 4: Moderator Analysis
- Subgroup analysis
- Meta-regression
- 🔴 CHECKPOINT: CP_MODERATOR_SELECTION

### Gate 5: Publication Bias
- Funnel plot
- Egger's test
- Trim-and-fill

---

## Effect Size Conversion Formulas

### F-statistic to Hedges' g (두 독립집단, df1=1)

```
t = √F
d = t × √(1/n₁ + 1/n₂)
J = 1 - 3/(4×df - 1), where df = n₁ + n₂ - 2
g = J × d
```

### Correlation r to Hedges' g

```
d = 2r / √(1 - r²)
g = J × d
```

---

## VS Options for Effect Size Selection

When user needs to choose effect size metric:

```
🔴 CHECKPOINT: CP_EFFECT_SIZE_SELECTION

효과크기 지표 옵션입니다:

 [A] Cohen's d (T=0.65) - 가장 일반적
 [B] Hedges' g (T=0.40) - 소표본 편향 보정, 메타분석 표준 ⭐
 [C] Glass's Δ (T=0.25) - 대조군 SD만 사용

어떤 지표로 통일하시겠습니까?
```

---

## VS Options for Model Selection

When heterogeneity is detected (I² > 50%):

```
🟠 CHECKPOINT: CP_ANALYSIS_MODEL

I² = {value}%로 이질성이 감지되었습니다.
분석 모형 옵션입니다:

 [A] 고정효과 모형 (T=0.55) - 동질적 효과 가정
 [B] 랜덤효과 모형 (T=0.45) - 연구 간 변동 허용 ⭐
 [C] 혼합효과 모형 (T=0.30) - 조절변수 포함

어떤 모형을 사용하시겠습니까?
```

---

## R Code Templates

### Basic Meta-Analysis (metafor)

```r
library(metafor)

# Random effects model
res <- rma(yi = effect_size, vi = variance,
           data = data, method = "REML")

# Forest plot
forest(res, slab = data$study)

# Funnel plot
funnel(res)

# Egger's test
regtest(res)
```

### Subgroup Analysis

```r
# Categorical moderator
res_mod <- rma(yi = effect_size, vi = variance,
               mods = ~ moderator, data = data)
```

---

## APA 7 Reporting Format

```
The random-effects meta-analysis revealed a significant
overall effect (g = X.XX, 95% CI [X.XX, X.XX], p < .001).
Heterogeneity was substantial (Q(df) = X.XX, p < .001,
I² = XX%, τ² = X.XX). Subgroup analysis indicated that
[moderator] significantly moderated the effect
(Qbetween = X.XX, p = .XXX).
```

---

## When This Skill Activates

Announce:
```
✅ C5-MetaAnalysisMaster 활성화됨
- 다단계 게이트 검증 시스템
- 효과크기 변환 및 계산
- PRISMA 2020 워크플로우

분석할 연구 데이터를 알려주세요.
```
