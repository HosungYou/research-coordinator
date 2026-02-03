"""Layer 2 Task Interceptor for Diverga Memory System v7.0.

Intercepts Task tool calls to diverga: agents and injects full research context.
"""

import re
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

# Support both package-relative and standalone imports
try:
    from .task_interceptor_models import ResearchContext, ProjectState, Decision, CheckpointState
    from .checkpoint_trigger import CheckpointTrigger
except ImportError:
    from task_interceptor_models import ResearchContext, ProjectState, Decision, CheckpointState
    from checkpoint_trigger import CheckpointTrigger


def extract_agent_id(subagent_type: str) -> Optional[str]:
    """
    Extract agent ID from subagent_type string.

    Args:
        subagent_type: Agent type string (e.g., "diverga:a1", "oh-my-claudecode:executor")

    Returns:
        Agent ID if diverga agent, None otherwise

    Examples:
        >>> extract_agent_id("diverga:a1")
        'a1'
        >>> extract_agent_id("diverga:c4-metaanalyst")
        'c4-metaanalyst'
        >>> extract_agent_id("oh-my-claudecode:executor")
        None
    """
    if not subagent_type or not isinstance(subagent_type, str):
        return None

    # Match pattern: diverga:AGENT_ID
    match = re.match(r'^diverga:([a-z0-9-]+)$', subagent_type.lower())
    if match:
        return match.group(1)

    return None


