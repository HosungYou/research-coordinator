"""
Diverga Memory System v7.0 - Core Data Models

This module defines the core data structures for the Diverga Memory System,
which provides cross-session memory for research projects with checkpoint-based
state management.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class CheckpointLevel(str, Enum):
    """Priority level for checkpoints."""

    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


@dataclass
class CheckpointTrigger:
    """
    Definition of when a checkpoint should be activated.

    Attributes:
        type: Trigger type ('decision', 'file_exists', 'stage_entry', 'manual')
        path: File path for file_exists triggers
        decision_key: Decision key for decision triggers
    """

    type: str  # 'decision', 'file_exists', 'stage_entry', 'manual'
    path: Optional[str] = None
    decision_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CheckpointTrigger:
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Checkpoint:
    """
    Checkpoint definition in the research pipeline.

    Checkpoints are save points that capture research decisions and project state.
    They can be required, recommended, or optional based on the research methodology.

    Attributes:
        id: Unique checkpoint identifier (e.g., 'THEORY_SELECTION')
        name: Human-readable checkpoint name
        level: Priority level (required/recommended/optional)
        icon: Visual indicator emoji
        stage: Research stage this checkpoint belongs to
        agents: List of agent IDs that interact with this checkpoint
        triggers: Conditions that activate this checkpoint
        validation: Validation rules for checkpoint completion
        persistence: Storage configuration (memory/notepad/both)
    """

    id: str
    name: str
    level: CheckpointLevel
    icon: str
    stage: str
    agents: List[str] = field(default_factory=list)
    triggers: List[CheckpointTrigger] = field(default_factory=list)
    validation: Dict[str, Any] = field(default_factory=dict)
    persistence: str = "memory"  # 'memory', 'notepad', 'both'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['level'] = self.level.value
        data['triggers'] = [t.to_dict() for t in self.triggers]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Checkpoint:
        """Create from dictionary."""
        data = data.copy()
        data['level'] = CheckpointLevel(data['level'])
        data['triggers'] = [
            CheckpointTrigger.from_dict(t) for t in data.get('triggers', [])
        ]
        return cls(**data)


@dataclass
class Decision:
    """
    A research decision made at a checkpoint.

    Decisions capture key choices made during the research process, including
    the selected option, alternatives considered, and rationale.

    Attributes:
        checkpoint_id: ID of the checkpoint where decision was made
        stage: Research stage when decision was made
        agent_id: Agent that facilitated the decision
        selected: The chosen option
        alternatives: Other options that were considered
        rationale: Explanation for the choice
        user_confirmed: Whether user explicitly confirmed the decision
        timestamp: When the decision was made
        amendments: List of subsequent amendments to this decision
    """

    checkpoint_id: str
    stage: str
    agent_id: str
    selected: Union[str, List[str], Dict[str, Any]]
    alternatives: List[Union[str, Dict[str, Any]]] = field(default_factory=list)
    rationale: str = ""
    user_confirmed: bool = False
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    amendments: List[Amendment] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['amendments'] = [a.to_dict() for a in self.amendments]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Decision:
        """Create from dictionary."""
        data = data.copy()
        data['amendments'] = [
            Amendment.from_dict(a) for a in data.get('amendments', [])
        ]
        return cls(**data)


@dataclass
class Amendment:
    """
    An amendment to a previous decision.

    Amendments track changes to decisions over time, preserving the history
    of how research design evolved.

    Attributes:
        decision_id: ID of the decision being amended (checkpoint_id)
        new_selected: Updated selection
        new_rationale: Explanation for the change
        amended_by: Agent or user who made the amendment
        timestamp: When the amendment was made
    """

    decision_id: str
    new_selected: Union[str, List[str], Dict[str, Any]]
    new_rationale: str
    amended_by: str = "user"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Amendment:
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ContextInjection:
    """
    Context to inject into agent prompts.

    Context injections ensure agents have access to relevant past decisions
    and project state when making new recommendations.

    Attributes:
        checkpoint_id: Source checkpoint for this context
        stage: Research stage this context relates to
        summary: Brief summary of the context
        full_context: Complete context details
        priority: Importance level (high/medium/low)
    """

    checkpoint_id: str
    stage: str
    summary: str
    full_context: Dict[str, Any]
    priority: str = "medium"  # 'high', 'medium', 'low'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ContextInjection:
        """Create from dictionary."""
        return cls(**data)


@dataclass
class SessionData:
    """
    Information about a research session.

    Sessions represent distinct periods of work on a research project.

    Attributes:
        session_id: Unique session identifier
        start_time: Session start timestamp
        end_time: Session end timestamp
        checkpoints_reached: List of checkpoint IDs reached in this session
        decisions_made: List of decision checkpoint IDs
        agents_invoked: List of agent IDs used
        summary: Brief session summary
    """

    session_id: str
    start_time: str
    end_time: Optional[str] = None
    checkpoints_reached: List[str] = field(default_factory=list)
    decisions_made: List[str] = field(default_factory=list)
    agents_invoked: List[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SessionData:
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ResearchContext:
    """
    Complete context for a research project.

    This is the main data structure that gets persisted across sessions,
    providing continuity and memory for long-running research projects.

    Attributes:
        project_name: Name of the research project
        research_question: Primary research question
        paradigm: Research paradigm (quantitative/qualitative/mixed)
        current_stage: Current stage in the research pipeline
        recent_decisions: Recent checkpoint decisions (kept in memory)
        pending_checkpoints: Checkpoints waiting for completion
        last_session_summary: Summary of the most recent session
        created_at: Project creation timestamp
        updated_at: Last update timestamp
        sessions: Historical session data
        all_decisions: Complete decision history
    """

    project_name: str
    research_question: str
    paradigm: str = "quantitative"  # 'quantitative', 'qualitative', 'mixed'
    current_stage: str = "A"  # A=Theory, B=Literature, C=Methodology, etc.
    recent_decisions: List[Decision] = field(default_factory=list)
    pending_checkpoints: List[str] = field(default_factory=list)
    last_session_summary: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    sessions: List[SessionData] = field(default_factory=list)
    all_decisions: Dict[str, Decision] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization."""
        data = asdict(self)
        data['recent_decisions'] = [d.to_dict() for d in self.recent_decisions]
        data['sessions'] = [s.to_dict() for s in self.sessions]
        data['all_decisions'] = {k: v.to_dict() for k, v in self.all_decisions.items()}
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ResearchContext:
        """Create from dictionary."""
        data = data.copy()
        data['recent_decisions'] = [
            Decision.from_dict(d) for d in data.get('recent_decisions', [])
        ]
        data['sessions'] = [
            SessionData.from_dict(s) for s in data.get('sessions', [])
        ]
        data['all_decisions'] = {
            k: Decision.from_dict(v)
            for k, v in data.get('all_decisions', {}).items()
        }
        return cls(**data)

    def add_decision(self, decision: Decision) -> None:
        """
        Add a new decision to the context.

        Args:
            decision: Decision to add
        """
        self.all_decisions[decision.checkpoint_id] = decision
        self.recent_decisions.append(decision)
        # Keep only last 10 decisions in memory
        if len(self.recent_decisions) > 10:
            self.recent_decisions = self.recent_decisions[-10:]
        self.updated_at = datetime.utcnow().isoformat()

    def amend_decision(
        self,
        checkpoint_id: str,
        new_selected: Union[str, List[str], Dict[str, Any]],
        new_rationale: str,
        amended_by: str = "user"
    ) -> None:
        """
        Amend an existing decision.

        Args:
            checkpoint_id: ID of the checkpoint to amend
            new_selected: New selection value
            new_rationale: Explanation for the change
            amended_by: Who made the amendment
        """
        if checkpoint_id in self.all_decisions:
            decision = self.all_decisions[checkpoint_id]
            amendment = Amendment(
                decision_id=checkpoint_id,
                new_selected=new_selected,
                new_rationale=new_rationale,
                amended_by=amended_by
            )
            decision.amendments.append(amendment)
            decision.selected = new_selected
            decision.rationale = new_rationale
            self.updated_at = datetime.utcnow().isoformat()

    def get_decision(self, checkpoint_id: str) -> Optional[Decision]:
        """
        Retrieve a decision by checkpoint ID.

        Args:
            checkpoint_id: Checkpoint identifier

        Returns:
            Decision if found, None otherwise
        """
        return self.all_decisions.get(checkpoint_id)

    def get_stage_decisions(self, stage: str) -> List[Decision]:
        """
        Get all decisions for a specific research stage.

        Args:
            stage: Stage identifier (A, B, C, etc.)

        Returns:
            List of decisions from that stage
        """
        return [
            d for d in self.all_decisions.values()
            if d.stage == stage
        ]

    def start_session(self) -> SessionData:
        """
        Start a new research session.

        Returns:
            New SessionData object
        """
        session = SessionData(
            session_id=f"session_{len(self.sessions) + 1}",
            start_time=datetime.utcnow().isoformat()
        )
        self.sessions.append(session)
        return session

    def end_session(self, summary: str = "") -> None:
        """
        End the current session.

        Args:
            summary: Session summary
        """
        if self.sessions:
            current_session = self.sessions[-1]
            current_session.end_time = datetime.utcnow().isoformat()
            current_session.summary = summary
            self.last_session_summary = summary
            self.updated_at = datetime.utcnow().isoformat()
