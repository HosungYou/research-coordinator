"""
Diverga Memory System v7.0 - Unified API
========================================

Main facade providing simplified access to all memory system features.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from .fs_state import FilesystemState
    from .decision_log import DecisionLog
    from .session_hooks import SessionHooks
    from .checkpoint_trigger import CheckpointTrigger
    from .context_trigger import (
        should_load_context,
        load_and_display_context,
    )
    from .artifact_generator import ArtifactGenerator, ResearchSchema
    from .archive import ArchiveManager
    from .templates import TemplateEngine
except ImportError:
    from fs_state import FilesystemState
    from decision_log import DecisionLog
    from session_hooks import SessionHooks
    from checkpoint_trigger import CheckpointTrigger
    from context_trigger import (
        should_load_context,
        load_and_display_context,
    )
    from artifact_generator import ArtifactGenerator, ResearchSchema
    from archive import ArchiveManager
    from templates import TemplateEngine


class MemoryAPI:
    """
    Unified API for Diverga Memory System v7.0
    
    Provides simplified access to all memory system features.
    """

    VERSION = "7.0.0"

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize Memory API with project root."""
        self.project_root = Path(project_root) if project_root else Path.cwd()

        # Initialize core modules
        self.fs_state = FilesystemState(self.project_root)
        self.decision_log = DecisionLog(self.project_root)
        self.session_hooks = SessionHooks(self.project_root)
        self.checkpoint_trigger = CheckpointTrigger(self.project_root)

        # Initialize artifact generation
        self.schema = ResearchSchema()
        self.templates = TemplateEngine()
        self.artifact_generator = ArtifactGenerator(
            self.project_root,
            self.schema,
            self.templates
        )

        # Initialize archive manager
        self.archive_manager = ArchiveManager(self.project_root)

        # Track current session
        self._current_session_id: Optional[str] = None

    # === Context Layer 1 ===
    def should_load_context(self, message: str) -> bool:
        """Check if message contains trigger keywords."""
        try:
            return should_load_context(message)
        except Exception as e:
            print(f"Warning: Context keyword check failed: {e}")
            return False

    def display_context(self) -> str:
        """Load and display research context."""
        try:
            return load_and_display_context(self.project_root)
        except Exception as e:
            return f"⚠️ Error loading context: {str(e)}"

    # === Context Layer 2 ===
    def intercept_task(self, subagent_type: str, prompt: str) -> str:
        """Intercept and enrich task prompt with context."""
        try:
            project_state = self.fs_state.get_project_state()

            if not project_state:
                return prompt

            context_parts = []
            project_name = project_state.get("project_name", "")
            research_question = project_state.get("research_question", "")
            paradigm = project_state.get("paradigm", "")
            current_stage = project_state.get("current_stage", "")

            if project_name:
                context_parts.append(f"[Research Project: {project_name}]")
            if research_question:
                context_parts.append(f"[Research Question: {research_question}]")
            if paradigm:
                context_parts.append(f"[Paradigm: {paradigm}]")
            if current_stage:
                context_parts.append(f"[Current Stage: {current_stage}]")

            recent_decisions = self.decision_log.get_recent_decisions(limit=3)
            if recent_decisions:
                context_parts.append("[Recent Decisions:")
                for dec in recent_decisions:
                    checkpoint = dec.get("checkpoint", "")
                    selected = dec.get("decision", {}).get("selected", "")
                    context_parts.append(f"  - {checkpoint}: {selected}")
                context_parts.append("]")

            if context_parts:
                context_block = "\n".join(context_parts)
                return f"{context_block}\n\n{prompt}"

            return prompt

        except Exception as e:
            print(f"Warning: Task interception failed: {e}")
            return prompt

    # === Context Layer 3 ===
    def run_command(self, command: str, args: Optional[List[str]] = None) -> str:
        """Run CLI command."""
        args = args or []

        try:
            if command == "status":
                return self.display_context()
            elif command == "list":
                return self._cmd_list()
            elif command == "view":
                return self._cmd_view(args[0] if args else None)
            elif command == "init":
                if len(args) >= 3:
                    return self._cmd_init(args[0], args[1], args[2])
                return "Usage: init <name> <question> <paradigm>"
            else:
                return f"Unknown command: {command}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _cmd_list(self) -> str:
        """List all decisions."""
        decisions = self.decision_log.get_recent_decisions(limit=20)
        if not decisions:
            return "No decisions recorded yet."

        lines = ["# Decision History\n"]
        for dec in decisions:
            dec_id = dec.get("id", "")
            timestamp = dec.get("timestamp", "")
            checkpoint = dec.get("checkpoint", "")
            selected = dec.get("decision", {}).get("selected", "")

            lines.append(f"- **{dec_id}** ({timestamp})")
            lines.append(f"  Checkpoint: {checkpoint}")
            lines.append(f"  Selected: {selected}\n")

        return "\n".join(lines)

    def _cmd_view(self, decision_id: Optional[str]) -> str:
        """View specific decision."""
        if not decision_id:
            return "Error: Please provide decision ID"

        decision = self.decision_log.get_decision(decision_id)
        if not decision:
            return f"Decision not found: {decision_id}"

        return f"""# Decision: {decision_id}

**Timestamp**: {decision.get('timestamp', '')}
**Checkpoint**: {decision.get('checkpoint', '')}
**Stage**: {decision.get('stage', '')}

## Selected
{decision.get('decision', {}).get('selected', '')}

## Rationale
{decision.get('rationale', '')}
"""

    def _cmd_init(self, name: str, question: str, paradigm: str) -> str:
        """Initialize new project."""
        success = self.initialize_project(name, question, paradigm)
        return f"✅ Project '{name}' initialized!" if success else "❌ Initialization failed."

    # === Session Management ===
    def start_session(self) -> str:
        """Start new session, return session_id."""
        try:
            context_injection = self.session_hooks.on_session_start()
            self._current_session_id = context_injection.full_context.get("session_id", "")
            return self._current_session_id
        except Exception as e:
            print(f"Warning: Failed to start session: {e}")
            self._current_session_id = str(uuid.uuid4())
            return self._current_session_id

    def end_session(self) -> None:
        """End current session, save data."""
        if not self._current_session_id:
            print("Warning: No active session to end")
            return

        try:
            self.session_hooks.on_session_end(self._current_session_id)
            self._current_session_id = None
        except Exception as e:
            print(f"Warning: Failed to end session: {e}")

    def get_current_session(self) -> Optional[Dict]:
        """Get current session data."""
        if not self._current_session_id:
            return None
        return self.session_hooks.session_data

    # === Checkpoint Management ===
    def check_checkpoint(self, agent_id: str, action: str) -> Optional[str]:
        """Check if checkpoint should trigger."""
        try:
            checkpoint = self.checkpoint_trigger.check_triggers(agent_id, action)
            if checkpoint:
                return self.checkpoint_trigger.inject_checkpoint_prompt(checkpoint)
            return None
        except Exception as e:
            print(f"Warning: Checkpoint check failed: {e}")
            return None

    def record_checkpoint(self, checkpoint_id: str, decision: str) -> None:
        """Record checkpoint decision."""
        try:
            self.checkpoint_trigger.record_checkpoint_decision(
                checkpoint_id, "approved", decision, "user"
            )
            if self._current_session_id:
                self.session_hooks.record_checkpoint(checkpoint_id)
        except Exception as e:
            print(f"Warning: Failed to record checkpoint: {e}")

    def get_pending_checkpoints(self) -> List[str]:
        """Get list of pending checkpoint IDs."""
        try:
            project_state = self.fs_state.get_project_state()
            return project_state.get("pending_checkpoints", [])
        except Exception as e:
            print(f"Warning: Failed to get pending checkpoints: {e}")
            return []

    # === Decision Management ===
    def add_decision(self, checkpoint: str, selected: str, rationale: str, 
                     alternatives: Optional[List[Dict]] = None) -> str:
        """Add new decision, return decision_id."""
        try:
            current_stage = self.fs_state.detect_current_stage()

            decision = {
                "checkpoint": checkpoint,
                "stage": current_stage,
                "agent": "user",
                "decision": {
                    "selected": selected,
                    "alternatives": alternatives or []
                },
                "rationale": rationale,
                "metadata": {
                    "session_id": self._current_session_id or "",
                    "user_confirmed": True
                }
            }

            decision_id = self.decision_log.add_decision(decision)

            if self._current_session_id:
                self.session_hooks.record_decision(decision_id)

            return decision_id
        except Exception as e:
            print(f"Error: Failed to add decision: {e}")
            return ""

    def amend_decision(self, decision_id: str, new_selected: str, new_rationale: str) -> str:
        """Amend existing decision, return new decision_id."""
        try:
            return self.decision_log.amend_decision(decision_id, new_selected, new_rationale)
        except Exception as e:
            print(f"Error: Failed to amend decision: {e}")
            return ""

    def get_recent_decisions(self, limit: int = 5) -> List[Dict]:
        """Get recent decisions."""
        try:
            return self.decision_log.get_recent_decisions(limit)
        except Exception as e:
            print(f"Warning: Failed to get recent decisions: {e}")
            return []

    # === Project State ===
    def initialize_project(self, name: str, question: str, paradigm: str) -> bool:
        """Initialize new research project."""
        try:
            return self.fs_state.initialize_project(name, question, paradigm)
        except Exception as e:
            print(f"Error: Failed to initialize project: {e}")
            return False

    def get_project_state(self) -> Dict:
        """Get current project state."""
        try:
            return self.fs_state.get_project_state()
        except Exception as e:
            print(f"Warning: Failed to get project state: {e}")
            return {}

    def get_current_stage(self) -> str:
        """Get current research stage."""
        try:
            return self.fs_state.detect_current_stage()
        except Exception as e:
            print(f"Warning: Failed to detect current stage: {e}")
            return "foundation"

    def is_initialized(self) -> bool:
        """Check if project is initialized."""
        try:
            return self.fs_state.is_initialized()
        except Exception as e:
            print(f"Warning: Failed to check initialization: {e}")
            return False

    # === Documentation ===
    def generate_artifact(self, artifact_id: str) -> Optional[Path]:
        """Generate research artifact from template."""
        try:
            return self.artifact_generator.generate(artifact_id)
        except Exception as e:
            print(f"Error: Failed to generate artifact '{artifact_id}': {e}")
            return None

    def archive_stage(self, stage_id: str, summary: Optional[str] = None) -> Optional[Path]:
        """Archive completed stage."""
        try:
            return self.archive_manager.archive_stage(stage_id, summary)
        except Exception as e:
            print(f"Error: Failed to archive stage '{stage_id}': {e}")
            return None

    # === Migration ===
    def needs_migration(self) -> bool:
        """Check if project needs migration."""
        old_markers = [
            self.project_root / ".diverga",
            self.project_root / "research_state.yaml",
            self.project_root / ".scholarag",
        ]
        return any(marker.exists() for marker in old_markers)

    def migrate(self, dry_run: bool = False) -> Dict:
        """Run migration if needed."""
        return {
            "needed": self.needs_migration(),
            "dry_run": dry_run,
            "status": "not_implemented",
            "message": "Migration feature coming in v7.1"
        }

    # === Utility ===
    def get_version(self) -> str:
        """Get memory system version."""
        return self.VERSION


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python memory_api.py <command> [args...]")
        print("\nCommands:")
        print("  status  - Show project status")
        print("  list    - List all decisions")
        print("  view <id> - View specific decision")
        print("  init <name> <question> <paradigm> - Initialize project")
        sys.exit(1)

    api = MemoryAPI()
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    result = api.run_command(command, args)
    print(result)


if __name__ == "__main__":
    main()
