"""
Diverga Memory System v7.0 - Session Lifecycle Hooks

This module implements session lifecycle management for research projects,
providing context injection at session start and state persistence at session end.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import uuid
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from .models import ContextInjection
    from .fs_state import FilesystemState
except ImportError:
    from models import ContextInjection
    from fs_state import FilesystemState


class SessionHooks:
    """
    Manages session lifecycle for research projects.

    Handles:
    - Session start: Load context from .research/ state files
    - Session end: Generate summary and save session data
    - Context injection: Provide relevant context to agents
    - Session tracking: Maintain session history

    Attributes:
        project_root: Root directory of the research project
        fs_state: FilesystemState instance for state management
        current_session_id: ID of the current session
        session_data: Data accumulated during current session
    """

    def __init__(self, project_root: Path):
        """
        Initialize SessionHooks with project root.

        Args:
            project_root: Root directory of the research project
        """
        self.project_root = Path(project_root)
        self.fs_state = FilesystemState(project_root)
        self.current_session_id: Optional[str] = None
        self.session_data: Dict[str, Any] = {}

    def on_session_start(self) -> ContextInjection:
        """
        Called at session start to load and inject context.

        Loads:
        - Project state from .research/project-state.yaml
        - Checkpoint states from .research/checkpoints.yaml
        - Recent decisions (last 5) from .research/decision-log.yaml
        - Detected current stage from filesystem

        Returns:
            ContextInjection object with all relevant context
        """
        # Generate new session ID
        self.current_session_id = str(uuid.uuid4())

        # Load project state
        project_state = self.fs_state.get_project_state()

        # Detect current stage from filesystem
        current_stage = self._detect_current_stage()

        # Load checkpoint states
        checkpoints_data = self._load_checkpoints()

        # Load recent decisions
        recent_decisions = self._load_recent_decisions(limit=5)

        # Build full context dictionary
        full_context = {
            "session_id": self.current_session_id,
            "project_name": project_state.get("project_name", "Unknown Project"),
            "research_question": project_state.get("research_question", ""),
            "paradigm": project_state.get("paradigm", "quantitative"),
            "current_stage": current_stage,
            "created_at": project_state.get("created_at", ""),
            "last_updated": project_state.get("last_updated", ""),
            "pending_checkpoints": self._get_pending_checkpoints(checkpoints_data),
            "last_checkpoint": self._get_last_checkpoint(checkpoints_data),
            "recent_decisions": recent_decisions,
            "session_count": len(project_state.get("sessions", [])),
        }

        # Generate context summary
        summary = self._generate_context_summary(full_context)

        # Initialize session tracking
        self.session_data = {
            "session_id": self.current_session_id,
            "started_at": datetime.utcnow().isoformat() + "Z",
            "stage_on_entry": current_stage,
            "decisions_made": [],
            "checkpoints_passed": [],
            "agents_invoked": [],
        }

        # Create ContextInjection object
        context_injection = ContextInjection(
            checkpoint_id="SESSION_START",
            stage=current_stage,
            summary=summary,
            full_context=full_context,
            priority="high",
        )

        return context_injection

    def on_session_end(self, session_id: str) -> None:
        """
        Called at session end to save session data.

        Performs:
        - Generate session summary
        - Save session file to .research/sessions/
        - Update project state with last_updated timestamp
        - Record checkpoints passed during session
        - Record decisions made during session

        Args:
            session_id: ID of the session ending
        """
        if session_id != self.current_session_id:
            print(f"Warning: Session ID mismatch ({session_id} vs {self.current_session_id})")

        # Generate session summary
        summary = self.generate_session_summary()

        # Update session data
        self.session_data["ended_at"] = datetime.utcnow().isoformat() + "Z"
        self.session_data["summary"] = summary
        self.session_data["stage_on_exit"] = self._detect_current_stage()

        # Save session file
        session_file = (
            self.project_root
            / ".research"
            / "sessions"
            / f"session-{self.current_session_id}.yaml"
        )

        session_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(session_file, "w", encoding="utf-8") as f:
                f.write("# Diverga Session Log v7.0\n")
                f.write(f"# Session ID: {self.current_session_id}\n")
                f.write(f"# Duration: {self.session_data['started_at']} - {self.session_data['ended_at']}\n\n")

                yaml.safe_dump(
                    self.session_data,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                )
        except Exception as e:
            print(f"Warning: Failed to save session file: {e}")

        # Update project state
        project_state = self.fs_state.get_project_state()

        # Add session to sessions list
        session_summary = {
            "session_id": self.current_session_id,
            "started_at": self.session_data["started_at"],
            "ended_at": self.session_data["ended_at"],
            "summary": summary,
            "decisions_count": len(self.session_data["decisions_made"]),
            "checkpoints_count": len(self.session_data["checkpoints_passed"]),
        }

        if "sessions" not in project_state:
            project_state["sessions"] = []

        project_state["sessions"].append(session_summary)

        # Keep only last 20 sessions in project-state.yaml
        if len(project_state["sessions"]) > 20:
            project_state["sessions"] = project_state["sessions"][-20:]

        # Update timestamp
        project_state["last_updated"] = datetime.utcnow().isoformat() + "Z"

        # Save updated project state
        self.fs_state.update_project_state(project_state)

        # Clear current session
        self.current_session_id = None
        self.session_data = {}

    def generate_session_summary(self) -> str:
        """
        Auto-generate session summary based on session data.

        Generates a concise summary of what happened during the session,
        including agents invoked, decisions made, and checkpoints passed.

        Returns:
            Session summary string (supports Korean text)
        """
        parts = []

        # Session info
        stage_entry = self.session_data.get("stage_on_entry", "unknown")
        stage_exit = self.session_data.get("stage_on_exit", stage_entry)

        if stage_entry == stage_exit:
            parts.append(f"Research stage: {stage_entry}")
        else:
            parts.append(f"Stage progression: {stage_entry} → {stage_exit}")

        # Agents invoked
        agents = self.session_data.get("agents_invoked", [])
        if agents:
            unique_agents = list(set(agents))
            parts.append(f"Agents used: {', '.join(unique_agents)}")

        # Decisions made
        decisions = self.session_data.get("decisions_made", [])
        if decisions:
            parts.append(f"Decisions made: {len(decisions)}")

        # Checkpoints passed
        checkpoints = self.session_data.get("checkpoints_passed", [])
        if checkpoints:
            parts.append(f"Checkpoints passed: {', '.join(checkpoints)}")

        # If nothing happened, return minimal summary
        if not parts:
            return "Session completed with no major actions recorded."

        return " | ".join(parts)

    def get_last_session(self) -> Optional[dict]:
        """
        Get the most recent session data.

        Returns:
            Session dictionary if found, None otherwise
        """
        session_files = self.fs_state.get_session_files()

        if not session_files:
            return None

        # Get most recent session file
        latest_session_file = session_files[0]

        try:
            with open(latest_session_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Failed to load session file: {e}")
            return None

    def get_session(self, session_id: str) -> Optional[dict]:
        """
        Get specific session by ID.

        Args:
            session_id: Session ID to retrieve

        Returns:
            Session dictionary if found, None otherwise
        """
        session_file = (
            self.project_root / ".research" / "sessions" / f"session-{session_id}.yaml"
        )

        if not session_file.exists():
            return None

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Failed to load session file: {e}")
            return None

    def record_decision(self, decision_id: str) -> None:
        """
        Record a decision made during this session.

        Args:
            decision_id: ID of the decision (e.g., "dec-001")
        """
        if self.current_session_id and decision_id not in self.session_data.get("decisions_made", []):
            self.session_data.setdefault("decisions_made", []).append(decision_id)

    def record_checkpoint(self, checkpoint_id: str) -> None:
        """
        Record a checkpoint passed during this session.

        Args:
            checkpoint_id: ID of the checkpoint (e.g., "CP_RESEARCH_DIRECTION")
        """
        if self.current_session_id and checkpoint_id not in self.session_data.get("checkpoints_passed", []):
            self.session_data.setdefault("checkpoints_passed", []).append(checkpoint_id)

    def record_agent(self, agent_id: str) -> None:
        """
        Record an agent invoked during this session.

        Args:
            agent_id: ID of the agent (e.g., "A1", "B5", "C5")
        """
        if self.current_session_id:
            self.session_data.setdefault("agents_invoked", []).append(agent_id)

    def _detect_current_stage(self) -> str:
        """
        Internal method to detect current stage from filesystem.

        Uses FilesystemState.detect_current_stage() to determine stage
        from .research/changes/current/ indicator files.

        Returns:
            Stage name (foundation, evidence, design, collection,
                       analysis, quality, communication)
        """
        return self.fs_state.detect_current_stage()

    def _load_checkpoints(self) -> dict:
        """
        Load checkpoint data from .research/checkpoints.yaml.

        Returns:
            Dictionary with checkpoint data, or empty dict if not found
        """
        checkpoints_file = self.project_root / ".research" / "checkpoints.yaml"

        if not checkpoints_file.exists():
            return {"checkpoints": {}, "completed": [], "pending": []}

        try:
            with open(checkpoints_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load checkpoints: {e}")
            return {"checkpoints": {}, "completed": [], "pending": []}

    def _load_recent_decisions(self, limit: int = 5) -> List[dict]:
        """
        Load recent decisions from .research/decision-log.yaml.

        Args:
            limit: Maximum number of decisions to return

        Returns:
            List of decision dictionaries, ordered by timestamp (newest first)
        """
        decision_file = self.project_root / ".research" / "decision-log.yaml"

        if not decision_file.exists():
            return []

        try:
            with open(decision_file, "r", encoding="utf-8") as f:
                decision_data = yaml.safe_load(f) or {}

            decisions = decision_data.get("decisions", [])

            # Sort by timestamp (newest first)
            decisions.sort(
                key=lambda d: d.get("timestamp", ""), reverse=True
            )

            return decisions[:limit]

        except Exception as e:
            print(f"Warning: Failed to load decisions: {e}")
            return []

    def _get_last_checkpoint(self, checkpoints: dict) -> Optional[str]:
        """
        Get the last passed checkpoint.

        Args:
            checkpoints: Checkpoint data dictionary

        Returns:
            Checkpoint ID if found, None otherwise
        """
        completed = checkpoints.get("completed", [])

        if not completed:
            return None

        # Return most recent checkpoint
        if isinstance(completed, list) and completed:
            # If completed is a list of dicts with timestamps
            if isinstance(completed[0], dict):
                sorted_checkpoints = sorted(
                    completed, key=lambda c: c.get("timestamp", ""), reverse=True
                )
                return sorted_checkpoints[0].get("id")
            # If completed is a simple list of checkpoint IDs
            else:
                return completed[-1]

        return None

    def _get_pending_checkpoints(self, checkpoints: dict) -> List[str]:
        """
        Get list of pending checkpoints.

        Args:
            checkpoints: Checkpoint data dictionary

        Returns:
            List of pending checkpoint IDs
        """
        pending = checkpoints.get("pending", [])

        if isinstance(pending, list):
            return pending

        return []

    def _generate_context_summary(self, context: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the context.

        Args:
            context: Full context dictionary

        Returns:
            Summary string (supports Korean text)
        """
        parts = []

        # Project info
        project_name = context.get("project_name", "Unknown")
        parts.append(f"Project: {project_name}")

        # Research question
        rq = context.get("research_question", "")
        if rq:
            parts.append(f"RQ: {rq}")

        # Current stage
        stage = context.get("current_stage", "foundation")
        parts.append(f"Stage: {stage}")

        # Paradigm
        paradigm = context.get("paradigm", "quantitative")
        parts.append(f"Paradigm: {paradigm}")

        # Recent activity
        session_count = context.get("session_count", 0)
        if session_count > 0:
            parts.append(f"Sessions: {session_count}")

        # Pending checkpoints
        pending = context.get("pending_checkpoints", [])
        if pending:
            parts.append(f"Pending: {', '.join(pending)}")

        return " | ".join(parts)
