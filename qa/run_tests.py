#!/usr/bin/env python3
"""
Diverga QA Test Runner
=======================

Main entry point for running Diverga QA tests.
Executes test scenarios and generates comprehensive reports.

Usage:
    python -m qa.run_tests --scenario META-001 --verbose
    python -m qa.run_tests --all --report json
    python -m qa.run_tests --checkpoint CP_RESEARCH_DIRECTION
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from qa.protocol.scenarios import Scenario, list_scenarios, load_scenario
from qa.protocol.metrics import TestResult, GradeLevel
from qa.runners.conversation_simulator import ConversationSimulator
from qa.runners.checkpoint_validator import CheckpointValidator
from qa.runners.agent_tracker import AgentTracker


def print_header(text: str, char: str = "="):
    """Print formatted header."""
    print(f"\n{char * 60}")
    print(f"  {text}")
    print(f"{char * 60}\n")


def print_result_summary(result: TestResult, verbose: bool = False):
    """Print test result summary."""
    grade = result.get_grade()
    grade_colors = {
        GradeLevel.A_EXCELLENT: "\033[92m",  # Green
        GradeLevel.B_GOOD: "\033[94m",       # Blue
        GradeLevel.C_ACCEPTABLE: "\033[93m", # Yellow
        GradeLevel.D_POOR: "\033[91m",       # Red
        GradeLevel.F_FAIL: "\033[91m",       # Red
    }
    reset = "\033[0m"
    color = grade_colors.get(grade, "")

    print(f"Scenario: {result.scenario_id}")
    print(f"Timestamp: {result.timestamp.isoformat()}")
    print(f"Overall Grade: {color}{grade.value}{reset}")
    print(f"Overall Score: {result.compute_overall_score():.1f}%")
    print(f"Status: {'PASS' if result.is_passing() else 'FAIL'}")

    print("\nMetrics:")
    print(f"  Checkpoint Compliance: {result.compute_checkpoint_compliance():.1f}%")
    print(f"  Agent Accuracy: {result.compute_agent_accuracy():.1f}%")
    print(f"  VS Quality: {result.vs_quality.compute_score():.1f}%")

    if result.issues:
        print(f"\nIssues ({len(result.issues)}):")
        for issue in result.issues:
            print(f"  ❌ {issue}")

    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  ⚠️ {warning}")

    if verbose:
        print("\nCheckpoint Details:")
        for cp in result.checkpoint_results:
            status = "✅" if cp.is_passing() else "❌"
            print(f"  {status} {cp.checkpoint_id}: {cp.compute_score():.0f}%")
            if not cp.halt_verified:
                print(f"      - HALT not verified")
            if not cp.vs_options_presented:
                print(f"      - VS alternatives not presented")

        print("\nAgent Details:")
        for agent in result.agent_results:
            status = "✅" if agent.invoked else "❌"
            tier_status = "✅" if agent.correct_model_tier else "⚠️"
            print(f"  {status} {agent.agent_id}: {agent.compute_score():.0f}%")
            print(f"      - Tier: {tier_status} {agent.model_tier}")


def run_manual_simulation(
    scenario: Scenario,
    verbose: bool = False,
) -> TestResult:
    """
    Run manual simulation for a scenario.

    In manual mode, we don't have actual AI responses,
    so we simulate expected behavior for testing the framework.
    """
    print(f"Running manual simulation for: {scenario.name}")
    print(f"Paradigm: {scenario.paradigm.value}")
    print(f"Priority: {scenario.priority.value}")

    simulator = ConversationSimulator(scenario)

    # For manual simulation, we create mock responses
    for turn in scenario.conversation_flow:
        print(f"\n--- Turn {turn.turn_number} ---")
        print(f"User: {turn.user_input[:100]}...")

        # Generate mock AI response based on expected behavior
        mock_response = generate_mock_response(turn)

        if verbose:
            print(f"Mock Response: {mock_response[:200]}...")

        result = simulator.run_turn(turn.user_input, mock_response)

        print(f"Result: {'PASS' if result.passed else 'FAIL'}")
        if result.checkpoint_result:
            print(f"Checkpoint: {result.checkpoint_result.checkpoint_id}")
            print(f"  - Halt: {'✅' if result.checkpoint_result.halt_verified else '❌'}")
            print(f"  - Wait: {'✅' if result.checkpoint_result.wait_behavior_detected else '❌'}")
            print(f"  - Options: {result.checkpoint_result.alternatives_count}")

        if result.issues:
            for issue in result.issues:
                print(f"  ❌ {issue}")

    return simulator.finalize()


def generate_mock_response(turn) -> str:
    """Generate mock AI response for testing."""
    expected = turn.expected_behaviors
    elements = turn.expected_response_elements

    response_parts = []

    # Add checkpoint trigger text
    if expected.checkpoint_trigger:
        if expected.checkpoint_trigger == "CP_RESEARCH_DIRECTION":
            response_parts.append("연구 방향에 대해 몇 가지 옵션을 제시합니다:")
        elif expected.checkpoint_trigger == "CP_METHODOLOGY_APPROVAL":
            response_parts.append("연구 방법론 설계를 검토해 주세요:")
        elif expected.checkpoint_trigger == "CP_PARADIGM_SELECTION":
            response_parts.append("연구 패러다임을 선택해 주세요:")

    # Add VS alternatives
    if elements.vs_alternatives:
        for i, opt in enumerate(elements.vs_alternatives):
            letter = chr(65 + i)  # A, B, C...
            t_score = opt.t_score or 0.5
            recommended = " ⭐" if opt.recommended else ""
            response_parts.append(f"[{letter}] {opt.label} (T={t_score:.2f}){recommended}")
            response_parts.append(f"    {opt.description}")

    # Add wait behavior
    if elements.explicit_wait:
        response_parts.append("")
        response_parts.append("어떤 방향으로 진행하시겠습니까?")

    # Add design summary if required
    if elements.design_summary:
        response_parts.insert(0, "설계 요약:")
        response_parts.insert(1, "- 연구 유형: 메타분석")
        response_parts.insert(2, "- 접근 방식: 하위요인 분석")
        response_parts.insert(3, "")

    return "\n".join(response_parts)


def run_scenario(
    scenario_id: str,
    verbose: bool = False,
    output_format: str = "text",
    output_dir: Path | None = None,
) -> TestResult:
    """Run a single test scenario."""
    try:
        scenario = load_scenario(scenario_id)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print_header(f"Testing Scenario: {scenario_id}")

    result = run_manual_simulation(scenario, verbose)

    print_header("Results", "-")
    print_result_summary(result, verbose)

    # Save report if output directory specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{scenario_id}_{timestamp}"

        if output_format == "json":
            result.to_json(output_dir / f"{filename}.json")
            print(f"\nReport saved: {output_dir / filename}.json")
        else:
            result.to_yaml(output_dir / f"{filename}.yaml")
            print(f"\nReport saved: {output_dir / filename}.yaml")

    return result


def run_all_scenarios(
    verbose: bool = False,
    output_format: str = "text",
    output_dir: Path | None = None,
) -> list[TestResult]:
    """Run all available test scenarios."""
    scenarios = list_scenarios()

    if not scenarios:
        print("No test scenarios found.")
        return []

    print_header(f"Running {len(scenarios)} Test Scenarios")

    results = []
    for scenario_id, name, priority in scenarios:
        print(f"\n{'=' * 40}")
        print(f"Scenario: {scenario_id} ({priority.value})")
        print(f"{'=' * 40}")

        result = run_scenario(
            scenario_id,
            verbose=verbose,
            output_format=output_format,
            output_dir=output_dir,
        )
        results.append(result)

    # Print summary
    print_header("Test Summary")
    passed = sum(1 for r in results if r.is_passing())
    failed = len(results) - passed

    print(f"Total: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass Rate: {passed / len(results) * 100:.1f}%")

    if failed > 0:
        print("\nFailed Scenarios:")
        for r in results:
            if not r.is_passing():
                print(f"  ❌ {r.scenario_id}")

    return results


def test_checkpoint_only(
    checkpoint_id: str,
    verbose: bool = False,
):
    """Test a specific checkpoint in isolation."""
    print_header(f"Testing Checkpoint: {checkpoint_id}")

    validator = CheckpointValidator()

    # Test with sample responses
    test_cases = [
        {
            "name": "Proper halt with options",
            "response": """
