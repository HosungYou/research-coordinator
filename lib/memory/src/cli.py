"""
Diverga Memory System v7.0 - CLI Command Module

This module provides command-line interface for the Diverga Memory System,
allowing researchers to interact with project state, decisions, and checkpoints
through simple commands.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None

# Import core modules
try:
    from .models import ResearchContext, Decision, Amendment, Checkpoint
    from .fs_state import FilesystemState, load_yaml, save_yaml
    from .decision_log import DecisionLog
    from .archive import ArchiveManager
except ImportError:
    # For standalone execution
    from models import ResearchContext, Decision, Amendment, Checkpoint
    from fs_state import FilesystemState, load_yaml, save_yaml
    from decision_log import DecisionLog
    from archive import ArchiveManager


# ============================================================================
# CLI Entry Point
# ============================================================================


def run_cli(command: str, args: List[str] = None) -> str:
    """
    Main CLI entry point that dispatches commands.

    Args:
        command: Command name (status, context, init, etc.)
        args: List of command arguments

    Returns:
        Formatted output string for display

    Example:
        >>> run_cli("status", ["--verbose"])
        >>> run_cli("init", ["--name", "My Project", "--question", "..."])
    """
    if args is None:
        args = []

    # Dispatch to command handlers
    command_map = {
        'status': cmd_status,
        'context': cmd_context,
        'init': cmd_init,
        'decision': cmd_decision,
        'archive': cmd_archive,
        'generate': cmd_generate,
        'migrate': cmd_migrate,
    }

    handler = command_map.get(command.lower())
    if not handler:
        return format_error(f"Unknown command: {command}")

    try:
        return handler(args)
    except Exception as e:
        return format_error(f"Command failed: {str(e)}")


# ============================================================================
# Command Handlers
# ============================================================================


def cmd_status(args: List[str]) -> str:
    """
    Show research project status.

    Command: diverga memory status [--verbose]

    Args:
        args: Command arguments

    Returns:
        Formatted status report
    """
    parsed_args = parse_args(args)
    verbose = parsed_args.get('verbose', False)

    project_root = Path.cwd()
    fs_state = FilesystemState(project_root)

    # Check if project is initialized
    if not fs_state.is_initialized():
        return format_error(
            "No Diverga project found in current directory.\n"
            "Run 'diverga memory init' to create a new project."
        )

    # Load project state
    state = fs_state.get_project_state()
    if not state:
        return format_error("Failed to load project state")

    # Load recent decisions
    decision_log = DecisionLog(project_root)
    recent_decisions = decision_log.get_recent_decisions(limit=3)

    # Build status output
    output_lines = [
        "# 📊 Research Project Status",
        "",
        f"**Project**: {state.get('project_name', 'Unknown')}",
        f"**Research Question**: {state.get('research_question', 'Not set')}",
        f"**Paradigm**: {state.get('paradigm', 'Not set')}",
        "",
        f"**Current Stage**: {state.get('current_stage', 'Unknown')}",
        f"**Last Updated**: {state.get('updated_at', 'Unknown')}",
        "",
    ]

    # Recent decisions
    if recent_decisions:
        output_lines.extend([
            "## 📋 Recent Decisions (Last 3)",
            "",
        ])
        for i, decision in enumerate(recent_decisions, 1):
            checkpoint_id = decision.get('checkpoint', 'Unknown')
            selected = decision.get('decision', {}).get('selected', 'N/A')
            timestamp = decision.get('timestamp', 'Unknown')

            output_lines.extend([
                f"{i}. **{checkpoint_id}**",
                f"   - Selected: {selected}",
                f"   - Timestamp: {timestamp}",
                "",
            ])
    else:
        output_lines.extend([
            "## 📋 Recent Decisions",
            "",
            "No decisions recorded yet.",
            "",
        ])

    # Pending checkpoints
    pending_checkpoints = state.get('pending_checkpoints', [])
    if pending_checkpoints:
        output_lines.extend([
            "## 🚦 Pending Checkpoints",
            "",
        ])
        for cp_id in pending_checkpoints:
            output_lines.append(f"- {cp_id}")
        output_lines.append("")
    else:
        output_lines.extend([
            "## 🚦 Pending Checkpoints",
            "",
            "No pending checkpoints.",
            "",
        ])

    # Verbose mode: Add full context
    if verbose:
        output_lines.extend([
            "## 📁 Project Files",
            "",
            f"- State file: {fs_state.state_file}",
            f"- Decision log: {fs_state.decision_file}",
            f"- Checkpoints: {fs_state.checkpoints_file}",
            "",
        ])

        # Session count
        sessions = state.get('sessions', [])
        output_lines.append(f"**Total Sessions**: {len(sessions)}")
        output_lines.append("")

    return '\n'.join(output_lines)


def cmd_context(args: List[str]) -> str:
    """
    Show full research context.

    Command: diverga memory context [--verbose]

    Args:
        args: Command arguments

    Returns:
        Formatted context display
    """
    parsed_args = parse_args(args)
    verbose = parsed_args.get('verbose', False)

    project_root = Path.cwd()
    fs_state = FilesystemState(project_root)

    # Check if project is initialized
    if not fs_state.is_initialized():
        return format_error(
            "No Diverga project found in current directory.\n"
            "Run 'diverga memory init' to create a new project."
        )

    # Load project state
    state = fs_state.get_project_state()
    if not state:
        return format_error("Failed to load project state")

    # Load all decisions
    decision_log = DecisionLog(project_root)
    all_decisions = decision_log.log_data.get('decisions', [])

    # Build context output
    output_lines = [
        "# 🎯 Full Research Context",
        "",
        "## 📊 Project Overview",
        "",
        f"**Project Name**: {state.get('project_name', 'Unknown')}",
        f"**Research Question**: {state.get('research_question', 'Not set')}",
        f"**Paradigm**: {state.get('paradigm', 'Not set')}",
        f"**Current Stage**: {state.get('current_stage', 'Unknown')}",
        "",
        f"**Created**: {state.get('created_at', 'Unknown')}",
        f"**Last Updated**: {state.get('updated_at', 'Unknown')}",
        "",
    ]

    # All decisions
    if all_decisions:
        output_lines.extend([
            f"## 📋 All Decisions ({len(all_decisions)} total)",
            "",
        ])
        for i, decision in enumerate(all_decisions, 1):
            checkpoint_id = decision.get('checkpoint', 'Unknown')
            stage = decision.get('stage', 'Unknown')
            selected = decision.get('decision', {}).get('selected', 'N/A')

            output_lines.extend([
                f"{i}. **{checkpoint_id}** (Stage: {stage})",
                f"   - Selected: {selected}",
                "",
            ])

            if verbose:
                rationale = decision.get('rationale', 'No rationale')
                alternatives = decision.get('decision', {}).get('alternatives', [])
                output_lines.extend([
                    f"   - Rationale: {rationale}",
                    f"   - Alternatives: {', '.join(str(a) for a in alternatives) if alternatives else 'None'}",
                    "",
                ])
    else:
        output_lines.extend([
            "## 📋 Decisions",
            "",
            "No decisions recorded yet.",
            "",
        ])

    # Sessions
    sessions = state.get('sessions', [])
    if sessions and verbose:
        output_lines.extend([
            f"## 🕒 Sessions ({len(sessions)} total)",
            "",
        ])
        for session in sessions:
            session_id = session.get('session_id', 'Unknown')
            start_time = session.get('start_time', 'Unknown')
            output_lines.append(f"- {session_id} (Started: {start_time})")
        output_lines.append("")

    # Pending checkpoints
    pending_checkpoints = state.get('pending_checkpoints', [])
    if pending_checkpoints:
        output_lines.extend([
            "## 🚦 Pending Checkpoints",
            "",
        ])
        for cp_id in pending_checkpoints:
            output_lines.append(f"- {cp_id}")
        output_lines.append("")

    # Verbose: File paths
    if verbose:
        output_lines.extend([
            "## 📁 Project Structure",
            "",
            f"**Research Directory**: {fs_state.research_dir}",
            "",
            "Files:",
            f"- {fs_state.state_file.name}",
            f"- {fs_state.decision_file.name}",
            f"- {fs_state.checkpoints_file.name}",
            "",
        ])

    return '\n'.join(output_lines)


def cmd_init(args: List[str]) -> str:
    """
    Initialize new research project.

    Command: diverga memory init --name NAME --question QUESTION --paradigm PARADIGM

    Args:
        args: Command arguments

    Returns:
        Success or error message
    """
    parsed_args = parse_args(args)

    # Validate required arguments
    project_name = parsed_args.get('name')
    research_question = parsed_args.get('question')
    paradigm = parsed_args.get('paradigm', 'quantitative')

    if not project_name:
        return format_error("Missing required argument: --name")
    if not research_question:
        return format_error("Missing required argument: --question")

    # Validate paradigm
    valid_paradigms = ['quantitative', 'qualitative', 'mixed']
    if paradigm not in valid_paradigms:
        return format_error(
            f"Invalid paradigm: {paradigm}\n"
            f"Must be one of: {', '.join(valid_paradigms)}"
        )

    project_root = Path.cwd()
    fs_state = FilesystemState(project_root)

    # Check if already initialized
    if fs_state.is_initialized():
        return format_error(
            "Project already initialized in this directory.\n"
            "Use 'diverga memory status' to view current project."
        )

    # Initialize project
    success = fs_state.initialize_project(
        project_name=project_name,
        research_question=research_question,
        paradigm=paradigm
    )

    if not success:
        return format_error("Failed to initialize project")

    # Create initial decision log
    decision_log = DecisionLog(project_root)
    decision_log._save()

    # Return success message
    output_lines = [
        "# ✅ Project Initialized Successfully",
        "",
        f"**Project Name**: {project_name}",
        f"**Research Question**: {research_question}",
        f"**Paradigm**: {paradigm}",
        "",
        "**Directory Structure Created**:",
        f"- {fs_state.research_dir}/",
        f"  - baselines/",
        f"  - changes/current/",
        f"  - changes/archive/",
        f"  - sessions/",
        f"  - project-state.yaml",
        f"  - decision-log.yaml",
        f"  - checkpoints.yaml",
        "",
        "**Next Steps**:",
        "1. Use 'diverga memory status' to view project status",
        "2. Start working on your research with Diverga agents",
        "3. Decisions will be automatically tracked",
        "",
    ]

    return '\n'.join(output_lines)


def cmd_decision(args: List[str]) -> str:
    """
    Add or view decisions.

    Commands:
    - diverga memory decision list [--checkpoint CP_ID] [--stage STAGE]
    - diverga memory decision add --checkpoint CP_ID --selected OPTION --rationale RATIONALE
    - diverga memory decision amend --id DEC_ID --selected OPTION --rationale RATIONALE

    Args:
        args: Command arguments

    Returns:
        Formatted decision list or success message
    """
    if not args or len(args) == 0:
        return format_error("Missing decision subcommand (list/add/amend)")

    subcommand = args[0].lower()
    rest_args = args[1:] if len(args) > 1 else []

    if subcommand == 'list':
        return _decision_list(rest_args)
    elif subcommand == 'add':
        return _decision_add(rest_args)
    elif subcommand == 'amend':
        return _decision_amend(rest_args)
    else:
        return format_error(f"Unknown decision subcommand: {subcommand}")


def _decision_list(args: List[str]) -> str:
    """List decisions, optionally filtered by checkpoint or stage."""
    parsed_args = parse_args(args)

    checkpoint_id = parsed_args.get('checkpoint')
    stage = parsed_args.get('stage')

    project_root = Path.cwd()
    decision_log = DecisionLog(project_root)

    # Get decisions
    if checkpoint_id:
        decisions = decision_log.get_decision_history(checkpoint_id)
        title = f"Decisions for Checkpoint: {checkpoint_id}"
    elif stage:
        decisions = decision_log.get_stage_decisions(stage)
        title = f"Decisions for Stage: {stage}"
    else:
        decisions = decision_log.log_data.get('decisions', [])
        title = "All Decisions"

    if not decisions:
        return f"# {title}\n\nNo decisions found."

    # Format output
    output_lines = [
        f"# {title}",
        "",
        f"**Total**: {len(decisions)} decision(s)",
        "",
    ]

    for i, decision in enumerate(decisions, 1):
        decision_id = decision.get('id', 'Unknown')
        checkpoint = decision.get('checkpoint', 'Unknown')
        stage_val = decision.get('stage', 'Unknown')
        selected = decision.get('decision', {}).get('selected', 'N/A')
        rationale = decision.get('rationale', 'No rationale')
        timestamp = decision.get('timestamp', 'Unknown')

        output_lines.extend([
            f"## {i}. {decision_id}",
            "",
            f"- **Checkpoint**: {checkpoint}",
            f"- **Stage**: {stage_val}",
            f"- **Selected**: {selected}",
            f"- **Rationale**: {rationale}",
            f"- **Timestamp**: {timestamp}",
            "",
        ])

        # Show if this is an amendment
        if 'amends' in decision:
            output_lines.append(f"  *(Amends: {decision['amends']})*")
            output_lines.append("")

    return '\n'.join(output_lines)


def _decision_add(args: List[str]) -> str:
    """Add a new decision."""
    parsed_args = parse_args(args)

    checkpoint_id = parsed_args.get('checkpoint')
    selected = parsed_args.get('selected')
    rationale = parsed_args.get('rationale', '')

    if not checkpoint_id:
        return format_error("Missing required argument: --checkpoint")
    if not selected:
        return format_error("Missing required argument: --selected")

    project_root = Path.cwd()
    fs_state = FilesystemState(project_root)
    decision_log = DecisionLog(project_root)

    # Get current stage from project state
    state = fs_state.get_project_state()
    current_stage = state.get('current_stage', 'unknown')

    # Create decision entry
    decision = {
        'checkpoint': checkpoint_id,
        'stage': current_stage,
        'agent': 'manual',  # CLI-initiated
        'decision': {
            'selected': selected,
            'alternatives': []
        },
        'rationale': rationale,
        'metadata': {
            'user_confirmed': True
        }
    }

    # Add decision
    decision_id = decision_log.add_decision(decision)

    return (
        f"# ✅ Decision Added\n\n"
        f"**ID**: {decision_id}\n"
        f"**Checkpoint**: {checkpoint_id}\n"
        f"**Selected**: {selected}\n"
        f"**Stage**: {current_stage}\n"
    )


def _decision_amend(args: List[str]) -> str:
    """Amend an existing decision."""
    parsed_args = parse_args(args)

    decision_id = parsed_args.get('id')
    new_selected = parsed_args.get('selected')
    new_rationale = parsed_args.get('rationale', '')

    if not decision_id:
        return format_error("Missing required argument: --id")
    if not new_selected:
        return format_error("Missing required argument: --selected")

    project_root = Path.cwd()
    decision_log = DecisionLog(project_root)

    # Amend decision
    try:
        new_decision_id = decision_log.amend_decision(
            decision_id, new_selected, new_rationale
        )
    except ValueError as e:
        return format_error(str(e))

    return (
        f"# ✅ Decision Amended\n\n"
        f"**Original ID**: {decision_id}\n"
        f"**New ID**: {new_decision_id}\n"
        f"**New Selected**: {new_selected}\n"
    )


def cmd_archive(args: List[str]) -> str:
    """
    Archive current stage.

    Command: diverga memory archive [STAGE_ID] [--summary SUMMARY]

    Args:
        args: Command arguments

    Returns:
        Success message with archive path
    """
    parsed_args = parse_args(args)

    # Get stage ID (positional or from args)
    stage_id = None
    if args and not args[0].startswith('--'):
        stage_id = args[0]

    summary = parsed_args.get('summary', '')

    project_root = Path.cwd()
    fs_state = FilesystemState(project_root)
    archive_mgr = ArchiveManager(project_root)

    # If no stage ID provided, use current stage
    if not stage_id:
        state = fs_state.get_project_state()
        stage_id = state.get('current_stage', 'unknown')

    # Archive stage
    try:
        archive_path = archive_mgr.archive_stage(stage_id, summary)
    except ValueError as e:
        return format_error(str(e))
    except Exception as e:
        return format_error(f"Archive failed: {str(e)}")

    return (
        f"# ✅ Stage Archived Successfully\n\n"
        f"**Stage**: {stage_id}\n"
        f"**Archive Path**: {archive_path}\n"
        f"**Summary**: {summary if summary else '(No summary provided)'}\n\n"
        f"The current/ directory has been cleared for the next stage.\n"
    )


def cmd_generate(args: List[str]) -> str:
    """
    Generate artifact from template.

    Command: diverga memory generate ARTIFACT_ID [--force]

    Args:
        args: Command arguments

    Returns:
        Success message with artifact path
    """
    if not args or len(args) == 0:
        return format_error("Missing artifact ID")

    artifact_id = args[0]
    parsed_args = parse_args(args[1:] if len(args) > 1 else [])
    force = parsed_args.get('force', False)

    # Placeholder for artifact generation
    # This would integrate with a template system
    return format_error(
        f"Artifact generation not yet implemented.\n"
        f"Requested: {artifact_id}\n"
        f"Force: {force}"
    )


def cmd_migrate(args: List[str]) -> str:
    """
    Run migration from v6.8 to v7.0.

    Command: diverga memory migrate [--dry-run]

    Args:
        args: Command arguments

    Returns:
        Migration report
    """
    parsed_args = parse_args(args)
    dry_run = parsed_args.get('dry-run', False)

    project_root = Path.cwd()

    # Check for old structure
    old_state_file = project_root / ".diverga" / "state.yaml"
    if not old_state_file.exists():
        return (
            "# ℹ️ No Migration Needed\n\n"
            "No v6.8 project structure detected.\n"
            "This appears to be a fresh v7.0 project or no project at all.\n"
        )

    # Placeholder for migration logic
    if dry_run:
        return (
            f"# 🔍 Migration Dry Run\n\n"
            f"**Old Structure Detected**: {old_state_file}\n"
            f"**Actions That Would Be Taken**:\n"
            f"1. Create .research/ directory\n"
            f"2. Migrate state.yaml → project-state.yaml\n"
            f"3. Create decision-log.yaml from legacy decisions\n"
            f"4. Initialize checkpoints.yaml\n\n"
            f"Run without --dry-run to execute migration.\n"
        )
    else:
        return format_error(
            "Migration not yet implemented.\n"
            "Please manually create v7.0 project structure."
        )


# ============================================================================
# Argument Parsing
# ============================================================================


def parse_args(args_list: List[str]) -> Dict[str, Any]:
    """
    Simple argument parser for CLI commands.

    Supports:
    - Flags: --verbose, --force, --dry-run
    - Key-value: --name "value", --question "value"

    Args:
        args_list: List of argument strings

    Returns:
        Dictionary of parsed arguments
    """
    result = {}
    i = 0

    while i < len(args_list):
        arg = args_list[i]

        # Handle flags (--flag without value)
        if arg.startswith('--'):
            key = arg[2:]  # Remove --

            # Check if next arg is a value or another flag
            if i + 1 < len(args_list) and not args_list[i + 1].startswith('--'):
                # Has value
                value = args_list[i + 1]
                result[key] = value
                i += 2
            else:
                # Boolean flag
                result[key] = True
                i += 1
        else:
            # Positional argument (skip for now)
            i += 1

    return result


# ============================================================================
# Output Formatting
# ============================================================================


def format_output(data: Dict[str, Any], output_format: str = "text") -> str:
    """
    Format output in specified format.

    Args:
        data: Data dictionary to format
        output_format: Format type (text, yaml, json)

    Returns:
        Formatted string
    """
    if output_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif output_format == "yaml":
        if yaml is None:
            return "Error: PyYAML not installed for YAML output"
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)
    else:  # text
        # Simple text representation
        lines = []
        for key, value in data.items():
            lines.append(f"{key}: {value}")
        return '\n'.join(lines)


def format_error(message: str) -> str:
    """
    Format error message with consistent style.

    Args:
        message: Error message text

    Returns:
        Formatted error string
    """
    return f"# ❌ Error\n\n{message}\n"


# ============================================================================
# Main Entry Point (for standalone execution)
# ============================================================================


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [args...]")
        print("\nCommands:")
        print("  status          Show research project status")
        print("  context         Show full research context")
        print("  init            Initialize new research project")
        print("  decision        Add or view decisions")
        print("  archive         Archive current stage")
        print("  generate        Generate artifact")
        print("  migrate         Run migration")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    result = run_cli(command, args)
    print(result)


if __name__ == "__main__":
    main()
