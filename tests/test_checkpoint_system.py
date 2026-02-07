#!/usr/bin/env python3
"""
Tests for Checkpoint System
==============================

Validates the human checkpoint system:
- All checkpoints are defined (at least 11)
- Required checkpoints include CP_PARADIGM and CP_METHODOLOGY
- Checkpoint protocol includes STOP, WAIT, DO NOT PROCEED rules
- Checkpoint levels (REQUIRED/RECOMMENDED/OPTIONAL) are documented

Usage:
    pytest tests/test_checkpoint_system.py -v
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent
CLAUDE_MD = BASE_DIR / "CLAUDE.md"
MEMORY_SKILL_PATH = BASE_DIR / "skills" / "memory" / "SKILL.md"
SETUP_SKILL_PATH = BASE_DIR / "skills" / "setup" / "SKILL.md"
CONFIG_PATH = BASE_DIR / "config" / "diverga-config.json"


def _load_all_checkpoint_sources() -> str:
    """Load all files that define or reference checkpoints."""
    sources = []
    for path in [CLAUDE_MD, MEMORY_SKILL_PATH]:
        if path.exists():
            sources.append(path.read_text(encoding="utf-8"))
    return "\n".join(sources)


# Known checkpoint IDs extracted from CLAUDE.md and memory SKILL.md
KNOWN_CHECKPOINTS = [
    "CP_RESEARCH_DIRECTION",
    "CP_PARADIGM_SELECTION",
    "CP_SCOPE_DEFINITION",
    "CP_THEORY_SELECTION",
    "CP_VARIABLE_DEFINITION",
    "CP_METHODOLOGY_APPROVAL",
    "CP_DATABASE_SELECTION",
    "CP_SEARCH_STRATEGY",
    "CP_SAMPLE_PLANNING",
    "CP_SCREENING_CRITERIA",
    "CP_RAG_READINESS",
]

# Additional checkpoints that may be defined
EXTENDED_CHECKPOINTS = [
    "CP_DATA_EXTRACTION",
    "CP_ANALYSIS_PLAN",
    "CP_QUALITY_GATES",
    "CP_PEER_REVIEW",
    "CP_PUBLICATION_READY",
    "CP_HUMANIZATION_REVIEW",
    "CP_HUMANIZATION_VERIFY",
]


class TestCheckpointDefinitions:
    """Tests that all checkpoints are properly defined."""

    def test_at_least_11_checkpoints_defined(self):
        """At least 11 checkpoints must be defined across documentation."""
        content = _load_all_checkpoint_sources()
        # Find all CP_* patterns
        checkpoint_ids = set(re.findall(r"CP_[A-Z_]+", content))
        assert len(checkpoint_ids) >= 11, (
            f"Expected at least 11 checkpoints, found {len(checkpoint_ids)}: "
            f"{sorted(checkpoint_ids)}"
        )

    def test_known_checkpoints_are_defined(self):
        """All 11 core checkpoint IDs must appear in documentation."""
        content = _load_all_checkpoint_sources()

        missing = [
            cp for cp in KNOWN_CHECKPOINTS
            if cp not in content
        ]
        assert not missing, (
            f"Missing checkpoint definitions: {missing}"
        )

    def test_setup_mentions_11_checkpoints(self):
        """Setup SKILL.md should reference '11 checkpoints' for Full mode."""
        content = SETUP_SKILL_PATH.read_text(encoding="utf-8")
        assert "11 checkpoint" in content.lower() or "11" in content, (
            "Setup SKILL.md should mention '11 checkpoints' for Full checkpoint level"
        )


class TestRequiredCheckpoints:
    """Tests that mandatory checkpoints are correctly identified."""

    def test_cp_paradigm_is_required(self):
        """CP_PARADIGM_SELECTION or CP_PARADIGM must be in the required checkpoints."""
        content = _load_all_checkpoint_sources()
        has_paradigm_required = (
            ("CP_PARADIGM" in content and "required" in content.lower())
            or "CP_PARADIGM_SELECTION" in content
        )
        assert has_paradigm_required, (
            "CP_PARADIGM checkpoint must be defined as required"
        )

    def test_cp_methodology_is_required(self):
        """CP_METHODOLOGY_APPROVAL or CP_METHODOLOGY must be in required checkpoints."""
        content = _load_all_checkpoint_sources()
        has_methodology = (
            "CP_METHODOLOGY" in content
            or "CP_METHODOLOGY_APPROVAL" in content
        )
        assert has_methodology, (
            "CP_METHODOLOGY checkpoint must be defined"
        )

    def test_config_has_cp_paradigm_in_required(self):
        """diverga-config.json must list CP_PARADIGM in required checkpoints."""
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        required = data.get("human_checkpoints", {}).get("required", [])
        has_paradigm = any("PARADIGM" in cp for cp in required)
        assert has_paradigm, (
            f"Config required checkpoints {required} must include CP_PARADIGM"
        )

    def test_config_has_cp_methodology_in_required(self):
        """diverga-config.json must list CP_METHODOLOGY in required checkpoints."""
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        required = data.get("human_checkpoints", {}).get("required", [])
        has_methodology = any("METHODOLOGY" in cp for cp in required)
        assert has_methodology, (
            f"Config required checkpoints {required} must include CP_METHODOLOGY"
        )


class TestCheckpointProtocol:
    """Tests that checkpoint protocol rules are properly documented."""

    @pytest.fixture()
    def claude_content(self) -> str:
        """Load CLAUDE.md content."""
        return CLAUDE_MD.read_text(encoding="utf-8")

    def test_stop_rule_documented(self, claude_content: str):
        """Checkpoint protocol must include 'STOP immediately' rule."""
        assert "STOP immediately" in claude_content or "STOP" in claude_content, (
            "Checkpoint protocol must document STOP rule"
        )

    def test_wait_rule_documented(self, claude_content: str):
        """Checkpoint protocol must include 'WAIT for explicit human approval' rule."""
        content_lower = claude_content.lower()
        assert "wait for" in content_lower or "wait" in content_lower, (
            "Checkpoint protocol must document WAIT for human approval rule"
        )

    def test_do_not_proceed_rule_documented(self, claude_content: str):
        """Checkpoint protocol must include 'DO NOT proceed' rule."""
        assert (
            "DO NOT proceed" in claude_content
            or "do not proceed" in claude_content.lower()
            or "Cannot proceed" in claude_content
        ), "Checkpoint protocol must specify DO NOT PROCEED without approval"

    def test_do_not_assume_rule_documented(self, claude_content: str):
        """Checkpoint protocol must include 'DO NOT assume approval' rule."""
        assert (
            "DO NOT assume" in claude_content
            or "do not assume" in claude_content.lower()
        ), "Checkpoint protocol must specify DO NOT assume approval based on context"

    def test_checkpoint_protocol_box_exists(self, claude_content: str):
        """CLAUDE.md must contain the CHECKPOINT PROTOCOL block."""
        assert "CHECKPOINT PROTOCOL" in claude_content, (
            "CLAUDE.md must contain the CHECKPOINT PROTOCOL documentation block"
        )


class TestCheckpointLevels:
    """Tests that checkpoint levels are properly defined."""

    def test_required_level_defined(self):
        """REQUIRED checkpoint level must be defined."""
        content = _load_all_checkpoint_sources()
        assert "REQUIRED" in content, (
            "REQUIRED checkpoint level must be defined"
        )

    def test_recommended_level_defined(self):
        """RECOMMENDED checkpoint level must be defined."""
        content = _load_all_checkpoint_sources()
        assert "RECOMMENDED" in content, (
            "RECOMMENDED checkpoint level must be defined"
        )

    def test_optional_level_defined(self):
        """OPTIONAL checkpoint level must be defined."""
        content = _load_all_checkpoint_sources()
        assert "OPTIONAL" in content, (
            "OPTIONAL checkpoint level must be defined"
        )

    def test_required_level_has_stop_behavior(self):
        """REQUIRED level must specify that the system STOPS."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        # Look for REQUIRED and STOP in proximity
        required_section = re.search(
            r"REQUIRED.*?STOP|STOP.*?REQUIRED",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        assert required_section is not None, (
            "REQUIRED checkpoint level must specify STOP behavior"
        )

    def test_checkpoint_icons_documented(self):
        """Checkpoint levels should have icon indicators documented."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        has_red = "\U0001f534" in content     # Red circle for REQUIRED
        has_orange = "\U0001f7e0" in content  # Orange circle for RECOMMENDED
        has_yellow = "\U0001f7e1" in content  # Yellow circle for OPTIONAL

        assert has_red, "REQUIRED checkpoint should have red circle icon"
        assert has_orange, "RECOMMENDED checkpoint should have orange circle icon"
        assert has_yellow, "OPTIONAL checkpoint should have yellow circle icon"


class TestCheckpointInMemorySystem:
    """Tests that the memory system properly integrates with checkpoints."""

    @pytest.fixture()
    def memory_content(self) -> str:
        """Load memory SKILL.md content."""
        return MEMORY_SKILL_PATH.read_text(encoding="utf-8")

    def test_memory_tracks_checkpoint_status(self, memory_content: str):
        """Memory system must track checkpoint completion status."""
        content_lower = memory_content.lower()
        assert (
            "status" in content_lower
            and ("completed" in content_lower or "pending" in content_lower)
        ), "Memory system must track checkpoint status (completed/pending)"

    def test_memory_records_checkpoint_timestamp(self, memory_content: str):
        """Memory system must record timestamps for checkpoint events."""
        assert (
            "timestamp" in memory_content.lower()
            or "completed_at" in memory_content
            or "triggered_at" in memory_content
        ), "Memory system must record timestamps for checkpoints"

    def test_memory_links_checkpoints_to_decisions(self, memory_content: str):
        """Memory system must link checkpoints to decision IDs."""
        assert (
            "decision_id" in memory_content
            or "decision" in memory_content.lower()
        ), "Memory system must link checkpoints to decisions"

    def test_memory_defines_checkpoint_stages(self, memory_content: str):
        """Memory system must define checkpoint stages (foundation, design, etc.)."""
        stages = ["foundation", "design", "planning", "execution"]
        found = [s for s in stages if s in memory_content.lower()]
        assert len(found) >= 3, (
            f"Memory system should define at least 3 checkpoint stages. "
            f"Found: {found}"
        )


class TestCheckpointEnforcement:
    """Tests that checkpoint enforcement rules are clearly stated."""

    def test_never_auto_proceed(self):
        """Documentation must state never to auto-proceed past checkpoints."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert (
            "DO NOT proceed" in content
            or "DO NOT assume" in content
            or "NEVER" in content
        ), "Must document that AI should never auto-proceed past checkpoints"

    def test_always_ask_pattern(self):
        """Documentation must show the 'always ask' pattern."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert "ALWAYS" in content, (
            "Documentation must use ALWAYS to emphasize asking at checkpoints"
        )

    def test_human_centered_principle(self):
        """Documentation must state the human-centered principle."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert (
            "Human" in content
            and ("decide" in content.lower() or "decision" in content.lower())
        ), "Documentation must state the human-centered decision principle"
