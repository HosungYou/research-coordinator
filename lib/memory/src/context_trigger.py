"""
Diverga Memory System v7.0 - Layer 1: Context Trigger System

Keyword-based detection for automatic research context loading.
Provides smart context presentation when users ask about their research status.

Author: Diverga Team
License: MIT
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

try:
    from ruamel.yaml import YAML
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
except ImportError:
    import yaml as yaml_fallback
    yaml = None


# ============================================================================
# CONTEXT TRIGGER KEYWORDS
# ============================================================================

CONTEXT_TRIGGER_KEYWORDS = {
    "english": [
        "my research",
        "research status",
        "research progress",
        "where was i",
        "continue research",
        "what stage",
        "research question",
        "my project",
        "current stage",
        "project status",
        "where am i",
        "what's next",
        "next step",
        "project state",
        "research state",
    ],
    "korean": [
        "내 연구",
        "연구 진행",
        "연구 상태",
        "어디까지",
        "지금 단계",
        "연구 계속",
        "연구 질문",
        "내 프로젝트",
        "현재 단계",
        "프로젝트 상태",
        "어디 있어",
        "다음 단계",
        "다음 스텝",
        "프로젝트 진행",
        "연구 현황",
    ]
}


# ============================================================================
# CHECKPOINT ICONS AND DESCRIPTIONS
# ============================================================================

CHECKPOINT_ICONS = {
    "required": "🔴",
    "recommended": "🟠",
    "optional": "🟡"
}


# ============================================================================
# STAGE GUIDANCE TEMPLATES
# ============================================================================

STAGE_GUIDANCE = {
    "foundation": {
        "en": "Focus on clarifying your research question and selecting a theoretical framework.",
        "ko": "연구 질문 구체화와 이론적 틀 선정에 집중하세요."
    },
    "evidence": {
        "en": "Conduct systematic literature review and assess evidence quality.",
        "ko": "체계적 문헌고찰을 수행하고 증거의 질을 평가하세요."
    },
    "design": {
        "en": "Finalize your research methodology and data collection plan.",
        "ko": "연구 방법론과 데이터 수집 계획을 확정하세요."
    },
    "collection": {
        "en": "Execute data collection following your approved protocol.",
        "ko": "승인된 프로토콜에 따라 데이터를 수집하세요."
    },
    "analysis": {
        "en": "Analyze data using appropriate statistical/qualitative methods.",
        "ko": "적절한 통계/질적 방법으로 데이터를 분석하세요."
    },
    "quality": {
        "en": "Review quality, check for biases, and ensure reproducibility.",
        "ko": "품질을 검토하고 편향을 확인하며 재현성을 보장하세요."
    },
    "communication": {
        "en": "Prepare manuscript and response to reviewers.",
        "ko": "논문을 작성하고 리뷰어 응답을 준비하세요."
    },
    "default": {
        "en": "Continue with the next task in your research pipeline.",
        "ko": "연구 파이프라인의 다음 작업을 계속 진행하세요."
    }
}


# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def should_load_context(user_message: str) -> bool:
    """
    Check if user message contains context trigger keywords.

    Args:
        user_message: User's input message

    Returns:
        True if context should be loaded, False otherwise
    """
    if not user_message:
        return False

    message_lower = user_message.lower()

    # Check English keywords
    for keyword in CONTEXT_TRIGGER_KEYWORDS["english"]:
        if keyword.lower() in message_lower:
            return True

    # Check Korean keywords
    for keyword in CONTEXT_TRIGGER_KEYWORDS["korean"]:
        if keyword in user_message:  # Korean is case-sensitive
            return True

    return False


def load_and_display_context(project_root: Path) -> str:
    """
    Load research context from .research directory and format for display.

    Args:
        project_root: Path to project root directory

    Returns:
        Formatted markdown string with research context
    """
    research_dir = project_root / ".research"
    project_state_file = research_dir / "project-state.yaml"
    decision_log_file = research_dir / "decision-log.yaml"

    # Check if project exists
    if not research_dir.exists() or not project_state_file.exists():
        return format_no_project_message()

    try:
        # Load project state
        project_state = _load_yaml_file(project_state_file)
        if not project_state:
            return _format_no_project_message()

        # Load decision log (may not exist yet)
        decisions = []
        if decision_log_file.exists():
            decision_log = _load_yaml_file(decision_log_file)
            if decision_log and "decisions" in decision_log:
                decisions = decision_log["decisions"]

        # Build context display
        context_parts = []

        # Header
        context_parts.append("# 🎯 Your Research Context\n")

        # Project Status section
        context_parts.append(format_project_status(project_state))

        # Recent Decisions section
        if decisions:
            context_parts.append(format_recent_decisions(decisions[-3:]))  # Last 3

        # Pending Checkpoints section
        pending_checkpoints = extract_pending_checkpoints(project_state)
        if pending_checkpoints:
            context_parts.append(format_pending_checkpoints(pending_checkpoints))

        # Next Step Guidance section
        current_stage = project_state.get("current_stage", "default")
        context_parts.append(format_next_step_guidance(current_stage))

        return "\n\n".join(context_parts)

    except Exception as e:
        return f"⚠️ Error loading research context: {str(e)}\n\nPlease check your `.research/` directory structure."


# ============================================================================
# FORMATTING FUNCTIONS
# ============================================================================

def format_project_status(project_state: Dict[str, Any]) -> str:
    """Format project status section."""
    lines = ["## 📊 Project Status\n"]

    # Project name
    project_name = project_state.get("project_name", "Untitled Project")
    lines.append(f"**Project:** {project_name}")

    # Research question
    research_question = project_state.get("research_question", "Not yet defined")
    lines.append(f"**Research Question:** {research_question}")

    # Current stage
    current_stage = project_state.get("current_stage", "initialization")
    lines.append(f"**Current Stage:** {current_stage}")

    # Paradigm
    paradigm = project_state.get("paradigm", "Not selected")
    lines.append(f"**Paradigm:** {paradigm}")

    # Completed stages
    completed_stages = project_state.get("completed_stages", [])
    if completed_stages:
        lines.append(f"**Completed Stages:** {', '.join(completed_stages)}")

    # Last updated
    last_updated = project_state.get("last_updated", "Unknown")
    if isinstance(last_updated, datetime):
        last_updated = last_updated.strftime("%Y-%m-%d %H:%M")
    lines.append(f"**Last Updated:** {last_updated}")

    return "\n".join(lines)


def extract_pending_checkpoints(project_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract pending checkpoints from project state."""
    pending = []

    # Check if checkpoints section exists
    checkpoints = project_state.get("checkpoints", {})
    if not checkpoints:
        return []

    # Extract pending checkpoints
    for checkpoint_name, checkpoint_data in checkpoints.items():
        if isinstance(checkpoint_data, dict):
            status = checkpoint_data.get("status", "pending")
            if status == "pending":
                pending.append({
                    "name": checkpoint_name,
                    "level": checkpoint_data.get("level", "optional"),
                    "description": checkpoint_data.get("description", ""),
                    "human_action": checkpoint_data.get("human_action", "")
                })

    return pending


