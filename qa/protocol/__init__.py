"""
Diverga QA Protocol Module
===========================

Defines test scenarios, evaluation metrics, and grading rubrics for
comprehensive Diverga plugin testing.

Classes:
- Scenario: Test scenario definition
- Checkpoint: Expected checkpoint behavior
- Metrics: Evaluation metrics framework
"""

from .scenarios import (
    Scenario,
    CheckpointExpectation,
    AgentExpectation,
    ConversationTurn,
    load_scenario,
    list_scenarios,
)

from .metrics import (
    MetricsCollector,
    CheckpointMetrics,
    AgentMetrics,
    VSQualityMetrics,
    TestResult,
    GradeLevel,
)

__all__ = [
    "Scenario",
    "CheckpointExpectation",
    "AgentExpectation",
    "ConversationTurn",
    "load_scenario",
    "list_scenarios",
    "MetricsCollector",
    "CheckpointMetrics",
    "AgentMetrics",
    "VSQualityMetrics",
    "TestResult",
    "GradeLevel",
]
