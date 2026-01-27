# Diverga v6.5.0: Task Tool Agent Implementation Report

**Date**: 2026-01-27
**Author**: Claude Code
**Status**: 구현 완료 - 재설치 필요

---

## 작업 요약

oh-my-claudecode와 동일한 방식으로 Diverga 에이전트를 Task tool로 호출할 수 있도록 `/agents/` 디렉토리를 생성했습니다.

## 생성된 파일

### `/agents/` 디렉토리 구조

```
/Volumes/External SSD/Projects/Research/Diverga/agents/
├── a1.md    # Research Question Refiner
├── a2.md    # Theoretical Framework Architect
├── a3.md    # Devil's Advocate
├── a4.md    # Research Ethics Advisor
├── a5.md    # Paradigm & Worldview Advisor
├── a6.md    # Conceptual Framework Visualizer
├── b1.md    # Systematic Literature Scout
├── b2.md    # Evidence Quality Appraiser
├── b3.md    # Effect Size Extractor
├── b4.md    # Research Radar
├── b5.md    # Parallel Document Processor
├── c1.md    # Quantitative Design Consultant
├── c2.md    # Qualitative Design Consultant
├── c3.md    # Mixed Methods Design Consultant
├── c4.md    # Experimental Materials Developer
├── c5.md    # Meta-Analysis Master
├── c6.md    # Data Integrity Guard
├── c7.md    # Error Prevention Engine
├── d1.md    # Sampling Strategy Advisor
├── d2.md    # Interview & Focus Group Specialist
├── d3.md    # Observation Protocol Designer
├── d4.md    # Measurement Instrument Developer
├── e1.md    # Quantitative Analysis Guide
├── e2.md    # Qualitative Coding Specialist
├── e3.md    # Mixed Methods Integration
├── e4.md    # Analysis Code Generator
├── e5.md    # Sensitivity Analysis Designer
├── f1.md    # Internal Consistency Checker
├── f2.md    # Checklist Manager
├── f3.md    # Reproducibility Auditor
├── f4.md    # Bias & Trustworthiness Detector
├── f5.md    # Humanization Verifier
├── g1.md    # Journal Matcher
├── g2.md    # Academic Communicator
├── g3.md    # Peer Review Strategist
├── g4.md    # Pre-registration Composer
├── g5.md    # Academic Style Auditor
├── g6.md    # Academic Style Humanizer
├── h1.md    # Ethnographic Research Advisor
└── h2.md    # Action Research Facilitator
```

**총: 40개 에이전트 파일**

## 파일 형식 (oh-my-claudecode 호환)

각 에이전트 파일은 YAML frontmatter + Markdown 내용으로 구성:

```markdown
---
name: a1
description: VS-Enhanced Research Question Refiner - Prevents Mode Collapse
model: opus
tools: Read, Glob, Grep, WebSearch
---

# Research Question Refiner

**Agent ID**: A1
**Category**: A - Theory & Design
**VS Level**: Enhanced (3-Phase)
**Tier**: HIGH (Opus)

## Overview
...

## Human Checkpoint Protocol
...
```

## 에이전트 모델 및 티어 배분

| Model | Tier | Count | Agents |
|-------|------|-------|--------|
| opus | HIGH | 16 | a1, a2, a3, a5, b5, c1, c2, c3, c5, d4, e1, e2, e3, g6, h1, h2 |
| sonnet | MEDIUM | 17 | a4, a6, b1, b2, c4, c6, c7, d1, d2, e5, f3, f4, g1, g2, g3, g4, g5 |
| haiku | LOW | 7 | b3, b4, d3, e4, f1, f2, f5 |

## 현재 상태

### 완료된 작업

1. ✅ 40개 에이전트 `.md` 파일 생성 (`/agents/`)
2. ✅ oh-my-claudecode 형식과 동일한 YAML frontmatter
3. ✅ 플러그인 캐시에 복사 완료

### 미완료 작업

Task tool에서 `diverga:a1` 등의 에이전트를 찾지 못하는 상태:

```
Error: Agent type 'diverga:a1' not found.
```

## 원인 분석

Claude Code는 플러그인 설치 시점에 `/agents/` 디렉토리를 스캔하여 Task tool 에이전트를 등록합니다. 현재 캐시 디렉토리에 파일을 복사했지만, 이는 플러그인 등록 시스템에 반영되지 않습니다.

### oh-my-claudecode가 작동하는 이유

1. 원본 GitHub 저장소에 `/agents/` 디렉토리가 존재
2. 플러그인 설치 시 Claude Code가 해당 디렉토리를 스캔
3. 에이전트가 `oh-my-claudecode:architect` 형식으로 등록됨

### Diverga가 작동하지 않는 이유

1. 원본 GitHub 저장소에 `/agents/` 디렉토리가 없었음
2. 플러그인 설치 당시 에이전트 등록 안됨
3. 캐시에 파일을 추가해도 등록 시스템에 반영 안됨

## 해결 방법

### 단기 해결책 (즉시 적용 가능)

Skill tool을 통한 호출은 정상 작동:

```
/diverga:A1-research-question-refiner
```

### 장기 해결책 (GitHub 반영 필요)

1. `/agents/` 디렉토리를 GitHub에 커밋
2. 버전을 6.5.0으로 업데이트
3. 플러그인 재설치

```bash
# 1. 커밋
git add agents/
git commit -m "Add /agents/ directory for Task tool support"
git push

# 2. 재설치
/plugin reinstall diverga
```

재설치 후 사용 가능:

```python
Task(
    subagent_type="diverga:a1",
    model="opus",
    prompt="연구 질문 정제 요청..."
)
```

## Skill vs Task 호출 비교

| 방식 | 호출 예시 | 현재 상태 |
|------|----------|----------|
| **Skill** | `/diverga:A1-research-question-refiner` | ✅ 작동 |
| **Task** | `Task(subagent_type="diverga:a1")` | ❌ 재설치 필요 |

## 향후 작업

1. [ ] `/agents/` 디렉토리를 GitHub 저장소에 푸시
2. [ ] `marketplace.json` 버전을 6.5.0으로 업데이트
3. [ ] README.md에 Task tool 사용법 추가
4. [ ] 플러그인 재설치 후 테스트
5. [ ] 병렬 실행 테스트 (3개 에이전트 동시 호출)

---

## 참고: TypeScript Runtime

이전에 구현한 TypeScript runtime (`/src/agents/`)은 프로그래밍 방식의 에이전트 접근을 위한 것으로, Task tool 등록과는 별개입니다:

```typescript
import { getAgentDefinitions, getAgent } from 'diverga';

// 프로그래매틱 사용
const agents = getAgentDefinitions();
const a1 = getAgent('a1');
```

---

**결론**: `/agents/` 디렉토리 생성 완료. GitHub 푸시 및 플러그인 재설치 후 Task tool 사용 가능.
