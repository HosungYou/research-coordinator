# Checkpoint AskUserQuestion Templates

Reference file for exact AskUserQuestion parameters at each checkpoint.
When a checkpoint is reached, use the corresponding template below.

---

## 🔴 REQUIRED Checkpoints

### CP_RESEARCH_DIRECTION
```json
{
  "questions": [{
    "question": "연구 방향이 결정되었습니다. 이 방향으로 진행하시겠습니까? / Research direction confirmed. Shall we proceed?",
    "header": "Direction",
    "options": [
      {"label": "Approve / 승인", "description": "Proceed with the confirmed research direction"},
      {"label": "Modify / 수정", "description": "Revise the research question or scope before proceeding"},
      {"label": "Reconsider / 재고", "description": "Go back and explore different research directions"}
    ],
    "multiSelect": false
  }]
}
```

### CP_PARADIGM_SELECTION
```json
{
  "questions": [{
    "question": "연구 패러다임을 선택해 주세요. / Which research paradigm will you use?",
    "header": "Paradigm",
    "options": [
      {"label": "Quantitative / 양적", "description": "Hypothesis testing, statistical analysis, generalizability"},
      {"label": "Qualitative / 질적", "description": "Meaning-making, rich description, contextual understanding"},
      {"label": "Mixed Methods / 혼합", "description": "Integration of quantitative and qualitative approaches"}
    ],
    "multiSelect": false
  }]
}
```

### CP_THEORY_SELECTION
```json
{
  "questions": [{
    "question": "이론적 프레임워크를 선택해 주세요. / Please select your theoretical framework.",
    "header": "Theory",
    "options": [
      {"label": "Direction A", "description": "VS Option A - Safe but differentiated (T≈0.6)"},
      {"label": "Direction B", "description": "VS Option B - Balanced novelty (T≈0.4) ⭐"},
      {"label": "Direction C", "description": "VS Option C - Innovative approach (T<0.3)"}
    ],
    "multiSelect": false
  }]
}
```

### CP_METHODOLOGY_APPROVAL
```json
{
  "questions": [{
    "question": "연구 방법론 설계를 승인하시겠습니까? / Do you approve the research methodology design?",
    "header": "Methodology",
    "options": [
      {"label": "Approve / 승인", "description": "Approve the methodology and proceed to data collection"},
      {"label": "Revise / 수정", "description": "Request changes to the methodology design"},
      {"label": "Reject / 거부", "description": "Reject and redesign the methodology from scratch"}
    ],
    "multiSelect": false
  }]
}
```

### CP_VS_001 (VS Direction Selection)
```json
{
  "questions": [{
    "question": "어떤 방향으로 진행하시겠습니까? / Which VS direction would you like to proceed?",
    "header": "VS Choice",
    "options": [
      {"label": "Direction A", "description": "Safe differentiation (T≈0.6-0.7)"},
      {"label": "Direction B ⭐", "description": "Balanced novelty (T≈0.4) - Recommended"},
      {"label": "Direction C", "description": "Innovative/experimental (T<0.3)"}
    ],
    "multiSelect": false
  }]
}
```

### CP_VS_003 (VS Final Confirmation)
```json
{
  "questions": [{
    "question": "선택하신 방향으로 진행합니다. 확인하시겠습니까? / Proceeding with selected direction. Confirm?",
    "header": "Confirm",
    "options": [
      {"label": "Confirm / 확인", "description": "Proceed with the selected VS direction"},
      {"label": "Reconsider / 재고", "description": "Go back and choose a different direction"}
    ],
    "multiSelect": false
  }]
}
```

### SCH_DATABASE_SELECTION
```json
{
  "questions": [{
    "question": "논문 검색에 사용할 데이터베이스를 선택해 주세요. / Select databases for paper retrieval.",
    "header": "Databases",
    "options": [
      {"label": "All Three (Recommended)", "description": "Semantic Scholar + OpenAlex + arXiv for maximum coverage"},
      {"label": "Semantic Scholar + OpenAlex", "description": "Two major databases without arXiv preprints"},
      {"label": "Custom Selection", "description": "Choose specific databases based on your field"}
    ],
    "multiSelect": false
  }]
}
```

### SCH_API_KEY_VALIDATION
```json
{
  "questions": [{
    "question": "선택한 데이터베이스에 필요한 API 키가 누락되었습니다. 어떻게 진행하시겠습니까? / API key(s) missing for selected database(s). How would you like to proceed?",
    "header": "API Keys",
    "options": [
      {"label": "Provide Key / 키 제공", "description": "Set the API key in environment variables and retry validation"},
      {"label": "Skip DB / DB 제외", "description": "Remove databases with missing keys and continue with available ones"},
      {"label": "Pause / 중단", "description": "Pause the pipeline to configure API keys later"}
    ],
    "multiSelect": false
  }]
}
```

