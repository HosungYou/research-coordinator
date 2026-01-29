"""
Diverga QA Conversation Simulator
===================================

Simulates conversations against test scenarios and collects metrics.
Validates checkpoint behavior, agent invocations, and VS methodology quality.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from ..protocol.scenarios import (
    Scenario,
    ConversationTurn,
    Paradigm,
    CheckpointLevel,
)
from ..protocol.metrics import (
    MetricsCollector,
    TestResult,
    GradeLevel,
    CheckpointMetrics,
    AgentMetrics,
    VSQualityMetrics,
)
from .checkpoint_validator import CheckpointValidator, ValidationResult
from .agent_tracker import AgentTracker, AgentInvocation


@dataclass
class SimulationResult:
    """Result of a conversation simulation turn."""
    turn_number: int
    user_input: str
    ai_response: str | None = None

    # Validation results
    checkpoint_result: ValidationResult | None = None
    agent_invocations: list[AgentInvocation] = field(default_factory=list)

    # Behavior validation
    paradigm_detected: Paradigm | None = None
    keywords_matched: list[str] = field(default_factory=list)

    # Pass/fail
    passed: bool = True
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "turn_number": self.turn_number,
            "user_input": self.user_input[:100] + "..." if len(self.user_input) > 100 else self.user_input,
            "ai_response_preview": self.ai_response[:200] + "..." if self.ai_response and len(self.ai_response) > 200 else self.ai_response,
            "checkpoint_result": self.checkpoint_result.checkpoint_id if self.checkpoint_result else None,
            "paradigm_detected": self.paradigm_detected.value if self.paradigm_detected else None,
            "keywords_matched": self.keywords_matched,
            "passed": self.passed,
            "issues": self.issues,
            "warnings": self.warnings,
        }


class ConversationSimulator:
    """
    Simulates Diverga conversations based on test scenarios.

    This simulator:
    1. Loads test scenarios from YAML files
    2. Executes conversation turns
    3. Validates checkpoint behavior
    4. Tracks agent invocations
    5. Evaluates VS methodology quality
    6. Generates comprehensive test reports
    """

    # Paradigm detection patterns
    PARADIGM_PATTERNS = {
        Paradigm.QUANTITATIVE: [
            r"meta-analysis", r"메타분석", r"effect size", r"효과크기",
            r"hypothesis", r"가설", r"statistical", r"통계",
            r"experiment", r"실험", r"RCT", r"correlation", r"상관",
        ],
        Paradigm.QUALITATIVE: [
            r"lived experience", r"체험", r"phenomenology", r"현상학",
            r"grounded theory", r"근거이론", r"interview", r"인터뷰",
            r"thematic", r"주제", r"narrative", r"내러티브",
        ],
        Paradigm.MIXED_METHODS: [
            r"mixed method", r"혼합방법", r"sequential", r"순차적",
            r"convergent", r"수렴", r"integration", r"통합",
        ],
    }

    def __init__(self, scenario: Scenario):
        """
        Initialize simulator with a test scenario.

        Args:
            scenario: Test scenario to simulate
        """
        self.scenario = scenario
        self.checkpoint_validator = CheckpointValidator()
        self.agent_tracker = AgentTracker()
        self.metrics = MetricsCollector(scenario.scenario_id)

        # Simulation state
        self.current_turn = 0
        self.results: list[SimulationResult] = []
        self.triggered_checkpoints: list[str] = []

    def reset(self):
        """Reset simulator state for a new run."""
        self.current_turn = 0
        self.results = []
        self.triggered_checkpoints = []
        self.agent_tracker.reset()
        self.metrics = MetricsCollector(self.scenario.scenario_id)

    def run_turn(
        self,
        user_input: str,
        ai_response: str,
    ) -> SimulationResult:
        """
        Execute a single conversation turn and evaluate.

        Args:
            user_input: User message for this turn
            ai_response: AI response to evaluate

        Returns:
            SimulationResult with validation details
        """
        self.current_turn += 1

        result = SimulationResult(
            turn_number=self.current_turn,
            user_input=user_input,
            ai_response=ai_response,
        )

        # Get expected behavior for this turn
        expected = self._get_expected_turn(self.current_turn)

        if expected:
            # 1. Detect paradigm
            result.paradigm_detected = self._detect_paradigm(user_input)
            if expected.expected_behaviors.paradigm_detection:
                if result.paradigm_detected != expected.expected_behaviors.paradigm_detection:
                    result.warnings.append(
                        f"PARADIGM_MISMATCH: Expected {expected.expected_behaviors.paradigm_detection.value}, "
                        f"detected {result.paradigm_detected.value if result.paradigm_detected else 'none'}"
                    )

            # 2. Match keywords
            result.keywords_matched = self._match_keywords(
                user_input,
                expected.expected_behaviors.keyword_matches,
            )

            # 3. Validate checkpoint if expected
            if expected.expected_behaviors.checkpoint_trigger:
                checkpoint_id = expected.expected_behaviors.checkpoint_trigger

                # Determine checkpoint level
                level = "REQUIRED"
                for cp in self.scenario.checkpoints_required:
                    if cp.checkpoint_id == checkpoint_id:
                        level = cp.level.value
                        break

                result.checkpoint_result = self.checkpoint_validator.validate(
                    ai_response,
                    checkpoint_id,
                    level,
                )

                # Record to metrics
                self.metrics.record_checkpoint(
                    checkpoint_id=checkpoint_id,
                    level=level,
                    halt_verified=result.checkpoint_result.halt_verified,
                    approval_explicit=result.checkpoint_result.wait_behavior_detected,
                    vs_options_count=result.checkpoint_result.alternatives_count,
                    t_scores_shown=result.checkpoint_result.t_scores_visible,
                    t_score_range=result.checkpoint_result.t_score_range,
                )

                # Track checkpoint
                if result.checkpoint_result.checkpoint_triggered:
                    self.triggered_checkpoints.append(checkpoint_id)

                # Add issues from checkpoint validation
                if result.checkpoint_result.issues:
                    result.issues.extend(result.checkpoint_result.issues)

            # 4. Track agent invocation if expected
            if expected.expected_behaviors.agent_invoked:
                agent_id = expected.expected_behaviors.agent_invoked
                model_tier = expected.expected_behaviors.model_tier or "opus"

                # Detect agent from response
                detected = self._detect_agent_in_response(ai_response)

                if detected:
                    invocation = self.agent_tracker.record_invocation(
                        agent_id=detected,
                        model_tier=model_tier,
                    )
                    result.agent_invocations.append(invocation)

                    # Record to metrics
                    self.metrics.record_agent(
                        agent_id=agent_id,
                        model_tier=model_tier,
                        invoked=True,
                        correct_model_tier=invocation.is_correct_tier,
                    )
                else:
                    result.issues.append(
                        f"AGENT_NOT_DETECTED: Expected {agent_id} but not found in response"
                    )

            # 5. Check VS quality from response
            vs_quality = self._evaluate_vs_quality(ai_response)
            self.metrics.record_vs_quality(
                options_presented=vs_quality.get("options_count", 0),
                t_score_min=vs_quality.get("t_score_min", 1.0),
                t_score_max=vs_quality.get("t_score_max", 0.0),
                modal_identified=vs_quality.get("modal_identified", False),
                modal_recommended=vs_quality.get("modal_recommended", False),
            )

            # 6. Check for auto-proceed violation
            if expected.expected_behaviors.no_auto_proceed:
                if self._detect_auto_proceed(ai_response):
                    result.issues.append("AUTO_PROCEED_VIOLATION: AI proceeded without waiting")

        # Determine overall pass/fail
        result.passed = len(result.issues) == 0

        # Store result
        self.results.append(result)

        return result

    def finalize(self) -> TestResult:
        """
        Finalize simulation and generate test result.

        Returns:
            Complete TestResult with all metrics
        """
        # Validate checkpoint sequence
        expected_sequence = [
            cp.checkpoint_id for cp in self.scenario.checkpoints_required
        ]
        sequence_valid, sequence_issues = self.checkpoint_validator.validate_checkpoint_sequence(
            self.triggered_checkpoints,
            expected_sequence,
        )

        if not sequence_valid:
            for issue in sequence_issues:
                self.metrics.add_issue(issue)

        # Validate agent invocations
        for agent in self.scenario.agents_primary:
            valid, issues = self.agent_tracker.validate_invocation(
                agent.agent_id,
                agent.model_tier,
            )
            for issue in issues:
                self.metrics.add_warning(issue)

        return self.metrics.finalize()

    def _get_expected_turn(self, turn_number: int) -> ConversationTurn | None:
        """Get expected behavior for a turn."""
        for turn in self.scenario.conversation_flow:
            if turn.turn_number == turn_number:
                return turn
        return None

    def _detect_paradigm(self, text: str) -> Paradigm | None:
        """Detect research paradigm from text."""
        text_lower = text.lower()

        scores = {p: 0 for p in Paradigm if p != Paradigm.ANY}

        for paradigm, patterns in self.PARADIGM_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    scores[paradigm] += 1

        if all(s == 0 for s in scores.values()):
            return None

        return max(scores, key=scores.get)

    def _match_keywords(
        self,
        text: str,
        expected_keywords: list[str],
    ) -> list[str]:
        """Match expected keywords in text."""
        matched = []
        text_lower = text.lower()

        for keyword in expected_keywords:
            if keyword.lower() in text_lower:
                matched.append(keyword)

        return matched

    def _detect_agent_in_response(self, response: str) -> str | None:
        """Detect which agent was invoked based on response patterns."""
        # Look for Task tool patterns
        task_patterns = [
            r'subagent_type\s*=\s*["\']diverga:([a-h]\d)["\']',
            r'diverga:([a-h]\d)',
            r'([A-H]\d)-\w+Master',
            r'([A-H]\d)-\w+Guard',
            r'([A-H]\d)-\w+Engine',
        ]

        for pattern in task_patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                agent_code = match.group(1).lower()
                return f"diverga:{agent_code}"

        return None

    def _evaluate_vs_quality(self, response: str) -> dict[str, Any]:
        """Evaluate VS methodology quality in response."""
        quality = {
            "options_count": 0,
            "t_score_min": 1.0,
            "t_score_max": 0.0,
            "modal_identified": False,
            "modal_recommended": False,
        }

        # Count options
        option_patterns = [r"\[A\]", r"\[B\]", r"\[C\]", r"\[D\]"]
        for pattern in option_patterns:
            if re.search(pattern, response):
                quality["options_count"] += 1

        # Extract T-scores
        t_score_pattern = r"T\s*[=≈]\s*(0?\.\d+)"
        matches = re.findall(t_score_pattern, response, re.IGNORECASE)
        if matches:
            t_scores = [float(m) for m in matches]
            quality["t_score_min"] = min(t_scores)
            quality["t_score_max"] = max(t_scores)

            # Check for modal avoidance
            if quality["t_score_max"] >= 0.7:
                quality["modal_identified"] = True
                # Check if modal is recommended as primary
                if "권장" in response or "recommend" in response.lower():
                    # Check if high T-score option is marked as recommended
                    modal_recommended_pattern = r"\[A\].*?T\s*[=≈]\s*0\.[6-9].*?(?:권장|recommend)"
                    if re.search(modal_recommended_pattern, response, re.IGNORECASE | re.DOTALL):
                        quality["modal_recommended"] = True

        return quality

    def _detect_auto_proceed(self, response: str) -> bool:
        """Detect if AI auto-proceeded without waiting."""
        auto_proceed_patterns = [
            r"진행하겠습니다(?![?])",
            r"시작하겠습니다(?![?])",
            r"I will proceed",
            r"I'll proceed",
            r"proceeding with",
        ]

        for pattern in auto_proceed_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return True

        return False

    @classmethod
    def from_scenario_file(cls, scenario_path: Path | str) -> "ConversationSimulator":
        """Create simulator from scenario YAML file."""
        scenario = Scenario.from_yaml(scenario_path)
        return cls(scenario)

    @classmethod
    def from_scenario_id(cls, scenario_id: str) -> "ConversationSimulator":
        """Create simulator from scenario ID."""
        from ..protocol.scenarios import load_scenario
        scenario = load_scenario(scenario_id)
        return cls(scenario)
