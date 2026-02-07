"""Checkpoint trigger detection and management for Diverga Memory System v7.0.

This module implements auto-trigger detection for PRISMA checkpoints in the systematic review pipeline.
Checkpoints enforce human decision gates at critical research stages.
"""

import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None  # Graceful fallback if PyYAML not available

try:
    from .task_interceptor_models import CheckpointState
except ImportError:
    from task_interceptor_models import CheckpointState


class Checkpoint:
    """Checkpoint definition with trigger conditions and behavior rules."""

    def __init__(self, checkpoint_id: str, config: Dict[str, Any]):
        self.id = checkpoint_id
        self.level = config.get("level", "OPTIONAL")  # REQUIRED, RECOMMENDED, OPTIONAL
        self.agent = config.get("agent", "")
        self.stage = config.get("stage", 0)
        self.description = config.get("description", "")
        self.trigger_conditions = config.get("trigger_conditions", [])
        self.presentation_format = config.get("presentation_format", "")
        self.required_response = config.get("required_response", {})
        self.on_approval = config.get("on_approval", [])
        self.on_rejection = config.get("on_rejection", [])
        self.on_skip = config.get("on_skip", [])

    def get_emoji(self) -> str:
        """Return emoji based on checkpoint level."""
        emoji_map = {
            "REQUIRED": "🔴",
            "RECOMMENDED": "🟠",
            "OPTIONAL": "🟡"
        }
        return emoji_map.get(self.level, "🔵")

    def is_critical(self) -> bool:
        """Check if checkpoint is critical (REQUIRED level)."""
        return self.level == "REQUIRED"

    def format_options(self) -> str:
        """Format checkpoint options for display."""
        options = self.required_response.get("options", [])
        if not options:
            return ""

        formatted = ["Options:"]
        for i, opt in enumerate(options, 1):
            formatted.append(f"  [{i}] {opt}")
        return "\n".join(formatted)


