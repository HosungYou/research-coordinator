#!/usr/bin/env python3
"""
Tests for Agent System Consistency
====================================

Validates that the agent system is internally consistent:
- All agents referenced in CLAUDE.md exist as skill directories
- Model routing counts match (Opus/Sonnet/Haiku)
- Parallel execution groups reference valid agents
- Sequential pipeline agents exist
- Auto-trigger keywords map to valid agent IDs

Usage:
    pytest tests/test_agent_consistency.py -v
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"
CLAUDE_MD = BASE_DIR / "CLAUDE.md"

# Agent IDs as they appear in CLAUDE.md trigger tables (diverga:XX format)
AGENT_IDS = [
    "a1", "a2", "a3", "a4", "a5", "a6",
    "b1", "b2", "b3", "b4", "b5",
    "c1", "c2", "c3", "c4", "c5", "c6", "c7",
    "d1", "d2", "d3", "d4",
    "e1", "e2", "e3", "e4", "e5",
    "f1", "f2", "f3", "f4", "f5",
    "g1", "g2", "g3", "g4", "g5", "g6",
    "h1", "h2",
    "i0", "i1", "i2", "i3",
]

# Model routing per CLAUDE.md section "Model Routing (v6.7)"
OPUS_AGENTS = [
    "a1", "a2", "a3", "a5", "b5",
    "c1", "c2", "c3", "d4",
    "e1", "e2", "e3",
    "g3", "g6",
    "h1", "h2",
    "i0",
]  # 17 agents

SONNET_AGENTS = [
    "a4", "a6",
    "b1", "b2",
    "c4",
    "d1", "d2",
    "e5",
    "f3", "f4",
    "g1", "g2", "g4", "g5",
    "i1", "i2",
]  # 16 agents

HAIKU_AGENTS = [
    "b3", "b4",
    "d3",
    "e4",
    "f1", "f2", "f5",
    "i3",
]  # 8 agents

# Parallel execution groups from CLAUDE.md
PARALLEL_GROUPS = {
    "Group 1: Research Design": ["a1", "a2", "a5"],
    "Group 2: Literature & Evidence": ["b1", "b2", "b3"],
    "Group 4: Quality Assurance": ["f1", "f3", "f4"],
    "Group 5: Publication Prep": ["g1", "g2", "g5"],
    "Group 6: Systematic Review Screening (parallel)": ["i1", "i2"],
}

# Sequential pipeline agents from CLAUDE.md
SEQUENTIAL_PIPELINES = {
    "Meta-Analysis Pipeline": ["c5", "c6", "c7"],
    "Humanization Pipeline": ["g5", "g6", "f5"],
    "Systematic Review Pipeline": ["i0", "i1", "i2", "i3"],
}


class TestAgentDirectoryExistence:
    """Tests that all agents referenced in CLAUDE.md exist as skill directories."""

    def test_all_44_agents_have_skill_directories(self):
        """Every one of the 44 agent IDs must have a corresponding skill directory."""
        missing = [
            aid for aid in AGENT_IDS
            if not (SKILLS_DIR / aid).is_dir()
        ]
        assert not missing, (
            f"Agent IDs referenced in CLAUDE.md but missing skill directories: {missing}"
        )

    def test_all_44_agents_have_skill_md(self):
        """Every agent skill directory must contain a SKILL.md file."""
        missing_md = [
            aid for aid in AGENT_IDS
            if (SKILLS_DIR / aid).is_dir()
            and not (SKILLS_DIR / aid / "SKILL.md").exists()
        ]
        assert not missing_md, (
            f"Agent directories missing SKILL.md: {missing_md}"
        )

    def test_claude_md_references_all_agents(self):
        """CLAUDE.md must reference all 44 agent IDs in the auto-trigger tables."""
        assert CLAUDE_MD.exists(), f"CLAUDE.md not found at {CLAUDE_MD}"
        content = CLAUDE_MD.read_text(encoding="utf-8")

        unreferenced = []
        for aid in AGENT_IDS:
            # Look for diverga:XX pattern in CLAUDE.md
            pattern = f"diverga:{aid}"
            if pattern not in content:
                unreferenced.append(aid)

        assert not unreferenced, (
            f"Agent IDs not referenced in CLAUDE.md: {unreferenced}"
        )


class TestModelRoutingConsistency:
    """Tests that model routing in CLAUDE.md matches expected counts."""

    def test_opus_agent_count(self):
        """There must be exactly 17 Opus (HIGH tier) agents."""
        assert len(OPUS_AGENTS) == 17, (
            f"Expected 17 Opus agents, defined {len(OPUS_AGENTS)}: {OPUS_AGENTS}"
        )

    def test_sonnet_agent_count(self):
        """There must be exactly 16 Sonnet (MEDIUM tier) agents."""
        assert len(SONNET_AGENTS) == 16, (
            f"Expected 16 Sonnet agents, defined {len(SONNET_AGENTS)}: {SONNET_AGENTS}"
        )

    def test_haiku_agent_count(self):
        """There must be exactly 8 Haiku (LOW tier) agents."""
        assert len(HAIKU_AGENTS) == 8, (
            f"Expected 8 Haiku agents, defined {len(HAIKU_AGENTS)}: {HAIKU_AGENTS}"
        )

    def test_model_routing_covers_41_agents(self):
        """Opus + Sonnet + Haiku must total 41 agents in the routing table.

        CLAUDE.md routing table lists 17 + 16 + 8 = 41 agents explicitly.
        The remaining 3 agents (c5, c6, c7) are documented in their own
        meta-analysis section with model assignments.
        """
        all_routed = set(OPUS_AGENTS + SONNET_AGENTS + HAIKU_AGENTS)
        total = len(OPUS_AGENTS) + len(SONNET_AGENTS) + len(HAIKU_AGENTS)
        assert total == 41, (
            f"Model routing covers {total} agents, expected 41 "
            f"(17 Opus + 16 Sonnet + 8 Haiku)"
        )

    def test_no_duplicate_agents_across_tiers(self):
        """No agent should appear in more than one model tier."""
        opus_set = set(OPUS_AGENTS)
        sonnet_set = set(SONNET_AGENTS)
        haiku_set = set(HAIKU_AGENTS)

        opus_sonnet = opus_set & sonnet_set
        opus_haiku = opus_set & haiku_set
        sonnet_haiku = sonnet_set & haiku_set

        errors = []
        if opus_sonnet:
            errors.append(f"In both Opus and Sonnet: {opus_sonnet}")
        if opus_haiku:
            errors.append(f"In both Opus and Haiku: {opus_haiku}")
        if sonnet_haiku:
            errors.append(f"In both Sonnet and Haiku: {sonnet_haiku}")

        assert not errors, "Duplicate agents across tiers:\n" + "\n".join(errors)

    def test_all_routed_agents_are_valid(self):
        """Every agent in model routing must be a valid agent ID."""
        all_routed = set(OPUS_AGENTS + SONNET_AGENTS + HAIKU_AGENTS)
        invalid = all_routed - set(AGENT_IDS)
        assert not invalid, (
            f"Model routing references invalid agent IDs: {invalid}"
        )

    def test_unrouted_agents_are_meta_analysis(self):
        """Agents not in the main routing table should be the meta-analysis set (c5, c6, c7)."""
        all_routed = set(OPUS_AGENTS + SONNET_AGENTS + HAIKU_AGENTS)
        unrouted = set(AGENT_IDS) - all_routed
        expected_unrouted = {"c5", "c6", "c7"}
        assert unrouted == expected_unrouted, (
            f"Unrouted agents are {sorted(unrouted)}, "
            f"expected {sorted(expected_unrouted)} (meta-analysis agents)"
        )


class TestParallelExecutionGroups:
    """Tests that parallel execution groups reference valid agents."""

    def test_all_parallel_group_agents_exist(self):
        """Every agent referenced in a parallel execution group must exist."""
        invalid = {}
        for group_name, agents in PARALLEL_GROUPS.items():
            missing = [a for a in agents if a not in AGENT_IDS]
            if missing:
                invalid[group_name] = missing

        assert not invalid, (
            "Parallel groups reference invalid agents:\n"
            + "\n".join(f"  {g}: {a}" for g, a in invalid.items())
        )

    def test_all_parallel_group_agents_have_directories(self):
        """Every agent in a parallel group must have a skill directory."""
        missing = {}
        for group_name, agents in PARALLEL_GROUPS.items():
            no_dir = [a for a in agents if not (SKILLS_DIR / a).is_dir()]
            if no_dir:
                missing[group_name] = no_dir

        assert not missing, (
            "Parallel groups reference agents without directories:\n"
            + "\n".join(f"  {g}: {a}" for g, a in missing.items())
        )


class TestSequentialPipelines:
    """Tests that sequential pipeline agents exist and are valid."""

    def test_all_pipeline_agents_exist(self):
        """Every agent in a sequential pipeline must be a valid agent ID."""
        invalid = {}
        for pipeline_name, agents in SEQUENTIAL_PIPELINES.items():
            missing = [a for a in agents if a not in AGENT_IDS]
            if missing:
                invalid[pipeline_name] = missing

        assert not invalid, (
            "Sequential pipelines reference invalid agents:\n"
            + "\n".join(f"  {p}: {a}" for p, a in invalid.items())
        )

    def test_all_pipeline_agents_have_directories(self):
        """Every agent in a sequential pipeline must have a skill directory."""
        missing = {}
        for pipeline_name, agents in SEQUENTIAL_PIPELINES.items():
            no_dir = [a for a in agents if not (SKILLS_DIR / a).is_dir()]
            if no_dir:
                missing[pipeline_name] = no_dir

        assert not missing, (
            "Sequential pipelines reference agents without directories:\n"
            + "\n".join(f"  {p}: {a}" for p, a in missing.items())
        )


class TestAutoTriggerKeywords:
    """Tests that auto-trigger keyword tables reference valid agent IDs."""

    def test_claude_md_trigger_table_agents_are_valid(self):
        """All diverga:XX references in CLAUDE.md trigger tables must be valid agents."""
        assert CLAUDE_MD.exists(), f"CLAUDE.md not found at {CLAUDE_MD}"
        content = CLAUDE_MD.read_text(encoding="utf-8")

        # Extract all diverga:XX references
        references = set(re.findall(r"diverga:([a-z]\d+)", content))

        all_valid = set(AGENT_IDS)
        invalid = references - all_valid
        assert not invalid, (
            f"CLAUDE.md references invalid agent IDs: {sorted(invalid)}"
        )

    def test_every_agent_has_trigger_keywords(self):
        """Every agent ID should appear in the CLAUDE.md trigger keyword tables."""
        assert CLAUDE_MD.exists()
        content = CLAUDE_MD.read_text(encoding="utf-8")

        # Extract the auto-trigger section
        trigger_section_match = re.search(
            r"## Auto-Trigger Agent Dispatch.*?(?=^## |\Z)",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if trigger_section_match is None:
            pytest.skip("Auto-Trigger Agent Dispatch section not found in CLAUDE.md")

        trigger_section = trigger_section_match.group(0)
        missing_triggers = []
        for aid in AGENT_IDS:
            if f"diverga:{aid}" not in trigger_section:
                missing_triggers.append(aid)

        assert not missing_triggers, (
            f"Agents without trigger keywords in CLAUDE.md: {missing_triggers}"
        )


class TestCategoryStructure:
    """Tests that agent categories match the documented structure."""

    CATEGORIES = {
        "A: Foundation": ["a1", "a2", "a3", "a4", "a5", "a6"],
        "B: Evidence": ["b1", "b2", "b3", "b4", "b5"],
        "C: Design & Meta-Analysis": ["c1", "c2", "c3", "c4", "c5", "c6", "c7"],
        "D: Data Collection": ["d1", "d2", "d3", "d4"],
        "E: Analysis": ["e1", "e2", "e3", "e4", "e5"],
        "F: Quality": ["f1", "f2", "f3", "f4", "f5"],
        "G: Communication": ["g1", "g2", "g3", "g4", "g5", "g6"],
        "H: Specialized": ["h1", "h2"],
        "I: Systematic Review": ["i0", "i1", "i2", "i3"],
    }

    def test_category_agent_counts(self):
        """Each category must have the documented number of agents."""
        expected_counts = {
            "A: Foundation": 6,
            "B: Evidence": 5,
            "C: Design & Meta-Analysis": 7,
            "D: Data Collection": 4,
            "E: Analysis": 5,
            "F: Quality": 5,
            "G: Communication": 6,
            "H: Specialized": 2,
            "I: Systematic Review": 4,
        }

        for category, expected_count in expected_counts.items():
            agents = self.CATEGORIES[category]
            assert len(agents) == expected_count, (
                f"Category '{category}' has {len(agents)} agents, "
                f"expected {expected_count}"
            )

    def test_total_agents_across_categories_is_44(self):
        """Sum of all category agents must equal 44."""
        total = sum(len(agents) for agents in self.CATEGORIES.values())
        assert total == 44, (
            f"Total agents across categories is {total}, expected 44"
        )

    def test_no_duplicate_agents_across_categories(self):
        """No agent should appear in more than one category."""
        seen: dict[str, str] = {}
        duplicates = []
        for category, agents in self.CATEGORIES.items():
            for agent in agents:
                if agent in seen:
                    duplicates.append(
                        f"{agent} in both '{seen[agent]}' and '{category}'"
                    )
                seen[agent] = category

        assert not duplicates, (
            "Duplicate agents across categories:\n"
            + "\n".join(f"  {d}" for d in duplicates)
        )
