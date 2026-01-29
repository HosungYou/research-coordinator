# Diverga QA Protocol v3.0 Release Notes

## True Automated Testing Edition

**Release Date**: 2026-01-29
**Version**: QA Protocol v3.0

---

## Overview

QA Protocol v3.0 represents a paradigm shift from **simulation-based testing** to **true automated testing with real AI responses**. This release replaces hardcoded `RESPONSE_TEMPLATES` with actual CLI-based AI invocations, enabling genuine functional validation of the Diverga Research Coordinator.

---

## Core Philosophy

> **"Test with Real AI, Not Simulations"**
> **"시뮬레이션이 아닌 실제 AI로 테스트"**

---

## What's New

### 1. CLI-Based Automated Testing

Execute tests programmatically via CLI tools with no manual intervention:

| CLI Tool | Command | Session Support |
|----------|---------|-----------------|
| `claude` | `claude -p "message"` | `--continue` for multi-turn |
| `opencode` | `opencode run "message"` | Single-turn |
| `codex` | `codex exec "message"` | `--resume` |

### 2. CLITestRunner Class

New Python class for orchestrating CLI-based tests:

```python
from qa.runners import CLITestRunner

runner = CLITestRunner(
    scenario_id='QUAL-002',
    cli_tool='claude',
    verbose=True,
    dry_run=False,
    timeout=300
)

session = runner.run()
runner.save_results('qa/reports/sessions')
```

#### Key Features

- **Subprocess-based execution**: Capture real AI responses via `subprocess.run()`
- **Multi-turn sessions**: Maintain conversation context with `--continue` flag
- **Checkpoint detection**: Regex patterns for 🔴, 🟠, 🟡 markers
- **Agent tracking**: Detect `diverga:*` and `A1-*` style agent invocations
- **VS option extraction**: Parse T-Score values from responses
- **Dry run mode**: Test framework without API calls

### 3. Batch Testing Script

Run all scenarios with a single command:

```bash
# Real AI testing
./qa/run_all_scenarios.sh

# Dry run mode
./qa/run_all_scenarios.sh --dry-run

# Alternative CLI tool
./qa/run_all_scenarios.sh --cli opencode
```

### 4. Structured Output

Each test generates four files:

| File | Description |
|------|-------------|
| `README.md` | Session overview with metrics |
| `conversation_transcript.md` | Human-readable conversation |
| `conversation_raw.json` | RAW data with full metadata |
| `{SCENARIO}_test_result.yaml` | Test results and validation |

---

## v2.x vs v3.0 Comparison

| Aspect | v2.x (Simulation) | v3.0 (True Automation) |
|--------|-------------------|------------------------|
| **AI Response** | `RESPONSE_TEMPLATES` dict | **Real AI generation** |
| **Execution** | Python simulator | **CLI non-interactive mode** |
| **Validation** | Protocol format only | **Actual functionality** |
| **API Calls** | None | Real token consumption |
| **Response Variety** | Fixed templates | **Different every run** |

---

## Test Results: QUAL-002

First successful run with real AI on 2026-01-29:

```
============================================================
Diverga QA Protocol v3.0 - True Automated Testing
Scenario: QUAL-002
CLI Tool: claude
Mode: LIVE
============================================================

[Turn 1] INITIAL_REQUEST
  Received: 792 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 2] METHODOLOGICAL_CHALLENGE
  Received: 1810 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 3] SELECTION
  Received: 2469 chars
  ✓ Completed (CP: 1, Agents: 0)

...

[Turn 8] APPROVAL
  Received: 889 chars
  ✓ Completed (CP: 1, Agents: 0)

============================================================
Test Completed: QUAL-002
Turns: 8 | Checkpoints: 8 | Duration: ~4 min
============================================================
```

### Metrics Summary

| Metric | Value |
|--------|-------|
| Total Turns | 8 |
| Checkpoints Found | 8 |
| Total Response Characters | ~21,000 |
| Test Duration | ~4 minutes |

---

## Breaking Changes

### Removed

- `RESPONSE_TEMPLATES` dictionary in `automated_test.py` (v2.x only)
- Simulated response generation

### Changed

- `__init__.py` now exports both v2.x and v3.0 components
- Module structure supports backward compatibility

### Added

- `cli_test_runner.py` - New CLI test runner
- `run_all_scenarios.sh` - Batch testing script
- `CLITurn` alias to distinguish from v2.x `Turn`

---

## Directory Structure

```
qa/
├── README.md                    # Updated documentation
├── run_all_scenarios.sh         # v3.0 batch test script (NEW)
├── RELEASE-v3.0.md              # This file (NEW)
│
├── protocol/                    # Test scenario definitions
│   ├── test_qual_001.yaml
│   ├── test_qual_002.yaml       # QUAL-002 tested
│   ├── test_meta_001.yaml
│   ├── test_meta_002.yaml
│   ├── test_mixed_001.yaml
│   ├── test_mixed_002.yaml
│   ├── test_human_001.yaml
│   └── test_human_002.yaml
│
├── runners/                     # Test runners
│   ├── __init__.py              # Updated exports
│   ├── cli_test_runner.py       # v3.0 CLI runner (NEW)
│   ├── automated_test.py        # v2.x simulator
│   ├── extract_conversation.py
│   ├── checkpoint_validator.py
│   └── agent_tracker.py
│
└── reports/                     # Test results
    ├── sessions/
    │   └── QUAL-002/            # Real AI test results
    │       ├── README.md
    │       ├── conversation_transcript.md
    │       ├── conversation_raw.json
    │       └── QUAL-002_test_result.yaml
    └── real-transcripts/
```

---

## Usage Guide

### Single Scenario (Real AI)

```bash
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 --cli claude
```

### Single Scenario (Dry Run)

```bash
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 --dry-run
```

### All Scenarios (Batch)

```bash
./qa/run_all_scenarios.sh
```

### Verbose Mode

```bash
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 -v
```

---

## Requirements

1. **Claude Code CLI**: `npm install -g @anthropic-ai/claude-code`
2. **Authentication**: `claude` command must have API access
3. **Diverga Plugin**: Installed at `~/.claude/plugins/`

---

## Future Enhancements

- [ ] OpenCode and Codex CLI integration testing
- [ ] Parallel scenario execution
- [ ] Automated CI/CD integration
- [ ] Performance regression tracking
- [ ] Agent invocation verification

---

## Changelog

### v3.0.0 (2026-01-29)

- **ADDED**: `cli_test_runner.py` with `CLITestRunner` class
- **ADDED**: `run_all_scenarios.sh` batch test script
- **ADDED**: Dry run mode for framework testing
- **ADDED**: Multi-turn session support with `--continue`
- **UPDATED**: `__init__.py` to export v3.0 components
- **UPDATED**: `README.md` with v3.0 documentation
- **TESTED**: QUAL-002 scenario with real AI (8 turns, 8 checkpoints)

### v2.2.0 (2026-01-29)

- Automated test simulation with `RESPONSE_TEMPLATES`
- CLI-based execution: `python3 qa/runners/automated_test.py`

### v2.1.0 (2026-01-29)

- Session-based folder management
- RAW conversation extraction

### v2.0.0 (2026-01-29)

- Migrated to real Claude Code conversations
- Complex user input types
- JSONL session log extraction

---

## Contributors

- Hosung You (@HosungYou)
- Claude Opus 4.5 (AI Assistant)

---

## License

MIT License - Part of the Diverga Research Coordinator project.