def format_next_step_guidance(current_stage: str) -> str:
    """Format next step guidance section."""
    guidance_text = get_next_step_guidance(current_stage)

    lines = ["## 🎯 Next Step Guidance\n"]
    lines.append(guidance_text)
    lines.append("\n**Available Commands:**")
    lines.append("- `Continue research` - Resume where you left off")
    lines.append("- `Show agents` - List available research agents")
    lines.append("- `View decisions` - See full decision history")

    return "\n".join(lines)


def format_recent_decisions(decisions: List[Dict[str, Any]]) -> str:
    """
    Format recent decisions as markdown list.

    Args:
        decisions: List of decision dictionaries

    Returns:
        Formatted markdown string
    """
    if not decisions:
        return ""

    lines = ["## 📋 Recent Decisions\n"]

    for decision in decisions[-3:]:  # Last 3 decisions
        timestamp = decision.get("timestamp", "Unknown time")
        decision_type = decision.get("type", "Decision")
        description = decision.get("description", "No description")
        agent = decision.get("agent", "N/A")

        # Format timestamp if it's a datetime object or ISO string
        if isinstance(timestamp, datetime):
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M")
        elif isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                timestamp_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                timestamp_str = timestamp
        else:
            timestamp_str = str(timestamp)

        lines.append(f"- **{decision_type}** ({timestamp_str})")
        lines.append(f"  - {description}")
        if agent != "N/A":
            lines.append(f"  - Agent: {agent}")
        lines.append("")

    return "\n".join(lines)


