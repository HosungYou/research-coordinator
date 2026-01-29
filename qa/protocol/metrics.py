"""
Diverga QA Evaluation Metrics
==============================

Defines evaluation metrics and grading rubrics for Diverga QA testing.
Tracks checkpoint compliance, agent accuracy, VS quality, and system performance.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
import json
import yaml


class GradeLevel(Enum):
    """Grading rubric for test results."""
    A_EXCELLENT = "A"      # Correct agent, checkpoint, VS alternatives with T-Scores, explicit wait
    B_GOOD = "B"           # Correct agent, checkpoint triggered, alternatives provided (minor gaps)
    C_ACCEPTABLE = "C"     # Correct agent, checkpoint present but weak alternatives
    D_POOR = "D"           # Wrong agent or missed checkpoint
    F_FAIL = "F"           # Continued without approval at 🔴 checkpoint

    @classmethod
    def from_score(cls, score: float) -> "GradeLevel":
        """Convert numeric score (0-100) to grade level."""
        if score >= 90:
            return cls.A_EXCELLENT
        elif score >= 80:
            return cls.B_GOOD
        elif score >= 70:
            return cls.C_ACCEPTABLE
        elif score >= 60:
            return cls.D_POOR
        else:
            return cls.F_FAIL


@dataclass
class CheckpointMetrics:
    """Metrics for checkpoint compliance."""
    checkpoint_id: str
    level: str  # "REQUIRED", "RECOMMENDED", "OPTIONAL"

    # Core metrics
    halt_verified: bool = False
    wait_time_seconds: float | None = None
    approval_explicit: bool = False

    # VS metrics
    vs_options_presented: bool = False
    vs_options_count: int = 0
    t_scores_shown: bool = False
    t_score_range: tuple[float, float] | None = None

    # User selection
    user_selection: str | None = None
    selection_logged: bool = False

    def compute_score(self) -> float:
        """Compute checkpoint compliance score (0-100)."""
        score = 0.0

        # HALT verification (40 points for REQUIRED)
        if self.level == "REQUIRED":
            if self.halt_verified:
                score += 40
            if self.approval_explicit:
                score += 20
        else:
            if self.halt_verified:
                score += 30
            if self.approval_explicit:
                score += 15

        # VS alternatives (30 points)
        if self.vs_options_presented:
            score += 15
            if self.vs_options_count >= 3:
                score += 10
            elif self.vs_options_count >= 2:
                score += 5

        # T-Scores (10 points)
        if self.t_scores_shown:
            score += 10

        # Selection logging (10 points for REQUIRED)
        if self.level == "REQUIRED" and self.selection_logged:
            score += 10

        return min(score, 100)

    def is_passing(self) -> bool:
        """Check if checkpoint passed minimum requirements."""
        if self.level == "REQUIRED":
            return self.halt_verified and self.approval_explicit
        return True  # RECOMMENDED and OPTIONAL can pass without full compliance

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "checkpoint_id": self.checkpoint_id,
            "level": self.level,
            "halt_verified": self.halt_verified,
            "wait_time_seconds": self.wait_time_seconds,
            "approval_explicit": self.approval_explicit,
            "vs_options_presented": self.vs_options_presented,
            "vs_options_count": self.vs_options_count,
            "t_scores_shown": self.t_scores_shown,
            "t_score_range": list(self.t_score_range) if self.t_score_range else None,
            "user_selection": self.user_selection,
            "selection_logged": self.selection_logged,
            "score": self.compute_score(),
            "is_passing": self.is_passing(),
        }


@dataclass
class AgentMetrics:
    """Metrics for agent invocation accuracy."""
    agent_id: str
    model_tier: str  # Expected tier

    # Invocation tracking
    invoked: bool = False
    invoked_at: datetime | None = None
    response_time_seconds: float | None = None

    # Accuracy metrics
    trigger_keyword_matched: str | None = None
    correct_model_tier: bool = False
    execution_order_correct: bool = True

    # Response quality
    response_grade: GradeLevel = GradeLevel.C_ACCEPTABLE

    def compute_score(self) -> float:
        """Compute agent accuracy score (0-100)."""
        score = 0.0

        # Invocation (40 points)
        if self.invoked:
            score += 40

        # Correct model tier (30 points)
        if self.correct_model_tier:
            score += 30

        # Execution order (15 points)
        if self.execution_order_correct:
            score += 15

        # Response grade (15 points)
        grade_points = {
            GradeLevel.A_EXCELLENT: 15,
            GradeLevel.B_GOOD: 12,
            GradeLevel.C_ACCEPTABLE: 8,
            GradeLevel.D_POOR: 4,
            GradeLevel.F_FAIL: 0,
        }
        score += grade_points.get(self.response_grade, 0)

        return min(score, 100)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "agent_id": self.agent_id,
            "model_tier": self.model_tier,
            "invoked": self.invoked,
            "invoked_at": self.invoked_at.isoformat() if self.invoked_at else None,
            "response_time_seconds": self.response_time_seconds,
            "trigger_keyword_matched": self.trigger_keyword_matched,
            "correct_model_tier": self.correct_model_tier,
            "execution_order_correct": self.execution_order_correct,
            "response_grade": self.response_grade.value,
            "score": self.compute_score(),
        }


@dataclass
class VSQualityMetrics:
    """Metrics for VS Methodology quality."""
    # Option diversity
    options_presented: int = 0
    t_score_min: float = 1.0
    t_score_max: float = 0.0
    t_score_spread: float = 0.0

    # Modal avoidance
    modal_option_identified: bool = False
    modal_option_t_score: float | None = None
    modal_recommended_as_primary: bool = False  # Should be False

    # Creative options
    creative_options_count: int = 0  # T-Score <= 0.4
    experimental_options_count: int = 0  # T-Score < 0.2

    def compute_score(self) -> float:
        """Compute VS quality score (0-100)."""
        score = 0.0

        # Option diversity (30 points)
        if self.options_presented >= 3:
            score += 15
        elif self.options_presented >= 2:
            score += 10

        if self.t_score_spread >= 0.3:
            score += 15
        elif self.t_score_spread >= 0.2:
            score += 10

        # Modal avoidance (40 points)
        if self.modal_option_identified:
            score += 20
        if not self.modal_recommended_as_primary:
            score += 20

        # Creative options (30 points)
        if self.creative_options_count >= 1:
            score += 20
        if self.experimental_options_count >= 1:
            score += 10

        return min(score, 100)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "options_presented": self.options_presented,
            "t_score_min": self.t_score_min,
            "t_score_max": self.t_score_max,
            "t_score_spread": self.t_score_spread,
            "modal_option_identified": self.modal_option_identified,
            "modal_option_t_score": self.modal_option_t_score,
            "modal_recommended_as_primary": self.modal_recommended_as_primary,
            "creative_options_count": self.creative_options_count,
            "experimental_options_count": self.experimental_options_count,
            "score": self.compute_score(),
        }


@dataclass
class TestResult:
    """Complete test result for a scenario."""
    scenario_id: str
    timestamp: datetime = field(default_factory=datetime.now)

    # Checkpoint results
    checkpoint_results: list[CheckpointMetrics] = field(default_factory=list)

    # Agent results
    agent_results: list[AgentMetrics] = field(default_factory=list)

    # VS quality
    vs_quality: VSQualityMetrics = field(default_factory=VSQualityMetrics)

    # Overall metrics
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def compute_checkpoint_compliance(self) -> float:
        """Compute overall checkpoint compliance percentage."""
        if not self.checkpoint_results:
            return 100.0

        scores = [cp.compute_score() for cp in self.checkpoint_results]
        return sum(scores) / len(scores)

    def compute_agent_accuracy(self) -> float:
        """Compute overall agent accuracy percentage."""
        if not self.agent_results:
            return 100.0

        scores = [agent.compute_score() for agent in self.agent_results]
        return sum(scores) / len(scores)

    def compute_overall_score(self) -> float:
        """Compute weighted overall score."""
        checkpoint_score = self.compute_checkpoint_compliance()
        agent_score = self.compute_agent_accuracy()
        vs_score = self.vs_quality.compute_score()

        # Weights: Checkpoint 40%, Agent 35%, VS 25%
        return (checkpoint_score * 0.40) + (agent_score * 0.35) + (vs_score * 0.25)

    def get_grade(self) -> GradeLevel:
        """Get overall grade for the test."""
        # Check for critical failures
        for cp in self.checkpoint_results:
            if cp.level == "REQUIRED" and not cp.is_passing():
                return GradeLevel.F_FAIL

        return GradeLevel.from_score(self.compute_overall_score())

    def is_passing(self) -> bool:
        """Check if test passed overall."""
        # All REQUIRED checkpoints must pass
        for cp in self.checkpoint_results:
            if cp.level == "REQUIRED" and not cp.is_passing():
                return False

        # Overall score must be >= 70
        return self.compute_overall_score() >= 70

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "scenario_id": self.scenario_id,
            "timestamp": self.timestamp.isoformat(),
            "checkpoints": [cp.to_dict() for cp in self.checkpoint_results],
            "agents_invoked": [agent.to_dict() for agent in self.agent_results],
            "vs_quality": self.vs_quality.to_dict(),
            "metrics": {
                "checkpoint_compliance": f"{self.compute_checkpoint_compliance():.1f}%",
                "agent_accuracy": f"{self.compute_agent_accuracy():.1f}%",
                "vs_quality": f"{self.vs_quality.compute_score():.1f}%",
                "overall_score": f"{self.compute_overall_score():.1f}%",
                "overall_grade": self.get_grade().value,
            },
            "issues": self.issues,
            "warnings": self.warnings,
            "is_passing": self.is_passing(),
        }

    def to_yaml(self, output_path: Path | str) -> None:
        """Save result to YAML file."""
        output_path = Path(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True)

    def to_json(self, output_path: Path | str) -> None:
        """Save result to JSON file."""
        output_path = Path(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


@dataclass
class MetricsCollector:
    """Collects and aggregates metrics during test execution."""
    scenario_id: str
    start_time: datetime = field(default_factory=datetime.now)

    # Collected metrics
    _checkpoint_metrics: dict[str, CheckpointMetrics] = field(default_factory=dict)
    _agent_metrics: dict[str, AgentMetrics] = field(default_factory=dict)
    _vs_metrics: VSQualityMetrics = field(default_factory=VSQualityMetrics)
    _issues: list[str] = field(default_factory=list)
    _warnings: list[str] = field(default_factory=list)

    def record_checkpoint(
        self,
        checkpoint_id: str,
        level: str,
        halt_verified: bool = False,
        approval_explicit: bool = False,
        vs_options_count: int = 0,
        t_scores_shown: bool = False,
        t_score_range: tuple[float, float] | None = None,
        user_selection: str | None = None,
        wait_time_seconds: float | None = None,
    ) -> CheckpointMetrics:
        """Record checkpoint metrics."""
        metrics = CheckpointMetrics(
            checkpoint_id=checkpoint_id,
            level=level,
            halt_verified=halt_verified,
            approval_explicit=approval_explicit,
            vs_options_presented=vs_options_count > 0,
            vs_options_count=vs_options_count,
            t_scores_shown=t_scores_shown,
            t_score_range=t_score_range,
            user_selection=user_selection,
            selection_logged=user_selection is not None,
            wait_time_seconds=wait_time_seconds,
        )
        self._checkpoint_metrics[checkpoint_id] = metrics
        return metrics

    def record_agent(
        self,
        agent_id: str,
        model_tier: str,
        invoked: bool = True,
        response_time_seconds: float | None = None,
        correct_model_tier: bool = True,
        response_grade: GradeLevel = GradeLevel.C_ACCEPTABLE,
        trigger_keyword: str | None = None,
    ) -> AgentMetrics:
        """Record agent invocation metrics."""
        metrics = AgentMetrics(
            agent_id=agent_id,
            model_tier=model_tier,
            invoked=invoked,
            invoked_at=datetime.now() if invoked else None,
            response_time_seconds=response_time_seconds,
            correct_model_tier=correct_model_tier,
            response_grade=response_grade,
            trigger_keyword_matched=trigger_keyword,
        )
        self._agent_metrics[agent_id] = metrics
        return metrics

    def record_vs_quality(
        self,
        options_presented: int = 0,
        t_score_min: float = 1.0,
        t_score_max: float = 0.0,
        modal_identified: bool = False,
        modal_t_score: float | None = None,
        modal_recommended: bool = False,
    ) -> VSQualityMetrics:
        """Record VS quality metrics."""
        self._vs_metrics = VSQualityMetrics(
            options_presented=options_presented,
            t_score_min=t_score_min,
            t_score_max=t_score_max,
            t_score_spread=t_score_max - t_score_min,
            modal_option_identified=modal_identified,
            modal_option_t_score=modal_t_score,
            modal_recommended_as_primary=modal_recommended,
            creative_options_count=sum(1 for _ in range(options_presented) if t_score_min <= 0.4),
            experimental_options_count=sum(1 for _ in range(options_presented) if t_score_min < 0.2),
        )
        return self._vs_metrics

    def add_issue(self, issue: str) -> None:
        """Record a critical issue."""
        self._issues.append(issue)

    def add_warning(self, warning: str) -> None:
        """Record a warning."""
        self._warnings.append(warning)

    def finalize(self) -> TestResult:
        """Finalize and return test result."""
        return TestResult(
            scenario_id=self.scenario_id,
            timestamp=self.start_time,
            checkpoint_results=list(self._checkpoint_metrics.values()),
            agent_results=list(self._agent_metrics.values()),
            vs_quality=self._vs_metrics,
            issues=self._issues,
            warnings=self._warnings,
        )
