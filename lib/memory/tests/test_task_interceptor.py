"""Tests for Layer 2 Task Interceptor."""

import pytest
from pathlib import Path
from datetime import datetime
import yaml
import tempfile
import shutil

from memory.src.task_interceptor import (
    extract_agent_id,
    detect_project_root,
    intercept_task_call,
    load_full_research_context,
    detect_current_stage,
)
from memory.src.task_interceptor_models import ResearchContext, ProjectState, Decision, CheckpointState


class TestExtractAgentId:
    """Tests for extract_agent_id function."""

    def test_valid_diverga_agent(self):
        assert extract_agent_id("diverga:a1") == "a1"
        assert extract_agent_id("diverga:c4-metaanalyst") == "c4-metaanalyst"
        assert extract_agent_id("diverga:g5") == "g5"

    def test_non_diverga_agent(self):
        assert extract_agent_id("oh-my-claudecode:executor") is None
        assert extract_agent_id("general-purpose") is None

    def test_invalid_input(self):
        assert extract_agent_id("") is None
        assert extract_agent_id(None) is None
        assert extract_agent_id("invalid:format:extra") is None


class TestDetectProjectRoot:
    """Tests for detect_project_root function."""

    def test_finds_research_dir(self, tmp_path):
        # Create .research/ directory
        research_dir = tmp_path / ".research"
        research_dir.mkdir()

        # Create subdirectory
        subdir = tmp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)

        # Should find project root from subdirectory
        assert detect_project_root(subdir) == tmp_path

    def test_no_research_dir(self, tmp_path):
        # No .research/ directory exists
        assert detect_project_root(tmp_path) is None


class TestDetectCurrentStage:
    """Tests for detect_current_stage function."""

    def test_analysis_stage(self, tmp_path):
        changes_dir = tmp_path / ".research" / "changes" / "current"
        changes_dir.mkdir(parents=True)

        # Create analysis indicator file
        (changes_dir / "correlation_table.md").write_text("data")

        assert detect_current_stage(tmp_path) == "analysis"

    def test_methodology_stage(self, tmp_path):
        changes_dir = tmp_path / ".research" / "changes" / "current"
        changes_dir.mkdir(parents=True)

        (changes_dir / "sample_calculation.yaml").write_text("data")

        assert detect_current_stage(tmp_path) == "methodology"

    def test_default_foundation(self, tmp_path):
        # No changes directory exists
        assert detect_current_stage(tmp_path) == "foundation"


class TestLoadFullResearchContext:
    """Tests for load_full_research_context function."""

    def test_loads_complete_context(self, tmp_path):
        # Create .research/ structure
        research_dir = tmp_path / ".research"
        research_dir.mkdir()

        # Create project-state.yaml
        project_state = {
            "project_id": "test-project",
            "stage": "methodology",
            "created_at": "2024-01-01T00:00:00Z",
            "last_updated": "2024-01-15T12:00:00Z",
            "metadata": {"researcher": "Test User"}
        }
        with open(research_dir / "project-state.yaml", 'w') as f:
            yaml.dump(project_state, f)

        # Create decision-log.yaml
        decisions = {
            "decisions": [
                {
                    "timestamp": "2024-01-10T10:00:00Z",
                    "agent_id": "a1",
                    "decision": "Refined research question",
                    "rationale": "Scope too broad",
                    "impact": "Narrowed focus",
                    "checkpoint_triggered": "CP_RESEARCH_DIRECTION"
                }
            ]
        }
        with open(research_dir / "decision-log.yaml", 'w') as f:
            yaml.dump(decisions, f)

        # Create checkpoints.yaml
        checkpoints = {
            "checkpoints": {
                "CP_RESEARCH_DIRECTION": {
                    "status": "completed",
                    "triggered_at": "2024-01-10T10:00:00Z",
                    "completed_at": "2024-01-10T10:30:00Z",
                    "triggered_by": "a1"
                },
                "CP_PARADIGM_SELECTION": {
                    "status": "pending"
                }
            }
        }
        with open(research_dir / "checkpoints.yaml", 'w') as f:
            yaml.dump(checkpoints, f)

        # Load context
        context = load_full_research_context(tmp_path)

        assert context.project_state.project_id == "test-project"
        assert context.project_state.stage == "methodology"
        assert len(context.recent_decisions) == 1
        assert context.recent_decisions[0].agent_id == "a1"
        assert len(context.checkpoints) == 2
        assert context.checkpoints["CP_RESEARCH_DIRECTION"].status == "completed"
        assert context.checkpoints["CP_PARADIGM_SELECTION"].status == "pending"

    def test_missing_project_state(self, tmp_path):
        research_dir = tmp_path / ".research"
        research_dir.mkdir()

        with pytest.raises(FileNotFoundError):
            load_full_research_context(tmp_path)


