# B5-ParallelDocumentProcessor Documentation
# B5-병렬문서처리기 문서

**Version**: 6.2.0 | **Agent ID**: B5 | **Category**: B - Literature & Evidence

---

## Quick Start / 빠른 시작

### English

B5-ParallelDocumentProcessor solves the problem of processing large PDF collections that would crash single-threaded approaches due to context overflow.

**Problem**: Processing 100+ PDFs sequentially causes memory overflow
**Solution**: Distribute work across parallel workers

### 한국어

B5-병렬문서처리기는 컨텍스트 오버플로우로 인해 단일 스레드 접근 방식에서 충돌하는 대규모 PDF 컬렉션 처리 문제를 해결합니다.

**문제**: 100개 이상의 PDF를 순차 처리하면 메모리 오버플로우 발생
**해결**: 병렬 워커들에게 작업 분배

---

## Architecture / 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                  B5-ParallelDocumentProcessor                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                           │
│                    │   COORDINATOR   │  (Opus)                   │
│                    │    코디네이터    │                           │
│                    │                 │                           │
│                    │ • Scan files    │                           │
│                    │ • Plan batches  │                           │
│                    │ • Spawn workers │                           │
│                    │ • Aggregate     │                           │
│                    └────────┬────────┘                           │
│                             │                                    │
│           ┌─────────────────┼─────────────────┐                  │
│           ▼                 ▼                 ▼                  │
│     ┌───────────┐    ┌───────────┐    ┌───────────┐             │
│     │ Worker 1  │    │ Worker 2  │    │ Worker N  │  (Haiku)    │
│     │ PDF 1-20  │    │ PDF 21-40 │    │ PDF ...   │             │
│     └─────┬─────┘    └─────┬─────┘    └─────┬─────┘             │
│           │                │                │                    │
│           └────────────────┼────────────────┘                    │
│                            ▼                                     │
│                    ┌─────────────┐                               │
│                    │   Results   │                               │
│                    │    결과     │                               │
│                    └─────────────┘                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## How It Works / 작동 방식

### Phase 1: Discovery / 발견 단계

```python
# Scan directory and plan
files = scan_directory("/path/to/pdfs")
total_count = 127
total_size = 512 MB
estimated_time = "15-20 minutes"
```

### Phase 2: Planning / 계획 단계

```python
# Determine optimal configuration
workers = 5
batch_size = 26  # PDFs per worker
worker_model = "haiku"  # Fast and cost-effective
```

### Phase 3: Parallel Execution / 병렬 실행 단계

```xml
<!-- Single message with multiple Task = Parallel execution -->
<function_calls>
  <invoke name="Task">Worker 1: PDFs 1-26</invoke>
  <invoke name="Task">Worker 2: PDFs 27-52</invoke>
  <invoke name="Task">Worker 3: PDFs 53-78</invoke>    ← All run simultaneously
  <invoke name="Task">Worker 4: PDFs 79-104</invoke>
  <invoke name="Task">Worker 5: PDFs 105-127</invoke>
</function_calls>
```

### Phase 4: Aggregation / 집계 단계

```python
# Combine results from all workers
results = merge(worker_1, worker_2, ..., worker_n)
failed = identify_failures()
retry(failed) if enabled
generate_report()
```

---

## Performance Comparison / 성능 비교

| PDF Count | Sequential | Parallel (5 workers) | Speedup |
|-----------|------------|---------------------|---------|
| 10 | 5 min | 1.5 min | **3.3x** |
| 50 | 25 min | 6 min | **4.2x** |
| 100 | 50 min | 12 min | **4.2x** |
| 200 | 100 min | 25 min | **4.0x** |

---

## Worker Types / 워커 유형

| Type | Model | Batch Size | Use Case |
|------|-------|------------|----------|
| **Light** | Haiku | 20 PDFs | Metadata, abstracts |
| **Standard** | Sonnet | 10 PDFs | Full text, tables |
| **Heavy** | Opus | 5 PDFs | Complex analysis |

---

## Trigger Keywords / 트리거 키워드

| English | Korean |
|---------|--------|
| "batch PDF" | "배치 PDF" |
| "parallel reading" | "병렬 처리" |
| "multiple PDFs" | "여러 PDF" |
| "large document" | "대용량 문서" |
| "bulk extraction" | "일괄 추출" |

---

## Input/Output Schema

### Input

