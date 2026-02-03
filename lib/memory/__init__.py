"""
Diverga Memory System v7.0
=========================

Human-centered research context persistence with checkpoint auto-trigger,
cross-session continuity, and research documentation automation.

Features:
- 3-Layer Context System (Keyword-Triggered, Task Interceptor, CLI)
- Checkpoint Auto-Trigger for Human-in-the-Loop decisions
- Dual-Tree filesystem structure (baselines + changes)
- Decision Audit Trail with version control
- Research documentation with templates and schema

Usage:
    from lib.memory import MemoryAPI

    # Initialize for a project
    memory = MemoryAPI(project_root=Path("."))

    # Check if context should load
    if memory.should_load_context("What's my research status?"):
        print(memory.display_context())

    # Intercept task calls for context injection
    prompt = memory.intercept_task("diverga:a1", original_prompt)
"""

__version__ = "7.0.0"
__author__ = "Hosung You"

from .src.memory_api import MemoryAPI
from .src.models import (
    ResearchContext,
    Checkpoint,
    CheckpointLevel,
    Decision,
    Amendment,
    ContextInjection,
    SessionData,
)
from .src.context_trigger import should_load_context, load_and_display_context
from .src.task_interceptor import intercept_task_call, detect_project_root
from .src.checkpoint_trigger import CheckpointTrigger
from .src.fs_state import FilesystemState
from .src.dual_tree import DualTreeManager
from .src.archive import ArchiveManager
from .src.decision_log import DecisionLog
from .src.session_hooks import SessionHooks
from .src.schema import ResearchSchema
from .src.templates import TemplateEngine
from .src.artifact_generator import ArtifactGenerator
from .src.cli import run_cli
from .src.migration import migrate_v68_to_v70, detect_version, needs_migration

__all__ = [
    # Main API
    "MemoryAPI",

    # Models
    "ResearchContext",
    "Checkpoint",
    "CheckpointLevel",
    "Decision",
    "Amendment",
    "ContextInjection",
    "SessionData",

    # Context System
    "should_load_context",
    "load_and_display_context",
    "intercept_task_call",
    "detect_project_root",
    "CheckpointTrigger",

    # Filesystem
    "FilesystemState",
    "DualTreeManager",
    "ArchiveManager",

    # Decision & Session
    "DecisionLog",
    "SessionHooks",

    # Documentation
    "ResearchSchema",
    "TemplateEngine",
    "ArtifactGenerator",

    # CLI & Migration
    "run_cli",
    "migrate_v68_to_v70",
    "detect_version",
    "needs_migration",
]