class CheckpointTrigger:
    """Detects and manages checkpoint triggers from agent actions and filesystem state."""

    def __init__(self, project_root: Path):
        """Initialize checkpoint trigger system.

        Args:
            project_root: Root directory of the research project
        """
        self.project_root = Path(project_root)
        self.checkpoints: List[Checkpoint] = []
        self.state_file = self.project_root / ".claude" / "state" / "review-checkpoints.json"
        self._load_checkpoints()
        self._load_state()

    def _load_checkpoints(self) -> None:
        """Load checkpoint definitions from YAML file."""
        # Try multiple possible locations for checkpoints.yaml
        possible_paths = [
            self.project_root / ".research" / "checkpoints.yaml",
            self.project_root / ".claude" / "checkpoints" / "review-checkpoints.yaml",
            Path("/Volumes/External SSD/Projects/Diverga/.claude/checkpoints/review-checkpoints.yaml"),
        ]

        checkpoint_data = None
        for yaml_path in possible_paths:
            if yaml_path.exists():
                try:
                    if yaml is None:
                        # Fallback: read as plain text and parse manually
                        checkpoint_data = self._parse_yaml_simple(yaml_path)
                    else:
                        with open(yaml_path, 'r', encoding='utf-8') as f:
                            checkpoint_data = yaml.safe_load(f)
                    break
                except Exception as e:
                    print(f"Warning: Failed to load checkpoints from {yaml_path}: {e}")
                    continue

        if checkpoint_data and "checkpoints" in checkpoint_data:
            for cp_id, cp_config in checkpoint_data["checkpoints"].items():
                self.checkpoints.append(Checkpoint(cp_id, cp_config))

    def _parse_yaml_simple(self, yaml_path: Path) -> Dict[str, Any]:
        """Simple YAML parser for basic checkpoint structure (fallback)."""
        # This is a simplified parser for when PyYAML is not available
        # Only handles the basic structure needed for checkpoints
        result = {"checkpoints": {}}
        current_checkpoint = None
        current_field = None

        with open(yaml_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue

                # Detect checkpoint ID
                if stripped.startswith("SCH_") and stripped.endswith(":"):
                    current_checkpoint = stripped.rstrip(":")
                    result["checkpoints"][current_checkpoint] = {}
                elif current_checkpoint and ":" in stripped:
                    key, value = stripped.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if value:
                        result["checkpoints"][current_checkpoint][key] = value

        return result

    def _load_state(self) -> Dict[str, Any]:
        """Load checkpoint state from JSON file."""
        if not self.state_file.exists():
            return {
                "project_path": str(self.project_root),
                "session_id": datetime.utcnow().isoformat(),
                "checkpoints": [],
                "current_stage": 1,
                "completed_stages": []
            }

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load checkpoint state: {e}")
            return {"checkpoints": [], "current_stage": 1}

    def _save_state(self, state: Dict[str, Any]) -> None:
        """Save checkpoint state to JSON file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save checkpoint state: {e}")

    def check_triggers(self, agent_id: str, action: str) -> Optional[Checkpoint]:
        """Check if any checkpoint should trigger based on agent action.

        Args:
            agent_id: ID of the agent performing the action (e.g., "I1", "I2")
            action: Action being performed (e.g., "query_strategy_defined", "screening_started")

        Returns:
            Checkpoint object if triggered, None otherwise
        """
        for checkpoint in self.checkpoints:
            # Check if this checkpoint applies to this agent
            if checkpoint.agent and not agent_id.startswith(checkpoint.agent.split("-")[0]):
                continue

            # Check if checkpoint is already completed
            if self._is_completed(checkpoint):
                continue

            # Check if trigger conditions are met
            if self._should_trigger(checkpoint, agent_id, action):
                return checkpoint

        return None

    def _should_trigger(self, cp: Checkpoint, agent_id: str, action: str) -> bool:
        """Internal trigger logic.

        Args:
            cp: Checkpoint to evaluate
            agent_id: Agent performing the action
            action: Action being performed

        Returns:
            True if checkpoint should trigger
        """
        # Check file-based triggers
        for condition in cp.trigger_conditions:
            condition_lower = condition.lower()

            # Database selection checkpoint
            if "boolean search" in condition_lower or "query strategy" in condition_lower:
                if action == "query_defined" or self._has_file("config.yaml"):
                    return True

            # Screening criteria checkpoint
            if "papers retrieved" in condition_lower or "before executing screening" in condition_lower:
                dedup_file = self.project_root / "data" / "02_deduplicated" / "deduplicated_papers.csv"
                if action == "deduplication_complete" or dedup_file.exists():
                    return True

            # RAG readiness checkpoint
            if "pdfs downloaded" in condition_lower or "vector database built" in condition_lower:
                pdf_dir = self.project_root / "data" / "04_full_text"
                chroma_dir = self.project_root / "rag" / "chroma_db"
                if pdf_dir.exists() or chroma_dir.exists():
                    return True

            # PRISMA generation checkpoint
            if "all statistics available" in condition_lower:
                stats_file = self.project_root / "outputs" / "statistics_report.md"
                if action == "rag_complete" or stats_file.exists():
                    return True

        return False

    def _has_file(self, filename: str) -> bool:
        """Check if file exists in project."""
        file_path = self.project_root / filename
        return file_path.exists()

    def _is_completed(self, cp: Checkpoint) -> bool:
        """Check if checkpoint is already completed.

        Args:
            cp: Checkpoint to check

        Returns:
            True if checkpoint was already completed
        """
        state = self._load_state()
        for checkpoint_state in state.get("checkpoints", []):
            if checkpoint_state.get("id") == cp.id and checkpoint_state.get("status") == "approved":
                return True
        return False

    def _has_decision(self, decision_key: str) -> bool:
        """Check if decision exists in project state.

        Args:
            decision_key: Key to check for in decisions

        Returns:
            True if decision exists
        """
        decision_file = self.project_root / ".research" / "decision-log.yaml"
        if not decision_file.exists():
            return False

        try:
            if yaml:
                with open(decision_file, 'r', encoding='utf-8') as f:
                    decisions = yaml.safe_load(f) or {}
            else:
                # Simple text search fallback
                with open(decision_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return decision_key in content

            return decision_key in decisions
        except Exception as e:
            print(f"Warning: Failed to check decision: {e}")
            return False

    def inject_checkpoint_prompt(self, cp: Checkpoint) -> str:
        """Generate prompt text to inject for checkpoint enforcement.

        Args:
            cp: Checkpoint to generate prompt for

        Returns:
            Formatted prompt text for checkpoint
        """
        emoji = cp.get_emoji()
        lines = [
            f"{emoji} CHECKPOINT: {cp.id}",
            "=" * 60,
            "",
            f"**Stage**: {cp.stage}",
            f"**Agent**: {cp.agent}",
            f"**Level**: {cp.level}",
            "",
            "**Description**:",
            cp.description.strip(),
            "",
        ]

        # Add formatted presentation if available
        if cp.presentation_format:
            lines.append("**Checkpoint Information**:")
            lines.append(cp.presentation_format.strip())
            lines.append("")

        # Add required response information
        if cp.required_response:
            lines.append("**Required Response**:")
            if cp.required_response.get("explicit_approval"):
                lines.append("✓ Explicit approval required")
            if cp.required_response.get("explicit_selection"):
                lines.append("✓ Explicit selection required")

            confirmation_phrases = cp.required_response.get("confirmation_phrase", [])
            if confirmation_phrases:
                lines.append(f"✓ Use phrases: {', '.join(confirmation_phrases)}")

            # Add options if available
            options_text = self._format_options(cp.required_response.get("options", []))
            if options_text:
                lines.append("")
                lines.append(options_text)
            lines.append("")

        # Add behavior based on level
        if cp.level == "REQUIRED":
            lines.extend([
                "**⚠️ CRITICAL CHECKPOINT - HUMAN APPROVAL REQUIRED**",
                "System will STOP and WAIT for your explicit approval.",
                "Cannot proceed without human decision.",
                ""
            ])
        elif cp.level == "RECOMMENDED":
            lines.extend([
                "**⚡ RECOMMENDED CHECKPOINT - REVIEW SUGGESTED**",
                "Please review before proceeding.",
                ""
            ])
        else:  # OPTIONAL
            lines.extend([
                "**ℹ️ OPTIONAL CHECKPOINT - YOUR CHOICE**",
                "You can proceed or customize this step.",
                ""
            ])

        lines.append("=" * 60)
        lines.append(f"Please respond to proceed with {cp.id}.")

        return "\n".join(lines)

    def _format_options(self, options: List[str]) -> str:
        """Format checkpoint options for display.

        Args:
            options: List of option strings

        Returns:
            Formatted options text
        """
        if not options:
            return ""

        lines = ["**Options**:"]
        for i, option in enumerate(options, 1):
            lines.append(f"  [{i}] {option}")
        return "\n".join(lines)

    def record_checkpoint_decision(
        self,
        checkpoint_id: str,
        status: str,
        human_decision: str,
        agent_id: str
    ) -> None:
        """Record checkpoint decision in state file.

        Args:
            checkpoint_id: ID of the checkpoint
            status: Status (approved, rejected, skipped)
            human_decision: Human's decision text
            agent_id: Agent that triggered the checkpoint
        """
        state = self._load_state()

        checkpoint_record = {
            "id": checkpoint_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "human_decision": human_decision,
            "agent": agent_id
        }

        state.setdefault("checkpoints", []).append(checkpoint_record)
        self._save_state(state)

    def get_checkpoint_by_id(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Get checkpoint definition by ID.

        Args:
            checkpoint_id: Checkpoint ID to retrieve

        Returns:
            Checkpoint object if found, None otherwise
        """
        for cp in self.checkpoints:
            if cp.id == checkpoint_id:
                return cp
        return None

    def list_pending_checkpoints(self, current_stage: int) -> List[Checkpoint]:
        """List all pending checkpoints for current stage.

        Args:
            current_stage: Current research stage number

        Returns:
            List of pending checkpoints
        """
        pending = []
        for cp in self.checkpoints:
            if cp.stage <= current_stage and not self._is_completed(cp):
                pending.append(cp)
        return pending
