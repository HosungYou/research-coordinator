"""
Unit tests for Layer 1: Context Trigger System

Tests keyword detection and context loading functionality.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from context_trigger import (
    should_load_context,
    load_and_display_context,
    format_recent_decisions,
    format_pending_checkpoints,
    get_next_step_guidance,
    CONTEXT_TRIGGER_KEYWORDS,
)


class TestKeywordDetection:
    """Test keyword detection for context triggers."""

    def test_english_keywords(self):
        """Test English keyword detection."""
        test_cases = [
            ("What is my research question?", True),
            ("Show me my research status", True),
            ("Where was I in the project?", True),
            ("Continue my research", True),
            ("What stage am I at?", True),
            ("Just a random message", False),
            ("Hello world", False),
        ]

        for message, expected in test_cases:
            result = should_load_context(message)
            assert result == expected, f"Failed for: {message}"

    def test_korean_keywords(self):
        """Test Korean keyword detection."""
        test_cases = [
            ("내 연구 진행 상황 알려줘", True),
            ("연구 어디까지 했어?", True),
            ("지금 단계가 뭐야?", True),
            ("연구 계속 하자", True),
            ("안녕하세요", False),
            ("날씨가 좋네요", False),
        ]

        for message, expected in test_cases:
            result = should_load_context(message)
            assert result == expected, f"Failed for: {message}"

    def test_case_insensitive_english(self):
        """Test case-insensitive English keyword matching."""
        assert should_load_context("MY RESEARCH STATUS")
        assert should_load_context("What Is My Research Question?")
        assert should_load_context("where was i")

    def test_empty_message(self):
        """Test empty message handling."""
        assert not should_load_context("")
        assert not should_load_context(None)


class TestContextLoading:
    """Test context loading from project files."""

    def test_no_project_message(self):
        """Test message when no project exists."""
        non_existent_path = Path("/non/existent/path")
        context = load_and_display_context(non_existent_path)

        assert "No Research Project Found" in context
        assert "To start a new project" in context

    def test_with_sample_project(self):
        """Test loading with sample project data."""
        # Use the test sample in Diverga root
        project_root = Path("/Volumes/External SSD/Projects/Research/Diverga")

        context = load_and_display_context(project_root)

        # Check if main sections are present
        assert "Your Research Context" in context or "No Research Project Found" in context


class TestFormatting:
    """Test formatting functions."""

    def test_format_recent_decisions(self):
        """Test decision formatting."""
        decisions = [
            {
                "timestamp": "2026-02-03T10:30:00Z",
                "type": "Research Question",
                "description": "Approved research question",
                "agent": "A1-research-question-refiner",
            },
            {
                "timestamp": "2026-02-03T10:35:00Z",
                "type": "Paradigm Selection",
                "description": "Selected quantitative paradigm",
                "agent": "A5-paradigm-worldview-advisor",
            },
        ]

        result = format_recent_decisions(decisions)

        assert "Recent Decisions" in result
        assert "Research Question" in result
        assert "Paradigm Selection" in result
        assert "A1-research-question-refiner" in result

    def test_format_pending_checkpoints(self):
        """Test checkpoint formatting."""
        checkpoints = [
            {
                "name": "CP_THEORY_SELECTION",
                "level": "required",
                "description": "Theoretical framework selection",
                "human_action": "Select and approve theoretical framework",
            },
            {
                "name": "CP_ANALYSIS_PLAN",
                "level": "recommended",
                "description": "Analysis plan review",
                "human_action": "Review statistical analysis plan",
            },
        ]

        result = format_pending_checkpoints(checkpoints)

        assert "Pending Checkpoints" in result
        assert "🔴" in result  # Required icon
        assert "🟠" in result  # Recommended icon
        assert "CP_THEORY_SELECTION" in result
        assert "CP_ANALYSIS_PLAN" in result

    def test_get_next_step_guidance(self):
        """Test stage guidance generation."""
        # Test foundation stage
        guidance = get_next_step_guidance("foundation")
        assert "research question" in guidance.lower()
        assert "연구 질문" in guidance or "이론적" in guidance

        # Test evidence stage
        guidance = get_next_step_guidance("evidence")
        assert "literature" in guidance.lower() or "systematic" in guidance.lower()

        # Test default stage
        guidance = get_next_step_guidance("unknown_stage")
        assert "Continue" in guidance or "pipeline" in guidance.lower()


class TestKeywordCoverage:
    """Test keyword list coverage."""

    def test_all_english_keywords_work(self):
        """Test that all documented English keywords trigger context."""
        for keyword in CONTEXT_TRIGGER_KEYWORDS["english"]:
            message = f"Can you tell me about {keyword}?"
            assert should_load_context(message), f"Keyword failed: {keyword}"

    def test_all_korean_keywords_work(self):
        """Test that all documented Korean keywords trigger context."""
        for keyword in CONTEXT_TRIGGER_KEYWORDS["korean"]:
            message = f"{keyword} 보여줘"
            assert should_load_context(message), f"Keyword failed: {keyword}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
