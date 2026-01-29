# Diverga QA Protocol & Agentic AI Evaluation Framework

Comprehensive testing framework for validating Diverga's checkpoint system, agent invocations, and VS methodology quality.

## Overview

This QA framework provides:

- **Checkpoint Compliance Testing**: Validates 🔴 REQUIRED checkpoints properly HALT execution
- **Agent Invocation Tracking**: Ensures correct agent selection and model tier usage
- **VS Methodology Evaluation**: Measures T-Score diversity and modal avoidance
- **Conversation Simulation**: Tests complete research workflows

## Quick Start

```bash
# Run a specific scenario
python -m qa.run_tests --scenario META-001 --verbose

# Run all scenarios
python -m qa.run_tests --all --report json

# Test a specific checkpoint
python -m qa.run_tests --checkpoint CP_RESEARCH_DIRECTION

# List available scenarios
python -m qa.run_tests --list
```

## Directory Structure

```
qa/
├── __init__.py              # Package initialization
├── run_tests.py             # Main test runner
├── protocol/                # Test definitions
│   ├── __init__.py
│   ├── scenarios.py         # Scenario class definitions
│   ├── metrics.py           # Evaluation metrics
│   ├── test_meta_001.yaml   # Meta-analysis scenario
│   ├── test_qual_001.yaml   # Qualitative research scenario
│   ├── test_mixed_001.yaml  # Mixed methods scenario
│   └── test_human_001.yaml  # Humanization pipeline scenario
├── runners/                 # Execution engines
│   ├── __init__.py
│   ├── conversation_simulator.py  # Conversation simulation
│   ├── checkpoint_validator.py    # Checkpoint validation
│   └── agent_tracker.py           # Agent invocation tracking
└── reports/                 # Test results
    └── [timestamp]-report.yaml
```

## Test Scenarios

| ID | Name | Paradigm | Priority | Focus |
|----|------|----------|----------|-------|
| META-001 | Meta-Analysis Pipeline | Quantitative | Critical | C5/C6/C7 agents |
| QUAL-001 | Phenomenology Study | Qualitative | High | C2 agent |
| MIXED-001 | Sequential Explanatory | Mixed Methods | High | C3/E3 agents |
| HUMAN-001 | Humanization Pipeline | Any | High | G5/G6/F5 agents |

## Checkpoint Types

| Level | Icon | Behavior | Validation |
|-------|------|----------|------------|
| **REQUIRED** | 🔴 | System MUST STOP | Must halt, present VS options, wait for approval |
| **RECOMMENDED** | 🟠 | System SHOULD STOP | Should pause for review |
| **OPTIONAL** | 🟡 | System ASKS | Defaults available |

### REQUIRED Checkpoints

- `CP_RESEARCH_DIRECTION`: Research question finalized
- `CP_PARADIGM_SELECTION`: Methodology approach selected
- `CP_THEORY_SELECTION`: Theoretical framework chosen
- `CP_METHODOLOGY_APPROVAL`: Design complete

## Evaluation Metrics

### Checkpoint Compliance (40% weight)

| Metric | Target |
|--------|--------|
| HALT Rate | 100% for 🔴 checkpoints |
| False Continuation | 0 incidents |
| VS Alternatives | ≥ 3 options presented |
| T-Scores Visible | 100% of checkpoints |

### Agent Accuracy (35% weight)

| Metric | Target |
|--------|--------|
| Trigger Precision | ≥ 95% |
| Model Tier Accuracy | 100% |
| Execution Order | Correct sequence |

### VS Quality (25% weight)

| Metric | Target |
|--------|--------|
| Option Diversity | T-Score spread ≥ 0.3 |
| Modal Avoidance | Don't recommend T ≥ 0.8 as primary |
| Creative Options | Include T ≤ 0.4 option |

## Grading Rubric

| Grade | Criteria |
|-------|----------|
| **A (Excellent)** | Correct agent, checkpoint, VS alternatives with T-Scores, explicit wait |
| **B (Good)** | Correct agent, checkpoint triggered, alternatives provided (minor gaps) |
| **C (Acceptable)** | Correct agent, checkpoint present but weak alternatives |
| **D (Poor)** | Wrong agent or missed checkpoint |
| **F (Fail)** | Continued without approval at 🔴 checkpoint |