class TestInterceptTaskCall:
    """Tests for intercept_task_call function."""

    def test_non_diverga_agent_returns_original(self):
        original = "Fix the bug in module.py"
        result = intercept_task_call("oh-my-claudecode:executor", original)
        assert result == original

    def test_no_project_root_returns_original(self):
        original = "Analyze research question"
        result = intercept_task_call("diverga:a1", original)
        # Should return original since no .research/ found
        assert result == original

    def test_injects_context_for_diverga_agent(self, tmp_path, monkeypatch):
        # Setup project structure
        research_dir = tmp_path / ".research"
        research_dir.mkdir()

        project_state = {
            "project_id": "test-project",
            "stage": "foundation",
            "created_at": "2024-01-01T00:00:00Z",
            "last_updated": "2024-01-15T12:00:00Z"
        }
        with open(research_dir / "project-state.yaml", 'w') as f:
            yaml.dump(project_state, f)

        (research_dir / "decision-log.yaml").write_text("decisions: []\n")

        checkpoints = {
            "checkpoints": {
                "CP_PARADIGM_SELECTION": {
                    "status": "pending"
                }
            }
        }
        with open(research_dir / "checkpoints.yaml", 'w') as f:
            yaml.dump(checkpoints, f)

        # Mock detect_project_root to return our tmp_path
        monkeypatch.setattr(
            "memory.src.task_interceptor.detect_project_root",
            lambda: tmp_path
        )

        original_prompt = "Analyze the research paradigm"
        result = intercept_task_call("diverga:a5", original_prompt)

        # Check injection markers
        assert "DIVERGA MEMORY SYSTEM v7.0" in result
        assert "RESEARCH CONTEXT" in result
        assert "test-project" in result
        assert "CP_PARADIGM_SELECTION" in result
        assert "Your Role: Agent A5" in result
        assert original_prompt in result


class TestResearchContextPromptInjection:
    """Tests for ResearchContext.to_prompt_section method."""

    def test_formats_context_correctly(self):
        project_state = ProjectState(
            project_id="test-project",
            stage="methodology",
            created_at="2024-01-01T00:00:00Z",
            last_updated="2024-01-15T12:00:00Z"
        )

        decisions = [
            Decision(
                timestamp="2024-01-10T10:00:00Z",
                agent_id="a1",
                decision="Refined RQ",
                rationale="Too broad",
                impact="Narrowed",
                checkpoint_triggered="CP_RESEARCH_DIRECTION"
            )
        ]

        checkpoints = {
            "CP_PARADIGM": CheckpointState(
                id="CP_PARADIGM",
                status="pending"
            )
        }

        context = ResearchContext(
            project_state=project_state,
            recent_decisions=decisions,
            checkpoints=checkpoints,
            current_stage="methodology"
        )

        prompt = context.to_prompt_section()

        assert "test-project" in prompt
        assert "methodology" in prompt
        assert "Refined RQ" in prompt
        assert "CP_PARADIGM" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