def format_pending_checkpoints(checkpoints: List[Dict[str, Any]]) -> str:
    """
    Format pending checkpoints as markdown.

    Args:
        checkpoints: List of checkpoint dictionaries

    Returns:
        Formatted markdown string
    """
    if not checkpoints:
        return ""

    lines = ["## 🚦 Pending Checkpoints\n"]

    for checkpoint in checkpoints:
        level = checkpoint.get("level", "optional")
        icon = CHECKPOINT_ICONS.get(level, "🟡")
        name = checkpoint.get("name", "Unknown")
        description = checkpoint.get("description", "")
        human_action = checkpoint.get("human_action", "")

        lines.append(f"{icon} **{name}** ({level.upper()})")
        if description:
            lines.append(f"   - {description}")
        if human_action:
            lines.append(f"   - Required action: {human_action}")
        lines.append("")

    return "\n".join(lines)


def get_next_step_guidance(current_stage: str) -> str:
    """
    Return stage-appropriate guidance text.

    Args:
        current_stage: Current research stage identifier

    Returns:
        Guidance text in both English and Korean
    """
    # Map stage to guidance category
    stage_map = {
        "foundation": ["research_question", "theory", "paradigm"],
        "evidence": ["literature", "systematic_review"],
        "design": ["methodology", "design", "instrument"],
        "collection": ["sampling", "data_collection", "interview"],
        "analysis": ["analysis", "coding", "statistics"],
        "quality": ["quality", "bias", "reproducibility"],
        "communication": ["writing", "journal", "peer_review"],
    }

    # Find matching category
    guidance_key = "default"
    current_stage_lower = current_stage.lower()

    # First, try direct category match
    if current_stage_lower in stage_map:
        guidance_key = current_stage_lower
    else:
        # Then try keyword matching
        for category, keywords in stage_map.items():
            if any(keyword in current_stage_lower for keyword in keywords):
                guidance_key = category
                break

    guidance = STAGE_GUIDANCE.get(guidance_key, STAGE_GUIDANCE["default"])
    return f"{guidance['en']}\n{guidance['ko']}"


# ============================================================================
# INTERNAL HELPER FUNCTIONS
# ============================================================================

def _load_yaml_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load YAML file using ruamel.yaml or fallback to PyYAML."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if yaml and hasattr(yaml, 'load'):
                return yaml.load(f)
            else:
                return yaml_fallback.safe_load(f)
    except Exception as e:
        print(f"Warning: Could not load {file_path}: {e}")
        return None


def format_no_project_message() -> str:
    """Return helpful message when no project is found."""
    return """
# 🔍 No Research Project Found

It looks like you don't have an active research project in this directory.

**To start a new project:**
1. Say: "Start a new research project" or "새 연구 프로젝트 시작"
2. Or use: `/diverga:setup`

**Looking for an existing project?**
- Make sure you're in the correct directory
- Check if `.research/` folder exists
- Run `/diverga:list` to see all projects
"""


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Test keyword detection
    test_messages = [
        "What is my research question?",
        "내 연구 진행 상황 알려줘",
        "Where was I in my project?",
        "어디까지 했더라?",
        "Just a random message",
    ]

    print("Testing keyword detection:")
    for msg in test_messages:
        result = should_load_context(msg)
        print(f"  '{msg}' -> {result}")

    # Test context loading
    print("\nTesting context loading:")
    test_project_root = Path("/Volumes/External SSD/Projects/Research/Diverga")
    context = load_and_display_context(test_project_root)
    print(context[:500] + "..." if len(context) > 500 else context)
