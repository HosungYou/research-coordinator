# Changelog

All notable changes to Research Coordinator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2025-01-24

### 🎯 Major Release: VS-Research v3.0

이 릴리스는 Verbalized Sampling 방법론의 대대적인 업그레이드입니다. Dynamic T-Score 시스템, 5가지 창의적 장치, 14개 User Checkpoints를 도입하여 Mode Collapse 방지 기능을 크게 강화했습니다.

### Added

#### Core Infrastructure
- **VS Engine v3.0** (`core/vs-engine.md`)
  - 5단계 VS 프로세스 정의
  - 창의적 장치 통합 인터페이스
  - User Checkpoint 트리거 시스템

- **Dynamic T-Score System** (`core/t-score-dynamics.md`)
  - 맥락 기반 동적 임계값 조정
  - 연구 유형별 T-Score 프로필 (탐색적/확인적/혁신적)
  - 권장 함수: `recommend(context) → (option, t_score, justification)`

#### Interaction System
- **14개 User Checkpoints** (`interaction/user-checkpoints.md`)
  - CP-INIT-001/002: 초기 맥락 및 목표 확인
  - CP-VS-001/002/003: VS 프로세스 단계별 확인
  - CP-FA-001: 강제 비유 적용 후 확인
  - CP-IL-001/002/003: 반복 루프 진행 확인
  - CP-SD-001: 의미적 거리 이동 확인
  - CP-TR-001: 시간 재구성 확인
  - CP-CS-001: 커뮤니티 시뮬레이션 확인
  - CP-FINAL-001: 최종 결정 전 확인

#### 5 Creativity Mechanisms
| 장치 | 파일 | 설명 |
|------|------|------|
| Forced Analogy | `creativity/forced-analogy.md` | 원거리 분야에서 비유 차용 |
| Iterative Loop | `creativity/iterative-loop.md` | 3-5회 발산-수렴 반복 |
| Semantic Distance | `creativity/semantic-distance.md` | 의미적으로 먼 개념 탐색 |
| Temporal Reframing | `creativity/temporal-reframing.md` | 시간축 재구성 (과거/미래 관점) |
| Community Simulation | `creativity/community-simulation.md` | 가상 연구자 커뮤니티 대화 |

#### Reference Documents
- `references/vs-quick-reference.md`: VS 방법론 빠른 참조
- `references/upgrade-matrix.md`: 에이전트별 업그레이드 매트릭스

### Changed

#### 3-Tier Agent Upgrade
모든 20개 에이전트가 v3.0으로 업그레이드되었습니다:

| Level | Agents | 창의적 장치 | Checkpoints |
|-------|--------|------------|-------------|
| **FULL** | 02, 03, 05, 10, 16 (5개) | 5개 모두 | 전체 |
| **ENHANCED** | 01, 04, 06, 07, 08, 09 (6개) | 3개 (FA, IL, SD) | 부분 |
| **LIGHT** | 11-15, 17-20 (9개) | 없음 | 기본 (2개) |

#### Agent SKILL.md Updates
- 모든 에이전트 frontmatter에 `version: 3.0.0` 추가
- `upgrade_level` 필드 추가 (FULL/ENHANCED/LIGHT)
- `v3_integration` 블록 추가:
  ```yaml
  v3_integration:
    dynamic_t_score: true/false
    creativity_modules: [list]
    checkpoints: [list]
  ```
- FULL/ENHANCED 에이전트에 "v3.0 창의적 장치 통합" 섹션 추가

#### Master Coordinator
- `agent-registry.yaml` 업데이트 (v3.0 메타데이터)
- Master SKILL.md에 VS Engine 참조 추가
- 창의적 장치 자동 활성화 로직 추가

### Technical Details

#### Directory Structure (New)
```
.claude/skills/research-coordinator/
├── SKILL.md                    # Master skill (updated)
├── core/
│   ├── vs-engine.md            # NEW: VS Engine v3.0
│   └── t-score-dynamics.md     # NEW: Dynamic T-Score
├── interaction/
│   └── user-checkpoints.md     # NEW: 14 checkpoints
├── creativity/
│   ├── forced-analogy.md       # NEW
│   ├── iterative-loop.md       # NEW
│   ├── semantic-distance.md    # NEW
│   ├── temporal-reframing.md   # NEW
│   └── community-simulation.md # NEW
└── references/
    ├── vs-quick-reference.md   # NEW
    └── upgrade-matrix.md       # NEW
```

#### Commit History (20 commits)
```
97c500e docs(readme): update to v3.0.0
3831eba chore(scripts): update install.sh for v3.0.0
ce796a0 chore(marketplace): bump version to v3.0.0
76328be feat(agents): upgrade 9 LIGHT VS agents to v3.0
be95ce2 feat(agents): upgrade 6 ENHANCED VS agents to v3.0
28d188d feat(agents): upgrade 5 FULL VS agents to v3.0
96dd69a feat: upgrade master SKILL.md to v3.0
b7e7894 feat(registry): update agent registry for v3.0
bb96a36 docs(references): add v3.0 specification documents
f7a49f8 feat(creativity): add community simulation mechanism
4e312ba feat(creativity): add temporal reframing mechanism
18c9732 feat(creativity): add semantic distance scorer
e4ecda9 feat(creativity): add iterative divergent-convergent loop
dee6766 feat(creativity): add forced analogy mechanism
9aba9ad feat(interaction): add comprehensive user checkpoint system
21899c3 feat(core): add dynamic T-Score system
4981c2a feat(core): add VS Engine v3.0
1b984df chore: create v3.0 modular directory structure
0fe386a docs: Add v3.0 detailed implementation plan
e85e05d docs: Add v3.0 design document and analysis report
```