### SCH_SCREENING_CRITERIA
```json
{
  "questions": [{
    "question": "PRISMA 스크리닝 기준을 승인하시겠습니까? / Approve the PRISMA screening criteria?",
    "header": "Screening",
    "options": [
      {"label": "Approve / 승인", "description": "Approve inclusion/exclusion criteria and start AI screening"},
      {"label": "Modify / 수정", "description": "Adjust the screening criteria before proceeding"},
      {"label": "Review Details / 상세 검토", "description": "Show detailed criteria breakdown for review"}
    ],
    "multiSelect": false
  }]
}
```

---

## 🟠 RECOMMENDED Checkpoints

### CP_ANALYSIS_PLAN
```json
{
  "questions": [{
    "question": "분석 계획을 검토하시겠습니까? / Would you like to review the analysis plan?",
    "header": "Analysis",
    "options": [
      {"label": "Approve / 승인", "description": "Approve the analysis plan and proceed"},
      {"label": "Modify / 수정", "description": "Request changes to the analysis plan"},
      {"label": "Skip / 건너뛰기", "description": "Proceed with default analysis plan (not recommended)"}
    ],
    "multiSelect": false
  }]
}
```

### CP_SCREENING_CRITERIA
```json
{
  "questions": [{
    "question": "선정/배제 기준을 확인해 주세요. / Please confirm inclusion/exclusion criteria.",
    "header": "Criteria",
    "options": [
      {"label": "Approve / 승인", "description": "Confirm the inclusion/exclusion criteria"},
      {"label": "Modify / 수정", "description": "Adjust the criteria before screening"},
      {"label": "Skip / 건너뛰기", "description": "Use default criteria (not recommended)"}
    ],
    "multiSelect": false
  }]
}
```

### CP_QUALITY_REVIEW
```json
{
  "questions": [{
    "question": "품질 평가 결과를 검토하시겠습니까? / Review quality assessment results?",
    "header": "Quality",
    "options": [
      {"label": "Approve / 승인", "description": "Accept quality assessment results"},
      {"label": "Revise / 수정", "description": "Request re-assessment or additional checks"},
      {"label": "Skip / 건너뛰기", "description": "Proceed without detailed review (not recommended)"}
    ],
    "multiSelect": false
  }]
}
```

### CP_INTEGRATION_STRATEGY
```json
{
  "questions": [{
    "question": "혼합방법 통합 전략을 확인해 주세요. / Confirm mixed methods integration strategy.",
    "header": "Integration",
    "options": [
      {"label": "Approve / 승인", "description": "Confirm the integration strategy (joint display, transformation, etc.)"},
      {"label": "Modify / 수정", "description": "Adjust integration approach"},
      {"label": "Skip / 건너뛰기", "description": "Proceed with default strategy"}
    ],
    "multiSelect": false
  }]
}
```

### CP_SAMPLING_STRATEGY
```json
{
  "questions": [{
    "question": "표본 추출 전략을 승인하시겠습니까? / Approve the sampling strategy?",
    "header": "Sampling",
    "options": [
      {"label": "Approve / 승인", "description": "Approve sample size, selection criteria, and recruitment plan"},
      {"label": "Modify / 수정", "description": "Adjust sampling parameters or strategy"},
      {"label": "Skip / 건너뛰기", "description": "Proceed with proposed strategy"}
    ],
    "multiSelect": false
  }]
}
```

### CP_CODING_APPROACH
```json
{
  "questions": [{
    "question": "질적 코딩 접근법을 확인해 주세요. / Confirm qualitative coding approach.",
    "header": "Coding",
    "options": [
      {"label": "Deductive / 연역적", "description": "Pre-defined codes from theory or literature"},
      {"label": "Inductive / 귀납적", "description": "Codes emerge from data (grounded theory style)"},
      {"label": "Hybrid / 혼합", "description": "Start with deductive, allow inductive emergence"}
    ],
    "multiSelect": false
  }]
}
```

### CP_THEME_VALIDATION
```json
{
  "questions": [{
    "question": "도출된 주제를 검증하시겠습니까? / Validate the identified themes?",
    "header": "Themes",
    "options": [
      {"label": "Approve / 승인", "description": "Accept the identified themes and proceed to reporting"},
      {"label": "Refine / 정제", "description": "Refine or merge themes before finalizing"},
      {"label": "Recode / 재코딩", "description": "Return to coding phase for additional analysis"}
    ],
    "multiSelect": false
  }]
}
```

### CP_VS_002 (VS Risk Warning)
```json
{
  "questions": [{
    "question": "선택하신 옵션의 T-Score가 낮습니다 (T < 0.3). 계속하시겠습니까? / Selected option has low T-Score. Continue?",
    "header": "Risk",
    "options": [
      {"label": "Proceed / 진행", "description": "Accept the risk and proceed with innovative approach"},
      {"label": "Safer Option / 안전한 옵션", "description": "Switch to a higher T-Score alternative"},
      {"label": "More Info / 추가 정보", "description": "Show more details about risks and justification needed"}
    ],
    "multiSelect": false
  }]
}
```

