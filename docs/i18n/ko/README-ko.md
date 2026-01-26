# Diverga 🌟

**Beyond Modal: 창의적으로 생각하는 AI 연구 어시스턴트**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-6.0.1-brightgreen)](https://github.com/HosungYou/Diverga)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai/code)
[![VS Methodology](https://img.shields.io/badge/VS-Verbalized%20Sampling-green)](https://arxiv.org/abs/2510.01171)

---

## 🌟 왜 "Diverga"인가? Mode Collapse에서 벗어나기

대부분의 AI 연구 어시스턴트는 **mode collapse** 문제를 겪습니다 - 항상 같은 뻔한 옵션만 추천합니다:

> ❌ "기술 채택 연구에는 TAM을 추천합니다." (매번 똑같음)
> ❌ "메타분석에는 랜덤 효과 모형을 사용하세요." (항상 같은 답)
> ❌ "질적 연구에는 주제 분석을 시도해보세요." (뻔한 선택)

**Diverga는 다릅니다.** **Verbalized Sampling (VS) 방법론** (arXiv:2510.01171)을 기반으로 mode collapse를 능동적으로 방지하고 **창의적이면서도 방어 가능한 연구 선택**으로 안내합니다.

---

## ✨ v6.0 (Human-Centered Edition)

### 핵심 원칙

> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**

### v6.0의 새로운 점

| 기능 | 설명 |
|------|------|
| **🔴 필수 체크포인트** | AI가 중요한 결정 지점에서 멈추고 기다림 |
| **33개 전문 에이전트** | 27개에서 33개로 확장, 카테고리 기반 명명 (A1-H2) |
| **인간 중심 설계** | 모든 주요 결정에 명시적 인간 승인 필요 |
| **깔끔한 아키텍처** | `.claude/` 아래 단순화된 폴더 구조 |

### 제거된 기능

| 제거됨 | 이유 |
|--------|------|
| ❌ Sisyphus 프로토콜 | 인간 체크포인트를 우회할 수 있었음 |
| ❌ Iron Law | "OR"이 체크포인트를 선택적으로 만들었음 |
| ❌ OMC 자율 모드 | ralph/ultrawork/ecomode가 우회를 가능하게 함 |

---

## 🎯 Human Checkpoint 시스템

### 체크포인트 수준

| 수준 | 아이콘 | 동작 |
|------|--------|------|
| **필수** | 🔴 | 시스템 정지 - 명시적 승인 없이 진행 불가 |
| **권장** | 🟠 | 시스템 일시정지 - 승인 강력 권장 |
| **선택** | 🟡 | 시스템 질문 - 건너뛰면 기본값 사용 |

### 필수 체크포인트

| 체크포인트 | 시점 | 내용 |
|-----------|------|------|
| CP_RESEARCH_DIRECTION | 연구 질문 확정 | VS 옵션 제시, 선택 대기 |
| CP_PARADIGM_SELECTION | 방법론 접근 | 양적/질적/혼합 질문 |
| CP_THEORY_SELECTION | 프레임워크 선택 | T-Score와 함께 대안 제시 |
| CP_METHODOLOGY_APPROVAL | 설계 완료 | 상세 검토 필요 |

---

## 🧠 핵심 혁신: Verbalized Sampling (VS) 방법론

### 문제: Modal 추천

AI 시스템은 통계적으로 가장 흔한 옵션 - **modal 추천**을 권장하는 경향이 있습니다:
- 획일화된 연구 지형
- 혁신적 기회 상실
- 연구의 차별화 어려움

### 해결책: Dynamic T-Score 시스템

| T-Score | 해석 | Diverga 행동 |
|---------|------|--------------|
| `T > 0.8` | **Modal** (가장 흔함) | ⚠️ "예측 가능함" 표시 |
| `T 0.5-0.8` | **확립된 대안** | ✅ 균형 잡힌 선택으로 제안 |
| `T 0.3-0.5` | **신흥 접근법** | ✅ 혁신을 위해 추천 |
| `T < 0.3` | **새로운/창의적** | 🔬 강력한 근거와 함께 제시 |

### VS 실제 적용

```
❌ VS 없이 (Mode Collapse):
   사용자: "AI 채택 연구를 위한 이론적 프레임워크 선택을 도와주세요"
   AI: "기술수용모델(TAM)을 추천합니다."
   (매번 같은 답, T=0.92)

✅ VS 적용 (Diverga):
   사용자: "AI 채택 연구를 위한 이론적 프레임워크 선택을 도와주세요"

   🔴 CHECKPOINT: CP_THEORY_SELECTION

   Diverga: "전형성 스펙트럼에 걸쳐 옵션을 분석합니다:

   [Modal 인식] TAM (T=0.92)과 UTAUT (T=0.85)은 예측 가능한 선택입니다.

   추천 옵션:
   • 방향 A (T≈0.6): 자기결정이론 × TAM 통합
   • 방향 B (T≈0.4): 인지부하이론 + 적응형 생태계 ⭐
   • 방향 C (T≈0.2): 신경가소성 기반 기술 학습

   어떤 방향으로 진행하시겠습니까?"
   (인간 선택 대기)
```

---

## 🏗️ 아키텍처 (8개 카테고리 33개 에이전트)

### Category A: Foundation (6개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| A1-research-question-refiner | Opus | FINER/PICO/SPIDER 프레임워크 |
| A2-theoretical-framework-architect | Opus | VS를 통한 이론 선택 |
| A3-devils-advocate | Opus | 비판적 평가 |
| A4-research-ethics-advisor | Sonnet | IRB, 윤리적 고려 |
| A5-paradigm-worldview-advisor | Opus | 양적/질적/혼합 안내 |
| A6-conceptual-framework-visualizer | Sonnet | 시각적 프레임워크 설계 |

### Category B: Evidence (4개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| B1-systematic-literature-scout | Sonnet | PRISMA/질적 검색 |
| B2-evidence-quality-appraiser | Sonnet | RoB, GRADE 평가 |
| B3-effect-size-extractor | Haiku | 효과크기 계산 |
| B4-research-radar | Haiku | 트렌드 모니터링 |

### Category C: Design (4개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| C1-quantitative-design-consultant | Opus | 실험, 조사 설계 |
| C2-qualitative-design-consultant | Opus | 현상학, GT, 사례연구 |
| C3-mixed-methods-design-consultant | Opus | 순차적, 수렴적 |
| C4-experimental-materials-developer | Sonnet | 처치 자료 |

### Category D: Data Collection (4개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| D1-sampling-strategy-advisor | Sonnet | 확률/의도적 표집 |
| D2-interview-focus-group-specialist | Sonnet | 프로토콜, 전사 |
| D3-observation-protocol-designer | Haiku | 현장 노트 |
| D4-measurement-instrument-developer | Opus | 척도 구성 |

### Category E: Analysis (5개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| E1-quantitative-analysis-guide | Opus | 통계 분석 |
| E2-qualitative-coding-specialist | Opus | 주제, GT 코딩 |
| E3-mixed-methods-integration | Opus | Joint display, 메타 추론 |
| E4-analysis-code-generator | Haiku | R/Python/NVivo 코드 |
| E5-sensitivity-analysis-designer | Sonnet | 강건성 검증 |

### Category F: Quality (4개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| F1-internal-consistency-checker | Haiku | 내적 타당도 |
| F2-checklist-manager | Haiku | PRISMA/CONSORT/COREQ |
| F3-reproducibility-auditor | Sonnet | Open Science |
| F4-bias-trustworthiness-detector | Sonnet | 편향 탐지 |

### Category G: Communication (4개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| G1-journal-matcher | Sonnet | 타겟 저널 선정 |
| G2-academic-communicator | Sonnet | 청중 맞춤 |
| G3-peer-review-strategist | Opus | 리뷰 대응 |
| G4-preregistration-composer | Sonnet | OSF/AsPredicted |

### Category H: Specialized (2개)
| 에이전트 | 모델 | 목적 |
|---------|------|------|
| H1-ethnographic-research-advisor | Opus | 현장 연구, 두꺼운 기술 |
| H2-action-research-facilitator | Opus | PAR, CBPR 사이클 |

---

## 🚀 시작하기

### 설치

```bash
git clone https://github.com/HosungYou/Diverga.git
cd Diverga
```

### 사용법

**자연어**:
```
"AI 교육에 대한 체계적 리뷰를 하고 싶어요"
"메타분석 연구를 시작하고 싶어요"
"실험 연구 설계를 도와주세요"
```

시스템은:
1. 패러다임 감지
2. **확인 요청** (🔴 CHECKPOINT)
3. T-Score와 함께 VS 대안 제시
4. **선택 대기**
5. 체크포인트와 함께 파이프라인 안내

---

## 🔗 통합 허브

### 기본 제공 (설정 불필요)
| 도구 | 용도 |
|------|------|
| Excel | 데이터 추출, 코딩 시트 |
| PowerPoint | 학회 발표 |
| Word | 원고, 방법론 섹션 |
| Python | 분석 스크립트 |
| Mermaid | 플로우 다이어그램 |

### 설정 필요
| 도구 | 목적 |
|------|------|
| Semantic Scholar | 문헌 검색 |
| OpenAlex | 오픈 액세스 검색 |
| Zotero MCP | 참고문헌 관리 |
| R Scripts | 통계 분석 |

---

## 🌐 다국어 지원

Diverga는 **한국어와 영어**를 완벽히 지원합니다:

```
English: "I want to conduct a systematic review"
한국어: "체계적 문헌고찰을 하고 싶어요"
혼합: "메타분석을 하려는데, can you help?"
```

---

## 📚 문서

| 문서 | 설명 |
|------|------|
| [CLAUDE.md](../../CLAUDE.md) | 전체 시스템 문서 |
| [AGENTS.md](../../AGENTS.md) | 33개 에이전트 상세 참조 |
| [Quick Start](../QUICKSTART.md) | 5분 안에 시작하기 |

---

## 📄 라이선스

MIT License - [LICENSE](../../LICENSE) 참조

---

## 📖 인용

```bibtex
@software{diverga,
  author = {You, Hosung},
  title = {Diverga: Beyond Modal AI Research Assistant},
  year = {2026},
  version = {6.0.1},
  url = {https://github.com/HosungYou/Diverga},
  note = {VS 방법론과 Human-Centered 설계를 갖춘 33개 에이전트. Verbalized Sampling (arXiv:2510.01171)을 통한 mode collapse 방지}
}
```

---

**Made with 🌟 for Social Science Researchers**

*Diverga: 창의성과 엄밀함이 만나는 곳. 뻔한 것을 넘어, 혁신을 향해.*