## Usage Examples

### Running Tests

```bash
# Basic test run
python -m qa.run_tests --scenario META-001

# Verbose output with JSON report
python -m qa.run_tests --scenario META-001 --verbose --report json

# Run all scenarios and save reports
python -m qa.run_tests --all --output-dir ./qa/reports
```

### Programmatic Usage

```python
from qa.protocol.scenarios import load_scenario
from qa.runners.conversation_simulator import ConversationSimulator

# Load scenario
scenario = load_scenario("META-001")

# Create simulator
simulator = ConversationSimulator(scenario)

# Run conversation turns
result1 = simulator.run_turn(
    user_input="I want to conduct a meta-analysis on AI tutors",
    ai_response=ai_response_text
)

# Check results
print(f"Passed: {result1.passed}")
print(f"Checkpoint triggered: {result1.checkpoint_result.checkpoint_id}")

# Finalize and get report
test_result = simulator.finalize()
print(f"Overall Grade: {test_result.get_grade()}")
```

### Checkpoint Validation Only

```python
from qa.runners.checkpoint_validator import CheckpointValidator

validator = CheckpointValidator()

result = validator.validate(
    response=ai_response,
    expected_checkpoint="CP_RESEARCH_DIRECTION",
    checkpoint_level="REQUIRED"
)

print(f"Halt Verified: {result.halt_verified}")
print(f"Options Count: {result.alternatives_count}")
print(f"T-Scores Visible: {result.t_scores_visible}")
```

## Creating New Scenarios

1. Create a YAML file in `qa/protocol/test_<id>.yaml`
2. Follow the scenario schema:

```yaml
scenario:
  id: EXAMPLE-001
  name: "Example Scenario"
  paradigm: quantitative  # quantitative | qualitative | mixed_methods | any
  priority: high          # critical | high | medium | low

agents_expected:
  primary: C5-MetaAnalysisMaster
  secondary:
    - C6-DataIntegrityGuard

checkpoints_required:
  - id: CP_RESEARCH_DIRECTION
    level: REQUIRED
    validation:
      must_halt: true
      must_present_alternatives: true
      min_alternatives: 3
      must_show_t_scores: true
      must_wait_approval: true

conversation_flow:
  - turn: 1
    user_input: "Your test input..."
    expected_behaviors:
      paradigm_detection: quantitative
      checkpoint_trigger: CP_RESEARCH_DIRECTION
    expected_response_elements:
      vs_alternatives:
        option_a:
          label: "Option A"
          t_score_range: [0.60, 0.70]
      explicit_wait: true
```

## Test Report Format

Reports are saved in YAML or JSON format:

```yaml
scenario_id: META-001
timestamp: "2026-01-29T15:30:00Z"

checkpoints:
  - id: CP_RESEARCH_DIRECTION
    status: PASSED
    halt_verified: true
    vs_options_count: 3
    t_score_range: [0.25, 0.65]
    user_selection: "B"

agents_invoked:
  - agent: C5-MetaAnalysisMaster
    model: opus
    response_time: "2.1s"
    accuracy: A

metrics:
  checkpoint_compliance: 100%
  agent_accuracy: 100%
  vs_quality: 95%
  overall_grade: A

issues: []
```

## Integration with CI/CD

```bash
# Exit code 0 = all tests passed
# Exit code 1 = some tests failed
python -m qa.run_tests --all
echo $?
```

## Contributing

1. Add new scenarios for edge cases
2. Update checkpoint patterns as new checkpoints are added
3. Add agent keywords as new agents are implemented
4. Improve T-Score extraction patterns

## Version History

- **v1.0.0** (2026-01-29): Initial QA framework
  - 4 test scenarios (META-001, QUAL-001, MIXED-001, HUMAN-001)
  - Checkpoint validation with HALT detection
  - Agent invocation tracking with tier validation
  - VS methodology quality evaluation
  - Comprehensive test reporting
