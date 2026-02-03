"""
Diverga Memory System v7.0 - Unified API
========================================

Main facade providing simplified access to all memory system features.

This is the primary interface for the Diverga Memory System, providing:
- Context loading (3-layer system)
- Checkpoint management
- Decision audit trail
- Session management
- Research documentation
- Migration support

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

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
    # Fallback for standalone usage
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

    Provides simplified access to:
    - Context loading (3-layer system)
    - Checkpoint management
    - Decision audit trail
    - Session management
    - Research documentation

    Example:
        memory = MemoryAPI(project_root=Path("."))

        # Start session
        memory.start_session()

        # Check context keywords
        if memory.should_load_context("What's my research status?"):
            print(memory.display_context())

        # Intercept agent calls
        prompt = memory.intercept_task("diverga:a1", original_prompt)

        # Add decision
        memory.add_decision(
            checkpoint="CP_RESEARCH_DIRECTION",
            selected="Meta-analysis",
            rationale="Strong evidence base"
        )

        # End session
        memory.end_session()
    """

    VERSION = "7.0.0"

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize Memory API with project root.

        Args:
            project_root: Root directory of the research project.
                         If None, uses current working directory.
        """
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

    # =========================================================================
    # Context Layer 1: Keyword-Triggered
    # =========================================================================

    def should_load_context(self, message: str) -> bool:
        """
        Check if message contains trigger keywords.

        Args:
            message: User message to check

        Returns:
            True if context should be loaded, False otherwise
        """
        try:
            return should_load_context(message)
        except Exception as e:
            print(f"Warning: Context keyword check failed: {e}")
            return False

    def display_context(self) -> str:
        """
        Load and format context for display to Claude Code.

        Returns:
            Formatted context string with research state, decisions, checkpoints
        """
        context = self.load_context()
        if not context:
            return "[No active research context found]"

        output = []
        output.append("=" * 70)
        output.append("DIVERGA RESEARCH CONTEXT")
        output.append("=" * 70)
        output.append(f"\nProject: {context.project_name}")
        output.append(f"Research Question: {context.research_question}")
        output.append(f"Current Stage: {context.current_stage}")
        output.append(f"Last Updated: {context.last_updated}")

        # Active checkpoints
        active = [cp for cp in context.checkpoints if cp.status == "pending"]
        if active:
            output.append(f"\n\nActive Checkpoints ({len(active)}):")
            for cp in active:
                emoji = "🔴" if cp.level == CheckpointLevel.RED else "🟠" if cp.level == CheckpointLevel.ORANGE else "🟢"
                output.append(f"  {emoji} {cp.checkpoint_id}: {cp.description}")

        # Recent decisions
        if context.decisions:
            recent = sorted(context.decisions, key=lambda d: d.timestamp, reverse=True)[:5]
            output.append(f"\n\nRecent Decisions ({len(recent)}):")
            for dec in recent:
                output.append(f"  [{dec.checkpoint_id}] {dec.choice}")
                output.append(f"    Rationale: {dec.rationale[:80]}...")

        # Filesystem changes
        changed_files = self.fs_state.get_changed_files()
        if changed_files:
            output.append(f"\n\nModified Files ({len(changed_files)}):")
            for file_path in changed_files[:10]:
                output.append(f"  - {file_path}")

        output.append("\n" + "=" * 70)
        return "\n".join(output)

    def load_context(self) -> Optional[ResearchContext]:
        """
        Load research context from JSON.

        Returns:
            ResearchContext object or None if not found
        """
        context_file = self.context_root / "context.json"
        if not context_file.exists():
            return None

        try:
            data = json.loads(context_file.read_text(encoding="utf-8"))
            return ResearchContext.from_dict(data)
        except Exception as e:
            print(f"Error loading context: {e}")
            return None

    def save_context(self, context: ResearchContext):
        """
        Save research context to JSON.

        Args:
            context: ResearchContext object to save
        """
        context_file = self.context_root / "context.json"
        context_file.parent.mkdir(parents=True, exist_ok=True)
        context_file.write_text(
            json.dumps(context.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    # ========================================================================
    # Task Interception
    # ========================================================================

    def intercept_task(self, agent_name: str, original_prompt: str) -> str:
        """
        Intercept Task tool calls to inject research context.

        Args:
            agent_name: Name of agent being called (e.g., "diverga:a1")
            original_prompt: Original prompt to agent

        Returns:
            Enhanced prompt with context injection
        """
        return _intercept_task_call(agent_name, original_prompt, self.context_root)

    # ========================================================================
    # Checkpoint Management
    # ========================================================================

    def trigger_checkpoint(self, checkpoint_id: str, context_data: Dict[str, Any]) -> bool:
        """
        Trigger a checkpoint and prompt for human decision.

        Args:
            checkpoint_id: ID of checkpoint (e.g., "RED_METHOD_CHOICE")
            context_data: Current research context for decision

        Returns:
            True if checkpoint was triggered successfully
        """
        return self.checkpoint_trigger.trigger(checkpoint_id, context_data)

    def resolve_checkpoint(
        self,
        checkpoint_id: str,
        choice: str,
        rationale: str,
        alternatives_considered: Optional[List[str]] = None,
    ):
        """
        Resolve a checkpoint with a decision.

        Args:
            checkpoint_id: ID of checkpoint to resolve
            choice: Chosen option
            rationale: Explanation of choice
            alternatives_considered: Other options considered
        """
        context = self.load_context()
        if not context:
            raise ValueError("No active research context")

        # Mark checkpoint as resolved
        for cp in context.checkpoints:
            if cp.checkpoint_id == checkpoint_id:
                cp.status = "resolved"
                cp.resolved_at = datetime.now()
                break

        # Record decision
        decision = Decision(
            checkpoint_id=checkpoint_id,
            choice=choice,
            rationale=rationale,
            alternatives_considered=alternatives_considered or [],
            timestamp=datetime.now(),
        )
        context.decisions.append(decision)

        # Log to decision log
        self.decision_log.log_decision(decision)

        # Save updated context
        self.save_context(context)

    # ========================================================================
    # Decision Management
    # ========================================================================

    def record_decision(
        self,
        checkpoint_id: str,
        choice: str,
        rationale: str,
        alternatives_considered: Optional[List[str]] = None,
    ):
        """
        Record a research decision (convenience wrapper for resolve_checkpoint).

        Args:
            checkpoint_id: ID of checkpoint this decision resolves
            choice: Chosen option
            rationale: Explanation of choice
            alternatives_considered: Other options considered
        """
        self.resolve_checkpoint(checkpoint_id, choice, rationale, alternatives_considered)

    def amend_decision(
        self,
        original_checkpoint_id: str,
        new_choice: str,
        amendment_rationale: str,
    ):
        """
        Amend a previous decision.

        Args:
            original_checkpoint_id: ID of checkpoint to amend
            new_choice: New choice replacing original
            amendment_rationale: Why decision was changed
        """
        context = self.load_context()
        if not context:
            raise ValueError("No active research context")

        # Find original decision
        original_decision = None
        for dec in context.decisions:
            if dec.checkpoint_id == original_checkpoint_id:
                original_decision = dec
                break

        if not original_decision:
            raise ValueError(f"No decision found for checkpoint: {original_checkpoint_id}")

        # Create amendment
        amendment = Amendment(
            original_checkpoint_id=original_checkpoint_id,
            original_choice=original_decision.choice,
            new_choice=new_choice,
            amendment_rationale=amendment_rationale,
            amended_at=datetime.now(),
        )
        context.amendments.append(amendment)

        # Update original decision
        original_decision.choice = new_choice
        original_decision.rationale += f"\n\n[AMENDED: {amendment_rationale}]"

        # Log amendment
        self.decision_log.log_amendment(amendment)

        # Save updated context
        self.save_context(context)

    def get_decision_history(self, checkpoint_id: str) -> List[Decision]:
        """
        Get all decisions for a checkpoint.

        Args:
            checkpoint_id: ID of checkpoint

        Returns:
            List of decisions (including amendments)
        """
        return self.decision_log.get_history(checkpoint_id)

    # ========================================================================
    # Filesystem Tracking
    # ========================================================================

    def snapshot_filesystem(self):
        """
        Capture current filesystem state as baseline.
        """
        self.fs_state.snapshot()

    def get_changed_files(self) -> List[str]:
        """
        Get list of files changed since baseline.

        Returns:
            List of file paths
        """
        return self.fs_state.get_changed_files()

    def archive_session(self, session_name: Optional[str] = None):
        """
        Archive current session to dual-tree structure.

        Args:
            session_name: Optional name for session (default: timestamp)
        """
        if not session_name:
            session_name = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.archive.archive_session(session_name, self.fs_state)

    # ========================================================================
    # Documentation Generation
    # ========================================================================

    def generate_summary(self) -> str:
        """
        Generate research summary document.

        Returns:
            Path to generated summary file
        """
        context = self.load_context()
        if not context:
            raise ValueError("No active research context")

        return self.artifacts.generate_summary(context)

    def generate_codebook(self) -> str:
        """
        Generate coding scheme documentation.

        Returns:
            Path to generated codebook file
        """
        context = self.load_context()
        if not context:
            raise ValueError("No active research context")

        return self.artifacts.generate_codebook(context)

    def generate_changelog(self) -> str:
        """
        Generate decision changelog.

        Returns:
            Path to generated changelog file
        """
        context = self.load_context()
        if not context:
            raise ValueError("No active research context")

        return self.artifacts.generate_changelog(context)

    # ========================================================================
    # Session Management
    # ========================================================================

    def start_session(self):
        """
        Start a new research session.
        """
        self.session_hooks.on_session_start()
        self.snapshot_filesystem()

    def end_session(self, auto_archive: bool = True):
        """
        End current research session.

        Args:
            auto_archive: Auto-archive changed files (default: True)
        """
        if auto_archive:
            self.archive_session()

        self.session_hooks.on_session_end()

    # ========================================================================
    # Migration
    # ========================================================================

    def _needs_migration(self) -> bool:
        """
        Check if project needs migration from v6.8.

        Returns:
            True if migration needed
        """
        from .migration import needs_migration
        return needs_migration(self.project_root)

    def _migrate_from_v68(self):
        """
        Migrate from v6.8 to v7.0.
        """
        from .migration import migrate_v68_to_v70
        print("Migrating from v6.8 to v7.0...")
        migrate_v68_to_v70(self.project_root)
        print("Migration complete!")

    # ========================================================================
    # Utilities
    # ========================================================================

    def get_status(self) -> Dict[str, Any]:
        """
        Get current system status.

        Returns:
            Dictionary with status information
        """
        context = self.load_context()

        return {
            "version": "7.0.0",
            "project_root": str(self.project_root),
            "context_root": str(self.context_root),
            "has_context": context is not None,
            "project_name": context.project_name if context else None,
            "current_stage": context.current_stage if context else None,
            "active_checkpoints": len([cp for cp in context.checkpoints if cp.status == "pending"]) if context else 0,
            "total_decisions": len(context.decisions) if context else 0,
            "changed_files": len(self.get_changed_files()),
        }

    def __repr__(self) -> str:
        status = self.get_status()
        return f"<MemoryAPI v{status['version']} project={status['project_name']} stage={status['current_stage']}>"
