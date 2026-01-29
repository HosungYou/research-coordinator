"""
Diverga QA Scenario Definitions
================================

Defines test scenario structures for comprehensive Diverga plugin testing.
Scenarios cover all major research paradigms and workflows.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any
import yaml


class Paradigm(Enum):
    """Research paradigm types."""
    QUANTITATIVE = "quantitative"
    QUALITATIVE = "qualitative"
    MIXED_METHODS = "mixed_methods"
    ANY = "any"


class CheckpointLevel(Enum):
    """Checkpoint severity levels - determines HALT behavior."""
    REQUIRED = "REQUIRED"      # 🔴 System MUST STOP
    RECOMMENDED = "RECOMMENDED"  # 🟠 System SHOULD STOP
    OPTIONAL = "OPTIONAL"      # 🟡 System ASKS


class Priority(Enum):
    """Test scenario priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class VSOption:
    """Represents a VS methodology option presented to user."""
    label: str
    description: str
    t_score: float
    t_score_range: tuple[float, float] | None = None
    recommended: bool = False

    def validate_t_score(self) -> bool:
        """Check if T-Score is within expected range."""
        if self.t_score_range:
            return self.t_score_range[0] <= self.t_score <= self.t_score_range[1]
        return 0.0 <= self.t_score <= 1.0


@dataclass
class CheckpointExpectation:
    """Expected checkpoint behavior in a scenario."""
    checkpoint_id: str
    level: CheckpointLevel

    # Validation criteria
    must_halt: bool = True
    must_present_alternatives: bool = True
    min_alternatives: int = 2
    must_show_t_scores: bool = True
    must_wait_approval: bool = True
    must_summarize_design: bool = False
    allows_revision: bool = True

    # VS Options (if alternatives expected)
    expected_options: list[VSOption] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "checkpoint_id": self.checkpoint_id,
            "level": self.level.value,
            "must_halt": self.must_halt,
            "must_present_alternatives": self.must_present_alternatives,
            "min_alternatives": self.min_alternatives,
            "must_show_t_scores": self.must_show_t_scores,
            "must_wait_approval": self.must_wait_approval,
            "must_summarize_design": self.must_summarize_design,
            "allows_revision": self.allows_revision,
        }


@dataclass
class AgentExpectation:
    """Expected agent invocation in a scenario."""
    agent_id: str  # e.g., "diverga:c5" or "C5-MetaAnalysisMaster"
    model_tier: str  # "opus", "sonnet", "haiku"
    trigger_keywords: list[str] = field(default_factory=list)
    must_be_invoked: bool = True
    execution_order: int | None = None  # For sequential execution
    parallel_group: str | None = None   # For parallel execution

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "agent_id": self.agent_id,
            "model_tier": self.model_tier,
            "trigger_keywords": self.trigger_keywords,
            "must_be_invoked": self.must_be_invoked,
            "execution_order": self.execution_order,
            "parallel_group": self.parallel_group,
        }


@dataclass
class ExpectedBehavior:
    """Expected system behavior after a conversation turn."""
    paradigm_detection: Paradigm | None = None
    keyword_matches: list[str] = field(default_factory=list)
    checkpoint_trigger: str | None = None
    agent_invoked: str | None = None
    model_tier: str | None = None
    decision_logged: bool = False

    # Response requirements
    explicit_wait: bool = True
    no_auto_proceed: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "paradigm_detection": self.paradigm_detection.value if self.paradigm_detection else None,
            "keyword_matches": self.keyword_matches,
            "checkpoint_trigger": self.checkpoint_trigger,
            "agent_invoked": self.agent_invoked,
            "model_tier": self.model_tier,
            "decision_logged": self.decision_logged,
            "explicit_wait": self.explicit_wait,
            "no_auto_proceed": self.no_auto_proceed,
        }


