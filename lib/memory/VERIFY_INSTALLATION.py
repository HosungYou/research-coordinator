#!/usr/bin/env python3
"""Verification script for Layer 2 Task Interceptor installation."""

import sys
from pathlib import Path

print("=" * 70)
print("DIVERGA MEMORY SYSTEM v7.0 - LAYER 2 TASK INTERCEPTOR")
print("Installation Verification")
print("=" * 70)
print()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

success_count = 0
fail_count = 0

def test(name, func):
    """Run a test and track results."""
    global success_count, fail_count
    try:
        func()
        print(f"✓ {name}")
        success_count += 1
        return True
    except Exception as e:
        print(f"✗ {name}: {e}")
        fail_count += 1
        return False


# Test 1: Import main module
def test_import_main():
    from task_interceptor import (
        extract_agent_id,
        detect_project_root,
        intercept_task_call,
        load_full_research_context,
        detect_current_stage,
    )

test("Import main module", test_import_main)


# Test 2: Import models
def test_import_models():
    from task_interceptor_models import (
        ResearchContext,
        ProjectState,
        Decision,
        CheckpointState,
    )

test("Import models", test_import_models)


# Test 3: Import from package (optional - only works if installed as package)
def test_import_package():
    try:
        import memory.src as memory
        assert hasattr(memory, 'intercept_task_call')
        assert hasattr(memory, 'extract_agent_id')
    except ModuleNotFoundError:
        # This is OK - package import only works when installed
        pass

test("Import from package (optional)", test_import_package)


# Test 4: Test extract_agent_id
def test_extract_agent():
    from task_interceptor import extract_agent_id
    assert extract_agent_id("diverga:a1") == "a1"
    assert extract_agent_id("diverga:c5-metaanalyst") == "c5-metaanalyst"
    assert extract_agent_id("oh-my-claudecode:executor") is None

test("Test extract_agent_id()", test_extract_agent)


# Test 5: Test detect_project_root
def test_detect_root():
    from task_interceptor import detect_project_root
    result = detect_project_root()
    # Just check it runs without error
    assert result is None or isinstance(result, Path)

test("Test detect_project_root()", test_detect_root)


# Test 6: Test intercept_task_call with non-diverga agent
def test_intercept_non_diverga():
    from task_interceptor import intercept_task_call
    original = "Fix the bug"
    result = intercept_task_call("oh-my-claudecode:executor", original)
    assert result == original

test("Test intercept_task_call() non-diverga", test_intercept_non_diverga)


# Test 7: Test ResearchContext model
def test_research_context():
    from task_interceptor_models import ResearchContext, ProjectState, Decision, CheckpointState

    project_state = ProjectState(
        project_id="test",
        stage="foundation",
        created_at="2024-01-01T00:00:00Z",
        last_updated="2024-02-03T00:00:00Z"
    )

    decision = Decision(
        timestamp="2024-01-10T00:00:00Z",
        agent_id="a1",
        decision="Test decision",
        rationale="Test",
        impact="Test"
    )

    checkpoint = CheckpointState(
        id="CP_TEST",
        status="pending"
    )

    context = ResearchContext(
        project_state=project_state,
        recent_decisions=[decision],
        checkpoints={"CP_TEST": checkpoint},
        current_stage="foundation"
    )

    prompt_section = context.to_prompt_section()
    assert "test" in prompt_section
    assert "CP_TEST" in prompt_section

test("Test ResearchContext model", test_research_context)


# Test 8: Check file structure
def test_file_structure():
    base = Path(__file__).parent
    required_files = [
        "src/__init__.py",
        "src/task_interceptor.py",
        "src/task_interceptor_models.py",
        "tests/__init__.py",
        "tests/test_task_interceptor.py",
        "examples/__init__.py",
        "examples/basic_usage.py",
        "requirements.txt",
        "README.md",
    ]

    for file in required_files:
        assert (base / file).exists(), f"Missing: {file}"

test("Check file structure", test_file_structure)


# Test 9: Check dependencies
def test_dependencies():
    import yaml  # Should be installed

test("Check dependencies (yaml)", test_dependencies)


# Summary
print()
print("=" * 70)
print(f"Tests: {success_count} passed, {fail_count} failed")

if fail_count == 0:
    print("✓ ALL TESTS PASSED - Installation verified successfully!")
    print()
    print("Next steps:")
    print("1. Run examples: python3 examples/basic_usage.py")
    print("2. Read docs: cat README.md")
    print("3. Run tests: python3 -m pytest tests/ -v")
else:
    print("✗ SOME TESTS FAILED - Check errors above")
    sys.exit(1)

print("=" * 70)
