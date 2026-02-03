"""Simplified data models for Task Interceptor (Layer 2).

These models are specifically for task interception and context injection,
separate from the full Diverga Memory System v7.0 models.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class ProjectState:
    """Current project state."""
    project_id: str
    stage: str
    created_at: str
    last_updated: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Decision:
    """Research decision record."""
    timestamp: str
    agent_id: str
    decision: str
    rationale: str
    impact: str
    checkpoint_triggered: Optional[str] = None


@dataclass
class CheckpointState:
    """Checkpoint state record."""
    id: str
    status: str  # "pending", "active", "completed", "skipped"
    triggered_at: Optional[str] = None
    completed_at: Optional[str] = None
    triggered_by: Optional[str] = None
    validation_result: Optional[Dict[str, Any]] = None


@dataclass
class ResearchContext:
    """Complete research context for agent injection."""
    project_state: ProjectState
    recent_decisions: List[Decision]
    checkpoints: Dict[str, CheckpointState]
    current_stage: str

    def to_prompt_section(self) -> str:
        """Convert context to prompt injection format."""
        sections = []

        # Project state
        sections.append("## Current Research Context")
        sections.append(f"Project: {self.project_state.project_id}")
        sections.append(f"Stage: {self.current_stage}")
        sections.append(f"Last Updated: {self.project_state.last_updated}")

        # Recent decisions
        if self.recent_decisions:
            sections.append("\n## Recent Decisions (Last 5)")
            for dec in self.recent_decisions[:5]:
                sections.append(f"- [{dec.timestamp}] {dec.agent_id}: {dec.decision}")
                if dec.checkpoint_triggered:
                    sections.append(f"  → Triggered: {dec.checkpoint_triggered}")

        # Pending checkpoints
        pending = [
            (cp_id, cp) for cp_id, cp in self.checkpoints.items()
            if cp.status in ["pending", "active"]
        ]
        if pending:
            sections.append("\n## Active Checkpoints")
            for cp_id, cp in pending:
                sections.append(f"- {cp_id} ({cp.status})")
                if cp.triggered_at:
                    sections.append(f"  Triggered: {cp.triggered_at}")

        return "\n".join(sections)