### Migration Guide

#### From 2.x to 3.0.0

```bash
# 마켓플레이스 업데이트
claude plugin marketplace update research-coordinator-skills

# 플러그인 업데이트
claude plugin update research-coordinator
```

로컬 설치 사용자:
```bash
cd /path/to/research-coordinator
git pull origin main
./scripts/install.sh
```

### Breaking Changes
- 없음. 모든 기존 명령어와 트리거가 동일하게 작동합니다.
- 새로운 기능은 자동으로 활성화됩니다.

---

## [2.1.0] - 2025-01-23

### Changed
- **Single plugin, all skills**: `research-coordinator` 플러그인 하나에 21개 스킬 모두 포함
- 설치 방법 대폭 간소화 (2줄로 완료)
- marketplace.json 구조 변경 (Anthropic document-skills 패턴 적용)

### Technical Details
```json
// Before: 21개 개별 플러그인
"plugins": [
  { "name": "research-coordinator", "skills": ["./"] },
  { "name": "01-research-question-refiner", "skills": ["./"] },
  ...
]

// After: 1개 플러그인에 21개 스킬 포함
"plugins": [
  {
    "name": "research-coordinator",
    "source": "./",
    "skills": [
      "./.claude/skills/research-coordinator",
      "./.claude/skills/research-agents/01-research-question-refiner",
      ... (19개 더)
    ]
  }
]
```

### Installation (v2.1.0+)
```bash
claude plugin marketplace add HosungYou/research-coordinator
claude plugin install research-coordinator  # 21개 스킬 모두 설치됨
```

---

## [2.0.1] - 2025-01-23

### Fixed
- marketplace.json 스키마 오류 수정
- Claude Code marketplace 호환성 확보

### Added
- `$schema` 참조 추가
- 각 플러그인에 `source` 필드 추가 (필수)
- 각 플러그인에 `strict: false` 추가
- 일괄 설치 스크립트 (`scripts/install-all-plugins.sh`)

### Technical Details
- 이전: `skills` 배열만 사용 → 스키마 오류
- 이후: `source` + `skills: ["./"]` 구조로 변경

---

## [2.0.0] - 2025-01-22

### Added
- **Verbalized Sampling (VS) 방법론** 통합
  - arXiv:2510.01171 기반 Mode Collapse 방지
  - T-Score (Typicality Score) 시스템
- VS 적용 수준 3단계
  - **Full VS**: 에이전트 02, 03, 05, 10, 16 (5단계 전체 프로세스)
  - **Enhanced VS**: 에이전트 01, 04, 06, 07, 08, 09 (3단계 간소화)
  - **Light VS**: 에이전트 11-15, 17-20 (모달 인식 + 대안 제시)

### Changed
- 모든 에이전트 SKILL.md에 VS 방법론 섹션 추가
- 추천 시 T-Score 범위 명시
- 모달(가장 흔한) 선택 회피 로직 내장

### Agents with Full VS
| ID | Agent | VS Feature |
|----|-------|------------|
| 02 | Theoretical Framework Architect | 이론 추천 시 TAM/UTAUT 등 모달 회피 |
| 03 | Devil's Advocate | 비판 관점 다양화 |
| 05 | Systematic Literature Scout | 검색 전략 차별화 |
| 10 | Statistical Analysis Guide | 분석 방법 대안 제시 |
| 16 | Bias Detector | 편향 유형 포괄적 탐지 |

---

## [1.0.0] - 2025-01-22

### Added
- 초기 릴리스
- 20개 전문 연구 에이전트
- 마스터 코디네이터 (자동 디스패치)
- 5개 카테고리 구성
  - A: 이론 및 연구 설계 (01-04)
  - B: 문헌 및 증거 (05-08)
  - C: 방법론 및 분석 (09-12)
  - D: 품질 및 검증 (13-16)
  - E: 출판 및 커뮤니케이션 (17-20)

### Features
- 맥락 인식 자동 에이전트 활성화
- 트리거 키워드 시스템
- 한국어/영어 이중 언어 지원
- Claude Code Skills 시스템 통합

---

## Version History Summary

| Version | Date | Key Changes |
|---------|------|-------------|
| 3.0.0 | 2025-01-24 | **VS-Research v3.0**: Dynamic T-Score, 5 Creativity Mechanisms, 14 User Checkpoints |
| 2.1.0 | 2025-01-23 | Single plugin with all 21 skills |
| 2.0.1 | 2025-01-23 | Marketplace schema fix |
| 2.0.0 | 2025-01-22 | VS methodology integration |
| 1.0.0 | 2025-01-22 | Initial release |

---

## Upgrading

### From 2.0.x to 2.1.0

```bash
# 기존 개별 플러그인 제거 (있는 경우)
claude plugin uninstall research-coordinator
claude plugin uninstall 01-research-question-refiner
# ... (기타 개별 플러그인)

# 마켓플레이스 업데이트
claude plugin marketplace update research-coordinator-skills

# 새 통합 플러그인 설치
claude plugin install research-coordinator
```

### From 1.x to 2.x

```bash
# 로컬 설치 사용자
cd /path/to/research-coordinator
git pull origin main

# 마켓플레이스 사용자
claude plugin marketplace update research-coordinator-skills
claude plugin update research-coordinator
```