def detect_project_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Walk up directories to find .research/ folder.

    Args:
        start_path: Starting directory (defaults to current working directory)

    Returns:
        Path to project root containing .research/, or None if not found

    Examples:
        >>> detect_project_root(Path("/project/subdir/file.py"))
        Path("/project")  # if /project/.research/ exists
    """
    if start_path is None:
        start_path = Path.cwd()
    elif isinstance(start_path, str):
        start_path = Path(start_path)

    # Walk up to root
    current = start_path.resolve()
    for parent in [current] + list(current.parents):
        research_dir = parent / ".research"
        if research_dir.exists() and research_dir.is_dir():
            return parent

    return None


def load_full_research_context(project_root: Path) -> ResearchContext:
    """
    Load complete research context from .research/ directory.

    Args:
        project_root: Project root directory containing .research/

    Returns:
        ResearchContext with all loaded data

    Raises:
        FileNotFoundError: If required files are missing
        yaml.YAMLError: If YAML parsing fails
    """
    research_dir = project_root / ".research"

    # Load project state
    project_state_path = research_dir / "project-state.yaml"
    if not project_state_path.exists():
        raise FileNotFoundError(f"Missing {project_state_path}")

    with open(project_state_path, 'r') as f:
        state_data = yaml.safe_load(f) or {}

    project_state = ProjectState(
        project_id=state_data.get('project_id', 'unknown'),
        stage=state_data.get('stage', 'foundation'),
        created_at=state_data.get('created_at', datetime.utcnow().isoformat()),
        last_updated=state_data.get('last_updated', datetime.utcnow().isoformat()),
        metadata=state_data.get('metadata', {})
    )

    # Load decision log (last 5 decisions)
    decision_log_path = research_dir / "decision-log.yaml"
    recent_decisions = []
    if decision_log_path.exists():
        with open(decision_log_path, 'r') as f:
            decisions_data = yaml.safe_load(f) or {}
            decisions_list = decisions_data.get('decisions', [])

        for dec_data in decisions_list[-5:]:  # Last 5 decisions
            recent_decisions.append(Decision(
                timestamp=dec_data.get('timestamp', ''),
                agent_id=dec_data.get('agent_id', 'unknown'),
                decision=dec_data.get('decision', ''),
                rationale=dec_data.get('rationale', ''),
                impact=dec_data.get('impact', ''),
                checkpoint_triggered=dec_data.get('checkpoint_triggered')
            ))

    # Load checkpoints state
    checkpoints_path = research_dir / "checkpoints.yaml"
    checkpoints = {}
    if checkpoints_path.exists():
        with open(checkpoints_path, 'r') as f:
            checkpoints_data = yaml.safe_load(f) or {}

        for cp_id, cp_data in checkpoints_data.get('checkpoints', {}).items():
            checkpoints[cp_id] = CheckpointState(
                id=cp_id,
                status=cp_data.get('status', 'pending'),
                triggered_at=cp_data.get('triggered_at'),
                completed_at=cp_data.get('completed_at'),
                triggered_by=cp_data.get('triggered_by'),
                validation_result=cp_data.get('validation_result')
            )

    # Detect current stage from filesystem
    current_stage = detect_current_stage(project_root)

    return ResearchContext(
        project_state=project_state,
        recent_decisions=recent_decisions,
        checkpoints=checkpoints,
        current_stage=current_stage
    )


def detect_current_stage(project_root: Path) -> str:
    """
    Detect current research stage from filesystem state.

    Args:
        project_root: Project root directory

    Returns:
        Stage name: "analysis", "methodology", "design", or "foundation"
    """
    changes_dir = project_root / ".research" / "changes" / "current"

    if not changes_dir.exists():
        return "foundation"

    # Check for stage indicators
    stage_indicators = {
        "analysis": ["correlation_table.md", "effect_sizes.yaml"],
        "methodology": ["sample_calculation.yaml", "statistical_plan.yaml"],
        "design": ["variable_definitions.yaml", "hypothesis_map.yaml"],
        "foundation": ["theory_map.yaml", "literature_gaps.yaml"]
    }

    for stage, indicators in stage_indicators.items():
        for indicator in indicators:
            if (changes_dir / indicator).exists():
                return stage

    return "foundation"


def intercept_task_call(subagent_type: str, prompt: str) -> str:
    """
    Main interception function for Task tool calls.

    Injects full research context and checkpoint instructions into prompt
    for diverga: agents.

    Args:
        subagent_type: Agent type string
        prompt: Original prompt from user

    Returns:
        Modified prompt with injected context (or original if not diverga agent)

    Examples:
        >>> intercept_task_call("diverga:a1", "Analyze theory")
        # Returns prompt with injected research context

        >>> intercept_task_call("oh-my-claudecode:executor", "Fix bug")
        "Fix bug"  # Returns original prompt unchanged
    """
    try:
        # Step 1: Check if this is a diverga agent
        agent_id = extract_agent_id(subagent_type)
        if not agent_id:
            return prompt  # Not a diverga agent, return original

        # Step 2: Detect project root
        project_root = detect_project_root()
        if not project_root:
            # No .research/ folder found, return original prompt
            return prompt

        # Step 3: Load full research context
        try:
            context = load_full_research_context(project_root)
        except (FileNotFoundError, yaml.YAMLError) as e:
            # Context loading failed, log error and return original
            print(f"Warning: Failed to load research context: {e}")
            return prompt

        # Step 4: Check for pending checkpoints
        pending_checkpoints = [
            (cp_id, cp) for cp_id, cp in context.checkpoints.items()
            if cp.status in ["pending", "active"]
        ]

        # Step 5: Build injected prompt
        injection_sections = []

        # Header
        injection_sections.append("=" * 80)
        injection_sections.append("DIVERGA MEMORY SYSTEM v7.0 - RESEARCH CONTEXT")
        injection_sections.append("=" * 80)
        injection_sections.append("")

        # Research context
        injection_sections.append(context.to_prompt_section())
        injection_sections.append("")

        # Checkpoint instructions
        if pending_checkpoints:
            injection_sections.append("## Checkpoint Instructions")
            injection_sections.append("You MUST address these checkpoints:")
            injection_sections.append("")
            for cp_id, cp in pending_checkpoints:
                # Format checkpoint instruction inline
                emoji = "🔴" if cp.status == "active" else "🟠"
                action = "STOP and validate" if cp.status == "active" else "Review and document"
                injection_sections.append(f"- {emoji} {cp_id}: {action}")
            injection_sections.append("")

        # Agent-specific guidance
        injection_sections.append(f"## Your Role: Agent {agent_id.upper()}")
        injection_sections.append("Consider the above context when responding.")
        injection_sections.append("If you trigger new checkpoints, mark them with 🔴/🟠/🔵.")
        injection_sections.append("")
        injection_sections.append("=" * 80)
        injection_sections.append("ORIGINAL REQUEST")
        injection_sections.append("=" * 80)
        injection_sections.append("")

        # Combine injection + original prompt
        injected_context = "\n".join(injection_sections)
        modified_prompt = f"{injected_context}{prompt}"

        return modified_prompt

    except Exception as e:
        # Graceful fallback on any error
        print(f"Error in task interception: {e}")
        return prompt


# Convenience function for external use
def inject_context_if_diverga(subagent_type: str, prompt: str) -> str:
    """
    Convenience wrapper for intercept_task_call.

    Use this function when integrating with Task tool wrappers.
    """
    return intercept_task_call(subagent_type, prompt)
