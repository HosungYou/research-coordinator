"""
Simple test runner for context_trigger module (no pytest required)
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from context_trigger import (
    should_load_context,
    load_and_display_context,
    format_recent_decisions,
    format_pending_checkpoints,
    get_next_step_guidance,
    CONTEXT_TRIGGER_KEYWORDS,
)


def test_english_keywords():
    """Test English keyword detection."""
    print("Testing English keywords...")
    test_cases = [
        ("What is my research question?", True),
        ("Show me my research status", True),
        ("Where was I in the project?", True),
        ("Continue my research", True),
        ("Just a random message", False),
    ]

    passed = 0
    for message, expected in test_cases:
        result = should_load_context(message)
        if result == expected:
            passed += 1
            print(f"  ✓ '{message}' -> {result}")
        else:
            print(f"  ✗ '{message}' -> {result} (expected {expected})")

    print(f"  Passed: {passed}/{len(test_cases)}\n")
    return passed == len(test_cases)


def test_korean_keywords():
    """Test Korean keyword detection."""
    print("Testing Korean keywords...")
    test_cases = [
        ("내 연구 진행 상황 알려줘", True),
        ("연구 어디까지 했어?", True),
        ("지금 단계가 뭐야?", True),
        ("안녕하세요", False),
    ]

    passed = 0
    for message, expected in test_cases:
        result = should_load_context(message)
        if result == expected:
            passed += 1
            print(f"  ✓ '{message}' -> {result}")
        else:
            print(f"  ✗ '{message}' -> {result} (expected {expected})")

    print(f"  Passed: {passed}/{len(test_cases)}\n")
    return passed == len(test_cases)


def test_case_insensitive():
    """Test case-insensitive matching."""
    print("Testing case-insensitive English...")
    test_cases = [
        "MY RESEARCH STATUS",
        "What Is My Research Question?",
        "where was i",
    ]

    passed = 0
    for message in test_cases:
        result = should_load_context(message)
        if result:
            passed += 1
            print(f"  ✓ '{message}' -> {result}")
        else:
            print(f"  ✗ '{message}' -> {result} (expected True)")

    print(f"  Passed: {passed}/{len(test_cases)}\n")
    return passed == len(test_cases)


def test_context_loading():
    """Test context loading."""
    print("Testing context loading...")

    # Test with non-existent path
    non_existent = Path("/non/existent/path")
    context = load_and_display_context(non_existent)

    if "No Research Project Found" in context:
        print("  ✓ No project message works")
        result1 = True
    else:
        print("  ✗ No project message failed")
        result1 = False

    # Test with Diverga root (may or may not have .research)
    diverga_root = Path("/Volumes/External SSD/Projects/Research/Diverga")
    context = load_and_display_context(diverga_root)

    if "Your Research Context" in context or "No Research Project Found" in context:
        print("  ✓ Context loading works")
        result2 = True
    else:
        print("  ✗ Context loading failed")
        result2 = False

    print()
    return result1 and result2


def test_formatting():
    """Test formatting functions."""
    print("Testing formatting functions...")

    # Test decisions
    decisions = [
        {
            "timestamp": "2026-02-03T10:30:00Z",
            "type": "Research Question",
            "description": "Approved research question",
            "agent": "A1-research-question-refiner",
        }
    ]
    result = format_recent_decisions(decisions)

    if "Recent Decisions" in result and "Research Question" in result:
        print("  ✓ Decision formatting works")
        result1 = True
    else:
        print("  ✗ Decision formatting failed")
        result1 = False

    # Test checkpoints
    checkpoints = [
        {
            "name": "CP_THEORY_SELECTION",
            "level": "required",
            "description": "Theoretical framework selection",
            "human_action": "Select framework",
        }
    ]
    result = format_pending_checkpoints(checkpoints)

    if "Pending Checkpoints" in result and "🔴" in result:
        print("  ✓ Checkpoint formatting works")
        result2 = True
    else:
        print("  ✗ Checkpoint formatting failed")
        result2 = False

    # Test guidance
    guidance = get_next_step_guidance("foundation")
    if "research question" in guidance.lower():
        print("  ✓ Stage guidance works")
        result3 = True
    else:
        print("  ✗ Stage guidance failed")
        result3 = False

    print()
    return result1 and result2 and result3


def test_keyword_coverage():
    """Test all documented keywords work."""
    print("Testing keyword coverage...")

    # Test all English keywords
    failed_en = []
    for keyword in CONTEXT_TRIGGER_KEYWORDS["english"]:
        message = f"Tell me about {keyword}"
        if not should_load_context(message):
            failed_en.append(keyword)

    if not failed_en:
        print(f"  ✓ All {len(CONTEXT_TRIGGER_KEYWORDS['english'])} English keywords work")
    else:
        print(f"  ✗ Failed English keywords: {failed_en}")

    # Test all Korean keywords
    failed_ko = []
    for keyword in CONTEXT_TRIGGER_KEYWORDS["korean"]:
        message = f"{keyword} 보여줘"
        if not should_load_context(message):
            failed_ko.append(keyword)

    if not failed_ko:
        print(f"  ✓ All {len(CONTEXT_TRIGGER_KEYWORDS['korean'])} Korean keywords work")
    else:
        print(f"  ✗ Failed Korean keywords: {failed_ko}")

    print()
    return len(failed_en) == 0 and len(failed_ko) == 0


def main():
    """Run all tests."""
    print("=" * 70)
    print("Context Trigger System - Test Suite")
    print("=" * 70)
    print()

    results = []
    results.append(("English Keywords", test_english_keywords()))
    results.append(("Korean Keywords", test_korean_keywords()))
    results.append(("Case Insensitive", test_case_insensitive()))
    results.append(("Context Loading", test_context_loading()))
    results.append(("Formatting", test_formatting()))
    results.append(("Keyword Coverage", test_keyword_coverage()))

    print("=" * 70)
    print("Test Summary")
    print("=" * 70)

    total = len(results)
    passed = sum(1 for _, result in results if result)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")

    print()
    print(f"Total: {passed}/{total} test groups passed")
    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
