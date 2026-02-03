"""Basic usage examples for Diverga Memory System v7.0 Task Interceptor."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.src import (
    extract_agent_id,
    detect_project_root,
    intercept_task_call,
    load_full_research_context,
    detect_current_stage,
)


def example_1_extract_agent_id():
    """Example 1: Extract agent ID from subagent_type."""
    print("=" * 60)
    print("Example 1: Extract Agent ID")
    print("=" * 60)

    test_cases = [
        "diverga:a1",
        "diverga:c5-metaanalyst",
        "diverga:g6",
        "oh-my-claudecode:executor",
        "general-purpose",
    ]

    for subagent_type in test_cases:
        agent_id = extract_agent_id(subagent_type)
        status = "✓ Diverga agent" if agent_id else "✗ Not a Diverga agent"
        print(f"{subagent_type:30} → {agent_id or 'None':20} [{status}]")

    print()


def example_2_detect_project_root():
    """Example 2: Detect project root containing .research/."""
    print("=" * 60)
    print("Example 2: Detect Project Root")
    print("=" * 60)

    # Try to find project root from current directory
    project_root = detect_project_root()

    if project_root:
        print(f"✓ Project found at: {project_root}")
        print(f"  .research/ directory: {project_root / '.research'}")
    else:
        print("✗ No .research/ folder found in directory tree")

    print()


def example_3_detect_stage():
    """Example 3: Detect current research stage."""
    print("=" * 60)
    print("Example 3: Detect Current Stage")
    print("=" * 60)

    project_root = detect_project_root()

    if project_root:
        stage = detect_current_stage(project_root)
        print(f"Current stage: {stage}")

        # Show stage mapping
        stage_descriptions = {
            "foundation": "Theory, literature, research questions",
            "design": "Variables, hypotheses, conceptual framework",
            "methodology": "Sampling, instruments, statistical plan",
            "analysis": "Data analysis, results, effect sizes"
        }
        print(f"Description: {stage_descriptions.get(stage, 'Unknown')}")
    else:
        print("✗ No project found (no .research/ folder)")

    print()


def example_4_load_context():
    """Example 4: Load full research context."""
    print("=" * 60)
    print("Example 4: Load Research Context")
    print("=" * 60)

    project_root = detect_project_root()

    if not project_root:
        print("✗ No project found")
        return

    try:
        context = load_full_research_context(project_root)

        print(f"Project ID: {context.project_state.project_id}")
        print(f"Stage: {context.project_state.stage}")
        print(f"Last Updated: {context.project_state.last_updated}")
        print(f"\nRecent Decisions: {len(context.recent_decisions)}")

        if context.recent_decisions:
            print("\nLast Decision:")
            last_dec = context.recent_decisions[-1]
            print(f"  Agent: {last_dec.agent_id}")
            print(f"  Decision: {last_dec.decision}")
            if last_dec.checkpoint_triggered:
                print(f"  Checkpoint: {last_dec.checkpoint_triggered}")

        print(f"\nCheckpoints: {len(context.checkpoints)}")
        pending = [
            cp_id for cp_id, cp in context.checkpoints.items()
            if cp.status in ["pending", "active"]
        ]
        if pending:
            print(f"  Pending: {', '.join(pending)}")

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    print()


def example_5_intercept_task():
    """Example 5: Intercept task call and inject context."""
    print("=" * 60)
    print("Example 5: Intercept Task Call")
    print("=" * 60)

    # Test with non-diverga agent (should return original)
    print("Test 1: Non-Diverga Agent")
    original = "Fix the bug in module.py"
    result = intercept_task_call("oh-my-claudecode:executor", original)
    print(f"Original: {original}")
    print(f"Modified: {result}")
    print(f"Changed: {result != original}")
    print()

    # Test with diverga agent (should inject context if project found)
    print("Test 2: Diverga Agent")
    original = "Analyze the theoretical framework for this research"
    result = intercept_task_call("diverga:a2", original)

    if "DIVERGA MEMORY SYSTEM" in result:
        print("✓ Context injection successful!")
        print(f"\nPrompt length:")
        print(f"  Original: {len(original)} chars")
        print(f"  Modified: {len(result)} chars")
        print(f"  Injected: {len(result) - len(original)} chars")

        # Show first 500 chars of injected context
        print("\nInjected Context (first 500 chars):")
        print("-" * 60)
        print(result[:500])
        print("...")
    else:
        print("⚠ No context injected (no .research/ folder found)")
        print("To test with context, run from a project with .research/ structure")

    print()


def example_6_prompt_section():
    """Example 6: Generate prompt section from context."""
    print("=" * 60)
    print("Example 6: Generate Prompt Section")
    print("=" * 60)

    project_root = detect_project_root()

    if not project_root:
        print("✗ No project found")
        return

    try:
        context = load_full_research_context(project_root)
        prompt_section = context.to_prompt_section()

        print("Generated Prompt Section:")
        print("-" * 60)
        print(prompt_section)
        print("-" * 60)

    except Exception as e:
        print(f"✗ Error: {e}")

    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("DIVERGA MEMORY SYSTEM v7.0 - USAGE EXAMPLES")
    print("=" * 60 + "\n")

    example_1_extract_agent_id()
    example_2_detect_project_root()
    example_3_detect_stage()
    example_4_load_context()
    example_5_intercept_task()
    example_6_prompt_section()

    print("=" * 60)
    print("Examples Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