```yaml
Required:
  - pdf_directory: "/path/to/pdfs"
  - extraction_task: "full_text | abstract | metadata | tables"

Optional:
  - max_workers: 5  # default, max 10
  - batch_size: 10  # PDFs per worker
  - output_format: "json | csv | markdown"
  - retry_failed: true
```

### Output

```json
{
  "summary": {
    "total_files": 127,
    "successful": 124,
    "failed": 3,
    "processing_time": "14m 32s"
  },
  "results": [
    {
      "file": "smith_2021.pdf",
      "status": "success",
      "extracted_data": {...}
    }
  ],
  "failed_files": [
    {
      "file": "scan_2019.pdf",
      "reason": "OCR required"
    }
  ]
}
```

---

## Error Handling / 에러 처리

| Error | Recovery Strategy |
|-------|------------------|
| Memory overflow | Reduce batch size, use Light worker |
| Corrupted PDF | Skip and log, continue with others |
| Timeout | Retry with extended timeout |
| OCR needed | Flag for preprocessing |
| Password protected | Skip and notify user |

---

## Integration with Other Agents / 다른 에이전트와 연동

### Upstream (provides data to B5)

```
B1-SystematicLiteratureScout → B5
  Provides: PDF list from search
```

### Downstream (receives data from B5)

```
B5 → B2-EvidenceQualityAppraiser
  Provides: Extracted text for quality assessment

B5 → B3-EffectSizeExtractor
  Provides: Statistical sections for effect size extraction

B5 → E1-QuantitativeAnalysisGuide
  Provides: Aggregated data for analysis
```

---

## Usage Examples / 사용 예시

### Example 1: Systematic Review

```
User: "Process all 127 PDFs in my SR folder"

B5 Response:
"Scanning systematic review folder...

📊 Discovery Results:
- Total PDFs: 127
- Total size: 512 MB
- Estimated time: 15-20 minutes

Configuration:
- Workers: 5 (Haiku)
- Batch size: 26 per worker

Worker Progress:
[W1] ████████░░ 80% (21/26)
[W2] ██████░░░░ 60% (16/26)
[W3] ██████████ 100% ✓
[W4] ████░░░░░░ 40% (11/26)
[W5] ████████░░ 80% (21/26)

Overall: 95/127 (75%) | ETA: 5 min"
```

### Example 2: Targeted Extraction (효과크기 추출)

```
User: "메타분석 논문들에서 표본크기와 효과크기만 추출해줘"

B5 Configuration:
  extraction_task: specific_sections
  fields: ["sample_size", "effect_size", "CI"]
  output_format: csv

Output:
file,sample_size,effect_size,effect_type
smith_2021.pdf,1234,0.45,Cohen's d
wang_2022.pdf,567,0.62,Hedge's g
```

### Example 3: Large Single File (대용량 단일 파일)

```
User: "500페이지 박사논문이 자꾸 크래시돼요"

B5 Strategy:
1. Split into 50-page chunks
2. Process chunks in parallel
3. Reassemble in order

Result: Processed in 8-12 minutes instead of crash
```

---

## Configuration Presets / 설정 프리셋

### Default (Balanced)

```yaml
workers: 5
batch_size: 10
worker_model: haiku
timeout: 60s
retry: true
```

### Memory-Safe (메모리 안전)

```yaml
workers: 3
batch_size: 5
worker_model: haiku
timeout: 120s
retry: true
```

### Maximum Speed (최대 속도)

```yaml
workers: 10
batch_size: 20
worker_model: haiku
timeout: 30s
retry: false
```

---

## Checkpoints / 체크포인트

| Checkpoint | Level | When |
|------------|-------|------|
| CP-INIT-001 | 🔴 Required | Before processing - confirm file count |
| CP-PROGRESS-001 | 🟠 Recommended | At 50% - allow adjustment |
| CP-COMPLETE-001 | 🟡 Optional | After processing - review results |

---

## Related Documentation / 관련 문서

- [MECHANISM.md](../.claude/skills/research-agents/B5-parallel-document-processor/MECHANISM.md) - Detailed implementation
- [workflow-parallel-pdf.md](../.claude/skills/research-agents/B5-parallel-document-processor/workflow-parallel-pdf.md) - Workflow details
- [README-ko.md](../.claude/skills/research-agents/B5-parallel-document-processor/README-ko.md) - Korean guide
- [AGENT-ORCHESTRATION-GUIDE.md](./AGENT-ORCHESTRATION-GUIDE.md) - Full orchestration guide