@dataclass
class ExpectedResponseElements:
    """Expected elements in AI response."""
    vs_alternatives: list[VSOption] = field(default_factory=list)
    explicit_wait: bool = True
    no_auto_proceed: bool = True
    design_summary: bool = False
    t_score_range: tuple[float, float] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "vs_alternatives": [
                {"label": opt.label, "t_score": opt.t_score, "recommended": opt.recommended}
                for opt in self.vs_alternatives
            ],
            "explicit_wait": self.explicit_wait,
            "no_auto_proceed": self.no_auto_proceed,
            "design_summary": self.design_summary,
            "t_score_range": list(self.t_score_range) if self.t_score_range else None,
        }


@dataclass
class ConversationTurn:
    """Single turn in a test conversation."""
    turn_number: int
    user_input: str
    expected_behaviors: ExpectedBehavior
    expected_response_elements: ExpectedResponseElements

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "turn": self.turn_number,
            "user_input": self.user_input,
            "expected_behaviors": self.expected_behaviors.to_dict(),
            "expected_response_elements": self.expected_response_elements.to_dict(),
        }


@dataclass
class Scenario:
    """Complete test scenario definition."""
    scenario_id: str
    name: str
    description: str
    paradigm: Paradigm
    priority: Priority

    # Agent expectations
    agents_primary: list[AgentExpectation] = field(default_factory=list)
    agents_secondary: list[AgentExpectation] = field(default_factory=list)

    # Checkpoint expectations
    checkpoints_required: list[CheckpointExpectation] = field(default_factory=list)
    checkpoints_recommended: list[CheckpointExpectation] = field(default_factory=list)

    # Conversation flow
    conversation_flow: list[ConversationTurn] = field(default_factory=list)

    # Metadata
    tags: list[str] = field(default_factory=list)
    estimated_duration_minutes: int = 10

    @classmethod
    def from_yaml(cls, yaml_path: Path | str) -> "Scenario":
        """Load scenario from YAML file."""
        yaml_path = Path(yaml_path)
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scenario":
        """Create scenario from dictionary."""
        scenario_data = data.get("scenario", data)

        # Parse paradigm
        paradigm = Paradigm(scenario_data.get("paradigm", "any"))
        priority = Priority(scenario_data.get("priority", "medium"))

        # Parse agents
        agents_expected = data.get("agents_expected", {})
        agents_primary = []
        if primary := agents_expected.get("primary"):
            if isinstance(primary, str):
                agents_primary = [AgentExpectation(agent_id=primary, model_tier="opus")]
            elif isinstance(primary, list):
                agents_primary = [
                    AgentExpectation(agent_id=a, model_tier="opus") for a in primary
                ]

        agents_secondary = []
        if secondary := agents_expected.get("secondary"):
            agents_secondary = [
                AgentExpectation(agent_id=a, model_tier="sonnet") for a in secondary
            ]

        # Parse checkpoints
        checkpoints_required = []
        for cp_data in data.get("checkpoints_required", []):
            checkpoints_required.append(CheckpointExpectation(
                checkpoint_id=cp_data.get("id", ""),
                level=CheckpointLevel.REQUIRED,
                must_halt=cp_data.get("validation", {}).get("must_halt", True),
                must_present_alternatives=cp_data.get("validation", {}).get("must_present_alternatives", True),
                min_alternatives=cp_data.get("validation", {}).get("min_alternatives", 3),
                must_show_t_scores=cp_data.get("validation", {}).get("must_show_t_scores", True),
                must_wait_approval=cp_data.get("validation", {}).get("must_wait_approval", True),
                must_summarize_design=cp_data.get("validation", {}).get("must_summarize_design", False),
            ))

        # Parse conversation flow
        conversation_flow = []
        for turn_data in data.get("conversation_flow", []):
            behaviors = turn_data.get("expected_behaviors", {})
            paradigm_str = behaviors.get("paradigm_detection")

            expected_behaviors = ExpectedBehavior(
                paradigm_detection=Paradigm(paradigm_str) if paradigm_str else None,
                keyword_matches=behaviors.get("keyword_matches", []),
                checkpoint_trigger=behaviors.get("checkpoint_trigger"),
                agent_invoked=behaviors.get("agent_invoked"),
                model_tier=behaviors.get("model_tier"),
                decision_logged=behaviors.get("decision_logged", False),
                explicit_wait=behaviors.get("explicit_wait", True),
                no_auto_proceed=behaviors.get("no_auto_proceed", True),
            )

            elements_data = turn_data.get("expected_response_elements", {})
            vs_alternatives = []
            for opt_key, opt_data in elements_data.get("vs_alternatives", {}).items():
                if isinstance(opt_data, dict):
                    t_range = opt_data.get("t_score_range")
                    vs_alternatives.append(VSOption(
                        label=opt_data.get("label", ""),
                        description=opt_data.get("description", ""),
                        t_score=(t_range[0] + t_range[1]) / 2 if t_range else 0.5,
                        t_score_range=tuple(t_range) if t_range else None,
                        recommended=opt_data.get("recommended", False),
                    ))

            expected_response = ExpectedResponseElements(
                vs_alternatives=vs_alternatives,
                explicit_wait=elements_data.get("explicit_wait", True),
                no_auto_proceed=elements_data.get("no_auto_proceed", True),
                design_summary=elements_data.get("design_summary", False),
            )

            conversation_flow.append(ConversationTurn(
                turn_number=turn_data.get("turn", 1),
                user_input=turn_data.get("user_input", ""),
                expected_behaviors=expected_behaviors,
                expected_response_elements=expected_response,
            ))

        return cls(
            scenario_id=scenario_data.get("id", ""),
            name=scenario_data.get("name", ""),
            description=scenario_data.get("description", ""),
            paradigm=paradigm,
            priority=priority,
            agents_primary=agents_primary,
            agents_secondary=agents_secondary,
            checkpoints_required=checkpoints_required,
            checkpoints_recommended=[],
            conversation_flow=conversation_flow,
            tags=data.get("tags", []),
            estimated_duration_minutes=data.get("estimated_duration_minutes", 10),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "scenario": {
                "id": self.scenario_id,
                "name": self.name,
                "description": self.description,
                "paradigm": self.paradigm.value,
                "priority": self.priority.value,
            },
            "agents_expected": {
                "primary": [a.agent_id for a in self.agents_primary],
                "secondary": [a.agent_id for a in self.agents_secondary],
            },
            "checkpoints_required": [cp.to_dict() for cp in self.checkpoints_required],
            "checkpoints_recommended": [cp.to_dict() for cp in self.checkpoints_recommended],
            "conversation_flow": [turn.to_dict() for turn in self.conversation_flow],
            "tags": self.tags,
            "estimated_duration_minutes": self.estimated_duration_minutes,
        }

    def to_yaml(self, output_path: Path | str) -> None:
        """Save scenario to YAML file."""
        output_path = Path(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True)


def load_scenario(scenario_id: str) -> Scenario:
    """Load a scenario by ID from the protocol directory."""
    protocol_dir = Path(__file__).parent

    # Try to find matching YAML file
    for yaml_file in protocol_dir.glob("test_*.yaml"):
        scenario = Scenario.from_yaml(yaml_file)
        if scenario.scenario_id == scenario_id:
            return scenario

    raise ValueError(f"Scenario not found: {scenario_id}")


def list_scenarios() -> list[tuple[str, str, Priority]]:
    """List all available test scenarios."""
    protocol_dir = Path(__file__).parent
    scenarios = []

    for yaml_file in protocol_dir.glob("test_*.yaml"):
        try:
            scenario = Scenario.from_yaml(yaml_file)
            scenarios.append((scenario.scenario_id, scenario.name, scenario.priority))
        except Exception as e:
            print(f"Warning: Could not load {yaml_file}: {e}")

    return scenarios
