# Layer 2 Task Interceptor - Quick Reference

## One-Line Summary

Automatic research context injection for `diverga:` agents - load once, agents remember forever.

## Installation

```bash
pip install pyyaml
```

## Basic Usage

```python
from memory.src import intercept_task_call

# Intercept before calling Task
modified_prompt = intercept_task_call(
    subagent_type="diverga:a1",  # Any diverga: agent
    prompt="Refine my research question"
)

# modified_prompt now includes full project context
```

## API Cheat Sheet

| Function | Input | Output | Use Case |
|----------|-------|--------|----------|
| `extract_agent_id()` | `"diverga:a1"` | `"a1"` | Check if diverga agent |
| `detect_project_root()` | `None` (cwd) | `Path` or `None` | Find .research/ folder |
| `load_full_research_context()` | `Path` | `ResearchContext` | Load all context |
| `detect_current_stage()` | `Path` | `"foundation"` | Detect research stage |
| `intercept_task_call()` | `(type, prompt)` | `str` | Main function |

## Project Structure

```
project/
└── .research/
    ├── project-state.yaml       # REQUIRED
    ├── decision-log.yaml        # Optional
    ├── checkpoints.yaml         # Optional
    └── changes/current/         # For stage detection
```

## Context Injected

```markdown
## Current Research Context
Project: my-project
Stage: methodology
Last Updated: 2024-02-03

## Recent Decisions (Last 5)
- [timestamp] agent: decision

## Active Checkpoints
- CP_ID (status)

## Your Role: Agent A1
[Original prompt here]
```

## Supported Agents

All 40 Diverga agents (`diverga:a1` through `diverga:h2`)

## Error Handling

**Always returns a prompt** - falls back to original on any error.

## Testing

```bash
cd /Volumes/External\ SSD/Projects/Research/Diverga/lib/memory
python3 examples/basic_usage.py
```

## Integration Example

```python
# wrapper.py
from memory.src import inject_context_if_diverga

def task_wrapper(subagent_type, prompt, **kwargs):
    prompt = inject_context_if_diverga(subagent_type, prompt)
    return Task(subagent_type=subagent_type, prompt=prompt, **kwargs)
```

## Dependencies

- Python 3.8+
- pyyaml

## Documentation

- Full docs: `README.md`
- Examples: `examples/basic_usage.py`
- Tests: `tests/test_task_interceptor.py`
- Summary: `IMPLEMENTATION_SUMMARY.md`

## Status

✅ Production Ready - v7.0.0 (2024-02-03)
