#!/usr/bin/env python3
"""
Agent Contract Validator
========================
Validates SKILL.md files against the Research Coordinator agent contract schema.

Usage:
    python validate_agents.py                 # Validate all agents
    python validate_agents.py --agent 01      # Validate specific agent
    python validate_agents.py --verbose       # Show detailed output
    python validate_agents.py --fix           # Attempt to fix common issues

Author: Research Coordinator v3.1
License: MIT
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ValidationResult:
    """Result of validating an agent contract."""

    agent_name: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        status = "PASS" if self.is_valid else "FAIL"
        icon = "\u2705" if self.is_valid else "\u274c"
        return f"{icon} {self.agent_name}: {status}"


class ContractValidator:
    """Validates agent SKILL.md files against the contract schema."""

    REQUIRED_FRONTMATTER = [
        "name",
        "version",
        "description",
        "upgrade_level",
        "v3_integration",
    ]

    UPGRADE_LEVELS = ["FULL", "ENHANCED", "LIGHT"]

    CREATIVITY_MODULES = [
        "forced-analogy",
        "iterative-loop",
        "semantic-distance",
        "temporal-reframing",
        "community-simulation",
    ]

    CHECKPOINT_PATTERN = re.compile(r"^CP[-_][A-Z]+[-_]\d{3}$", re.IGNORECASE)

    def __init__(self, skill_path: Path, verbose: bool = False):
        self.path = skill_path
        self.verbose = verbose
        self.content = ""
        self.frontmatter: dict[str, Any] = {}
        self.result = ValidationResult(agent_name=skill_path.parent.name, is_valid=True)

    def validate(self) -> ValidationResult:
        """Run all validations and return result."""
        try:
            self.content = self.path.read_text(encoding="utf-8")
        except Exception as e:
            self.result.errors.append(f"Failed to read file: {e}")
            self.result.is_valid = False
            return self.result

        self._parse_frontmatter()
        self._validate_frontmatter()
        self._validate_version()
        self._validate_upgrade_level()
        self._validate_v3_integration()
        self._validate_content_sections()

        self.result.is_valid = len(self.result.errors) == 0
        return self.result

    def _parse_frontmatter(self) -> None:
        """Extract YAML frontmatter from markdown."""
        if not self.content.startswith("---"):
            self.result.errors.append("No YAML frontmatter found (must start with ---)")
            return

        try:
            # Find the closing ---
            end_idx = self.content.index("---", 3)
            yaml_content = self.content[3:end_idx].strip()

            # Simple YAML parsing (no external dependency)
            self.frontmatter = self._simple_yaml_parse(yaml_content)

            if self.verbose:
                self.result.info.append(f"Parsed frontmatter: {list(self.frontmatter.keys())}")

        except ValueError:
            self.result.errors.append("Invalid frontmatter: missing closing ---")
        except Exception as e:
            self.result.errors.append(f"Failed to parse frontmatter: {e}")

    def _simple_yaml_parse(self, yaml_str: str) -> dict[str, Any]:
        """Simple YAML parser for frontmatter (no dependencies).

        Handles nested objects, lists, and multiline strings.
        """
        result: dict[str, Any] = {}
        lines = yaml_str.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                i += 1
                continue

            # Get indentation level
            indent = len(line) - len(line.lstrip())

            # Only process top-level keys (indent == 0)
            if indent == 0 and ":" in line:
                key_value = line.split(":", 1)
                key = key_value[0].strip()
                value = key_value[1].strip() if len(key_value) > 1 else ""

                if value.startswith("|"):
                    # Multiline string
                    multiline = []
                    i += 1
                    while i < len(lines):
                        next_line = lines[i]
                        next_indent = len(next_line) - len(next_line.lstrip())
                        if next_line.strip() and next_indent <= indent:
                            break
                        if next_line.strip():
                            multiline.append(next_line.strip())
                        i += 1
                    result[key] = "\n".join(multiline)
                    continue

                elif value.startswith("["):
                    # Inline list
                    result[key] = [v.strip().strip('"').strip("'")
                                   for v in value.strip("[]").split(",") if v.strip()]

                elif value.lower() in ("true", "false"):
                    result[key] = value.lower() == "true"

                elif value.startswith('"') or value.startswith("'"):
                    result[key] = value.strip('"').strip("'")

                elif value:
                    result[key] = value

                else:
                    # Nested object or list - collect nested content
                    nested: dict[str, Any] = {}
                    nested_list: list[str] = []
                    is_list = False
                    i += 1

                    while i < len(lines):
                        next_line = lines[i]
                        next_stripped = next_line.strip()
                        next_indent = len(next_line) - len(next_line.lstrip())

                        # Stop at next top-level key or end
                        if next_stripped and next_indent == 0:
                            break

                        if next_stripped:
                            # List item
                            if next_stripped.startswith("- "):
                                is_list = True
                                nested_list.append(next_stripped[2:].strip())
                            elif ":" in next_stripped:
                                # Nested key-value
                                nk, nv = next_stripped.split(":", 1)
                                nk = nk.strip()
                                nv = nv.strip()

                                if nv.lower() in ("true", "false"):
                                    nested[nk] = nv.lower() == "true"
                                elif nv:
                                    nested[nk] = nv
                                else:
                                    # Nested list under nested key
                                    sub_list: list[str] = []
                                    i += 1
                                    while i < len(lines):
                                        sub_line = lines[i]
                                        sub_stripped = sub_line.strip()
                                        sub_indent = len(sub_line) - len(sub_line.lstrip())
                                        if sub_stripped and sub_indent <= next_indent:
                                            i -= 1
                                            break
                                        if sub_stripped.startswith("- "):
                                            sub_list.append(sub_stripped[2:].strip())
                                        i += 1
                                    nested[nk] = sub_list
                        i += 1

                    if is_list:
                        result[key] = nested_list
                    elif nested:
                        result[key] = nested
                    else:
                        result[key] = {}
                    continue

            i += 1

        return result

    def _validate_frontmatter(self) -> None:
        """Check required frontmatter fields."""
        if not self.frontmatter:
            return  # Error already added in parsing

        for field_name in self.REQUIRED_FRONTMATTER:
            if field_name not in self.frontmatter:
                self.result.errors.append(f"Missing required field: {field_name}")

    def _validate_version(self) -> None:
        """Check version format (semantic versioning)."""
        version = self.frontmatter.get("version", "")
        if version:
            version_str = str(version)
            if not re.match(r"^\d+\.\d+\.\d+$", version_str):
                self.result.warnings.append(
                    f"Version '{version_str}' doesn't follow semantic versioning (X.Y.Z)"
                )
            elif self.verbose:
                self.result.info.append(f"Version: {version_str}")

    def _validate_upgrade_level(self) -> None:
        """Check upgrade level is valid."""
        level = self.frontmatter.get("upgrade_level", "")
        if level and level not in self.UPGRADE_LEVELS:
            self.result.errors.append(
                f"Invalid upgrade_level: '{level}' (must be FULL, ENHANCED, or LIGHT)"
            )
        elif self.verbose and level:
            self.result.info.append(f"Upgrade level: {level}")

    def _validate_v3_integration(self) -> None:
        """Check v3 integration requirements based on upgrade level."""
        v3 = self.frontmatter.get("v3_integration", {})
        level = self.frontmatter.get("upgrade_level", "")

        if not isinstance(v3, dict):
            self.result.warnings.append("v3_integration should be an object")
            return

        # Check based on upgrade level
        if level == "FULL":
            if not v3.get("dynamic_t_score"):
                self.result.errors.append("FULL agents require dynamic_t_score: true")

            modules = v3.get("creativity_modules", [])
            if isinstance(modules, list) and len(modules) < 5:
                self.result.warnings.append(
                    f"FULL agents should have 5 creativity modules, found {len(modules)}"
                )

            checkpoints = v3.get("checkpoints", [])
            if isinstance(checkpoints, list) and len(checkpoints) < 6:
                self.result.warnings.append(
                    f"FULL agents should have 6+ checkpoints, found {len(checkpoints)}"
                )

        elif level == "ENHANCED":
            modules = v3.get("creativity_modules", [])
            if isinstance(modules, list) and len(modules) < 3:
                self.result.warnings.append(
                    f"ENHANCED agents should have 3+ creativity modules, found {len(modules)}"
                )

    def _validate_content_sections(self) -> None:
        """Check for required content sections in the markdown."""
        required_sections = ["##"]  # At least one heading

        if not any(section in self.content for section in required_sections):
            self.result.warnings.append("No markdown headings found")

        # Check for VS-related sections in FULL/ENHANCED agents
        level = self.frontmatter.get("upgrade_level", "")
        if level in ("FULL", "ENHANCED"):
            vs_keywords = ["VS", "T-Score", "Phase", "\ubaa8\ub2ec"]
            if not any(kw in self.content for kw in vs_keywords):
                self.result.warnings.append(
                    f"{level} agents should document VS methodology"
                )


def find_agents(base_path: Path) -> list[Path]:
    """Find all agent SKILL.md files."""
    agents_dir = base_path / ".claude" / "skills" / "research-agents"

    if not agents_dir.exists():
        return []

    skill_files = []
    for agent_dir in sorted(agents_dir.iterdir()):
        if agent_dir.is_dir():
            skill_path = agent_dir / "SKILL.md"
            if skill_path.exists():
                skill_files.append(skill_path)

    return skill_files


def validate_all(base_path: Path, verbose: bool = False) -> list[ValidationResult]:
    """Validate all agents and return results."""
    results = []
    skill_files = find_agents(base_path)

    if not skill_files:
        print("\u26a0\ufe0f  No agent SKILL.md files found")
        return results

    for skill_path in skill_files:
        validator = ContractValidator(skill_path, verbose=verbose)
        result = validator.validate()
        results.append(result)

    return results


def validate_single(base_path: Path, agent_id: str, verbose: bool = False) -> ValidationResult | None:
    """Validate a single agent by ID (e.g., '01' or '01-research-question-refiner')."""
    agents_dir = base_path / ".claude" / "skills" / "research-agents"

    # Find matching agent directory
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir() and agent_id in agent_dir.name:
            skill_path = agent_dir / "SKILL.md"
            if skill_path.exists():
                validator = ContractValidator(skill_path, verbose=verbose)
                return validator.validate()

    return None


def print_results(results: list[ValidationResult], verbose: bool = False) -> None:
    """Print validation results in a formatted way."""
    if not results:
        return

    print("\n" + "=" * 60)
    print(" Research Coordinator Agent Validation Results")
    print("=" * 60 + "\n")

    passed = sum(1 for r in results if r.is_valid)
    failed = len(results) - passed

    for result in results:
        print(result)

        if verbose or not result.is_valid:
            for error in result.errors:
                print(f"    \u274c ERROR: {error}")
            for warning in result.warnings:
                print(f"    \u26a0\ufe0f  WARNING: {warning}")

        if verbose:
            for info in result.info:
                print(f"    \u2139\ufe0f  {info}")

        if verbose or not result.is_valid:
            print()

    print("-" * 60)
    print(f"Summary: {passed}/{len(results)} agents passed validation")

    if failed > 0:
        print(f"\u274c {failed} agent(s) failed validation")
    else:
        print("\u2705 All agents passed validation!")

    print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Research Coordinator agent contracts"
    )
    parser.add_argument(
        "--agent", "-a",
        help="Validate specific agent by ID (e.g., '01' or 'research-question-refiner')"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed validation output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--path", "-p",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Path to research-coordinator repository"
    )

    args = parser.parse_args()

    # Validate
    if args.agent:
        result = validate_single(args.path, args.agent, verbose=args.verbose)
        if result:
            results = [result]
        else:
            print(f"\u274c Agent not found: {args.agent}")
            return 1
    else:
        results = validate_all(args.path, verbose=args.verbose)

    # Output
    if args.json:
        output = [
            {
                "agent": r.agent_name,
                "valid": r.is_valid,
                "errors": r.errors,
                "warnings": r.warnings,
            }
            for r in results
        ]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print_results(results, verbose=args.verbose)

    # Return code
    return 0 if all(r.is_valid for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