연구 방향에 대해 몇 가지 옵션을 제시합니다:

[A] 전체 효과 분석 (T=0.65) - 일반적 접근
[B] 하위요인별 효과 (T=0.40) - 차별화된 접근 ⭐
[C] 개인차 조절효과 (T=0.25) - 혁신적 접근

어떤 방향으로 진행하시겠습니까?
            """,
            "expected_pass": True,
        },
        {
            "name": "Auto-proceed violation",
            "response": """
연구 방향을 분석했습니다. 하위요인별 효과 분석으로 진행하겠습니다.

다음 단계로 이론적 프레임워크를 선택합니다.
            """,
            "expected_pass": False,
        },
        {
            "name": "Missing T-Scores",
            "response": """
연구 방향에 대해 몇 가지 옵션을 제시합니다:

[A] 전체 효과 분석
[B] 하위요인별 효과
[C] 개인차 조절효과

어떤 방향으로 진행하시겠습니까?
            """,
            "expected_pass": True,  # Still passes but with warning
        },
    ]

    for test in test_cases:
        print(f"\n--- Test: {test['name']} ---")
        result = validator.validate(
            test["response"],
            checkpoint_id,
            "REQUIRED",
        )

        actual_pass = result.is_valid
        expected_pass = test["expected_pass"]

        status = "✅ PASS" if actual_pass == expected_pass else "❌ FAIL"
        print(f"Status: {status}")
        print(f"Score: {result.compute_score():.0f}%")

        if verbose:
            print(f"Halt Verified: {result.halt_verified}")
            print(f"Wait Detected: {result.wait_behavior_detected}")
            print(f"Options Count: {result.alternatives_count}")
            print(f"T-Scores Visible: {result.t_scores_visible}")

        if result.issues:
            print("Issues:")
            for issue in result.issues:
                print(f"  - {issue}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Diverga QA Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--scenario",
        "-s",
        help="Run specific scenario by ID (e.g., META-001)",
    )

    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Run all available scenarios",
    )

    parser.add_argument(
        "--checkpoint",
        "-c",
        help="Test specific checkpoint in isolation (e.g., CP_RESEARCH_DIRECTION)",
    )

    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all available scenarios",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
    )

    parser.add_argument(
        "--report",
        "-r",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format for reports (default: yaml)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        help="Directory for saving reports",
    )

    args = parser.parse_args()

    # Set default output directory
    if args.output_dir is None:
        args.output_dir = Path(__file__).parent / "reports"

    if args.list:
        scenarios = list_scenarios()
        print_header("Available Test Scenarios")
        for scenario_id, name, priority in scenarios:
            print(f"  {scenario_id}: {name} ({priority.value})")
        return

    if args.checkpoint:
        test_checkpoint_only(args.checkpoint, args.verbose)
        return

    if args.scenario:
        result = run_scenario(
            args.scenario,
            verbose=args.verbose,
            output_format=args.report,
            output_dir=args.output_dir,
        )
        sys.exit(0 if result.is_passing() else 1)

    if args.all:
        results = run_all_scenarios(
            verbose=args.verbose,
            output_format=args.report,
            output_dir=args.output_dir,
        )
        passed = all(r.is_passing() for r in results)
        sys.exit(0 if passed else 1)

    # No arguments - show help
    parser.print_help()


if __name__ == "__main__":
    main()