### SCH_RAG_READINESS
```json
{
  "questions": [{
    "question": "RAG 시스템 구축을 시작하시겠습니까? / Ready to build the RAG system?",
    "header": "RAG",
    "options": [
      {"label": "Build RAG / 구축", "description": "Proceed with vector database construction from collected PDFs"},
      {"label": "Review PDFs / PDF 검토", "description": "Review downloaded PDFs before building RAG"},
      {"label": "Skip RAG / 건너뛰기", "description": "Skip RAG and proceed to manual analysis"}
    ],
    "multiSelect": false
  }]
}
```

### CP_HUMANIZATION_REVIEW
```json
{
  "questions": [{
    "question": "AI 패턴 분석 결과를 검토하시겠습니까? / Review AI pattern analysis results?",
    "header": "AI Patterns",
    "options": [
      {"label": "Humanize / 휴먼화", "description": "Proceed to humanize detected AI patterns"},
      {"label": "Review Details / 상세 보기", "description": "Show detailed pattern report before deciding"},
      {"label": "Skip / 건너뛰기", "description": "Keep text as-is without humanization"}
    ],
    "multiSelect": false
  }]
}
```

---

## 🟡 OPTIONAL Checkpoints

### CP_VISUALIZATION_PREFERENCE
```json
{
  "questions": [{
    "question": "시각화 스타일을 선택해 주세요. / Select visualization style.",
    "header": "Visual",
    "options": [
      {"label": "Academic / 학술", "description": "Clean, publication-ready academic style"},
      {"label": "Presentation / 발표", "description": "Colorful, engagement-focused style"},
      {"label": "Minimal / 미니멀", "description": "Simple, data-focused minimal design"}
    ],
    "multiSelect": false
  }]
}
```

### CP_SEARCH_STRATEGY
```json
{
  "questions": [{
    "question": "검색 전략을 확인해 주세요. / Confirm search strategy.",
    "header": "Search",
    "options": [
      {"label": "Approve / 승인", "description": "Proceed with the proposed search strategy"},
      {"label": "Modify / 수정", "description": "Adjust search terms or database selection"}
    ],
    "multiSelect": false
  }]
}
```

### CP_WRITING_STYLE
```json
{
  "questions": [{
    "question": "작성 스타일을 선택해 주세요. / Select writing style.",
    "header": "Style",
    "options": [
      {"label": "APA 7th", "description": "American Psychological Association 7th edition"},
      {"label": "Chicago", "description": "Chicago Manual of Style"},
      {"label": "Custom / 사용자 정의", "description": "Specify custom style guidelines"}
    ],
    "multiSelect": false
  }]
}
```

### CP_PROTOCOL_DESIGN
```json
{
  "questions": [{
    "question": "프로토콜 설계를 확인해 주세요. / Confirm protocol design.",
    "header": "Protocol",
    "options": [
      {"label": "Approve / 승인", "description": "Approve the interview/observation protocol"},
      {"label": "Modify / 수정", "description": "Adjust protocol questions or structure"}
    ],
    "multiSelect": false
  }]
}
```

### CP_HUMANIZATION_VERIFY
```json
{
  "questions": [{
    "question": "휴먼화 결과를 최종 확인하시겠습니까? / Verify humanization results?",
    "header": "Verify",
    "options": [
      {"label": "Accept / 수락", "description": "Accept humanized text and proceed to export"},
      {"label": "Re-humanize / 재처리", "description": "Run humanization again with different settings"}
    ],
    "multiSelect": false
  }]
}
```

---

## Override Refusal Template (v8.2)

When a user requests to skip a REQUIRED (🔴) checkpoint, use this template:

```json
{
  "questions": [{
    "question": "이 체크포인트는 REQUIRED 등급입니다. 건너뛸 수 없습니다. / This checkpoint is REQUIRED and cannot be skipped. Please make a decision to proceed.",
    "header": "Required",
    "options": [
      {"label": "Continue / 계속", "description": "Provide the required decision now"},
      {"label": "Help / 도움", "description": "Get more information to make this decision"},
      {"label": "Pause / 일시중지", "description": "Take a break and return to this later"}
    ],
    "multiSelect": false
  }]
}
```

**Rule**: REQUIRED checkpoints can NEVER be skipped, even if the user explicitly asks. Always present this template when a skip is requested.

---

## Usage Notes

1. **REQUIRED checkpoints**: MUST call AskUserQuestion. Cannot be skipped even if user asks. Use Override Refusal Template if skip requested.
2. **RECOMMENDED checkpoints**: SHOULD call AskUserQuestion. Can be skipped only if user explicitly declines.
3. **OPTIONAL checkpoints**: MAY call AskUserQuestion. Defaults are acceptable.
4. **Dynamic options**: For CP_THEORY_SELECTION and CP_VS_001, replace Direction A/B/C labels with actual VS alternatives generated during the agent's work.
5. **Language**: Templates are bilingual (EN/KR). The agent should present in the user's preferred language.
6. **MCP Integration (v8.2)**: After AskUserQuestion approval, call `diverga_mark_checkpoint(checkpoint_id, decision, rationale)` to record the decision.
