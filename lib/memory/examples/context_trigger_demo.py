"""
Diverga Memory System v7.0 - Layer 1 Demo

This example demonstrates how the Context Trigger System automatically
detects user questions about research status and displays relevant context.

Usage:
    python3 examples/context_trigger_demo.py
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from context_trigger import should_load_context, load_and_display_context


def demo_keyword_detection():
    """Demonstrate keyword detection in multiple languages."""
    print("=" * 70)
    print("DEMO 1: Keyword Detection")
    print("=" * 70)
    print()

    test_messages = [
        # English
        ("What's my research status?", "English question"),
        ("Where was I in the project?", "English question"),
        ("Tell me about neural networks", "Non-trigger"),

        # Korean
        ("내 연구 진행 상황 알려줘", "Korean question"),
        ("어디까지 했더라?", "Korean question"),
        ("날씨가 좋네요", "Non-trigger"),
    ]

    for message, label in test_messages:
        triggered = should_load_context(message)
        status = "✓ TRIGGERED" if triggered else "✗ NOT TRIGGERED"
        print(f"{status:20} [{label:20}] {message}")

    print()


def demo_context_loading():
    """Demonstrate context loading and display."""
    print("=" * 70)
    print("DEMO 2: Context Loading")
    print("=" * 70)
    print()

    # Example 1: No project exists
    print("Example 1: Directory with no .research/ folder")
    print("-" * 70)
    non_existent = Path("/tmp/no_project_here")
    context = load_and_display_context(non_existent)
    print(context[:300] + "..." if len(context) > 300 else context)
    print()

    # Example 2: Real project (Diverga root)
    print("Example 2: Diverga project directory")
    print("-" * 70)
    diverga_root = Path("/Volumes/External SSD/Projects/Research/Diverga")

    # Only show if .research exists
    if (diverga_root / ".research").exists():
        context = load_and_display_context(diverga_root)
        print(context)
    else:
        print("No .research/ directory found in Diverga root.")
        print("(This is expected - sample data was created for testing)")

    print()


def demo_conversation_flow():
    """Demonstrate typical conversation flow."""
    print("=" * 70)
    print("DEMO 3: Typical Conversation Flow")
    print("=" * 70)
    print()

    conversation = [
        ("User", "Hello Claude!"),
        ("Claude", "Hello! How can I help you today?"),
        ("User", "내 연구 진행 상황 알려줘"),  # "Tell me my research status"
        ("System", "→ Keyword detected: '내 연구 진행'"),
        ("System", "→ Loading context from .research/"),
        ("Claude", "[Displays full research context with status, decisions, checkpoints]"),
    ]

    for speaker, message in conversation:
        if speaker == "System":
            print(f"  {message}")
        else:
            print(f"{speaker:10} {message}")

    print()


def demo_multilingual_support():
    """Demonstrate multilingual keyword support."""
    print("=" * 70)
    print("DEMO 4: Multilingual Support")
    print("=" * 70)
    print()

    print("Supported languages: English, Korean")
    print()

    print("English triggers:")
    english_keywords = [
        "my research", "research status", "research progress",
        "where was I", "continue research", "what stage",
    ]
    for keyword in english_keywords[:6]:
        print(f"  - '{keyword}'")

    print()
    print("Korean triggers:")
    korean_keywords = [
        "내 연구", "연구 진행", "연구 상태",
        "어디까지", "지금 단계", "연구 계속",
    ]
    for keyword in korean_keywords:
        print(f"  - '{keyword}'")

    print()


def main():
    """Run all demos."""
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  Diverga Memory System v7.0 - Layer 1: Context Trigger Demo       ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()

    demos = [
        demo_keyword_detection,
        demo_context_loading,
        demo_conversation_flow,
        demo_multilingual_support,
    ]

    for demo in demos:
        try:
            demo()
            input("Press Enter to continue to next demo...\n")
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
        except Exception as e:
            print(f"\n⚠️  Error in demo: {e}\n")
            import traceback
            traceback.print_exc()

    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("  1. Try the interactive demo: python3 examples/interactive_demo.py")
    print("  2. Read the docs: lib/memory/README.md")
    print("  3. Run tests: python3 tests/run_tests.py")
    print()


if __name__ == "__main__":
    main()
