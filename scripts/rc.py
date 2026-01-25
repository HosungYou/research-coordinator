#!/usr/bin/env python3
"""
Research Coordinator CLI (Cross-Platform)
==========================================
Python-based CLI tool for managing Research Coordinator agents.
Works on Windows, macOS, and Linux.

Usage:
    python rc.py help              - Show help message
    python rc.py status            - Show installation status
    python rc.py list              - List all available agents
    python rc.py validate [agent]  - Validate agent contracts
    python rc.py info <agent>      - Show agent details
    python rc.py doctor            - Diagnose installation issues

Author: Research Coordinator v3.1
License: MIT
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

VERSION = "3.1.0"


class Colors:
    """ANSI color codes for terminal output."""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    NC = "\033[0m"  # No color

    @classmethod
    def disable(cls) -> None:
        """Disable colors for non-TTY environments."""
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = cls.CYAN = cls.NC = ""


# Disable colors if not a TTY (e.g., redirected output)
if not sys.stdout.isatty():
    Colors.disable()

# Windows doesn't support ANSI by default in older terminals
if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        Colors.disable()


def print_header() -> None:
    """Print the CLI header banner."""
    print(f"{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════╗")
    print(f"║         Research Coordinator CLI v{VERSION}              ║")
    print("║         사회과학 연구 에이전트 시스템                  ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(f"{Colors.NC}")


def print_success(msg: str) -> None:
    print(f"{Colors.GREEN}✓{Colors.NC} {msg}")


def print_error(msg: str) -> None:
    print(f"{Colors.RED}✗{Colors.NC} {msg}")


def print_warning(msg: str) -> None:
    print(f"{Colors.YELLOW}!{Colors.NC} {msg}")


def print_info(msg: str) -> None:
    print(f"{Colors.CYAN}ℹ{Colors.NC} {msg}")


def get_paths() -> dict:
    """Get relevant directory paths."""
    script_dir = Path(__file__).parent.resolve()
    repo_dir = script_dir.parent

    # Cross-platform home directory
    home = Path.home()
    skills_dir = home / ".claude" / "skills"

    return {
        "script_dir": script_dir,
        "repo_dir": repo_dir,
        "skills_dir": skills_dir,
        "agents_dir": repo_dir / ".claude" / "skills" / "research-agents",
        "coordinator_dir": repo_dir / ".claude" / "skills" / "research-coordinator",
    }


def cmd_help() -> None:
    """Show help message."""
    print_header()
    print("Usage: python rc.py <command> [options]")
    print()
    print("Commands:")
    print("  help                    Show this help message")
    print("  status                  Show installation status")
    print("  list                    List all available agents")
    print("  validate [agent]        Validate agent contracts")
    print("  info <agent>            Show agent details")
    print("  doctor                  Diagnose installation issues")
    print()
    print("Examples:")
    print("  python rc.py list       # List all 21 agents")
    print("  python rc.py info 02    # Show info for agent 02")
    print("  python rc.py validate   # Validate all agents")
    print()
    print("Documentation: https://github.com/HosungYou/research-coordinator")


def cmd_status() -> None:
    """Show installation status."""
    print_header()
    print("Installation Status")
    print("───────────────────────────────────────────────────────")

    paths = get_paths()
    skills_dir = paths["skills_dir"]

    # Check coordinator
    coordinator_path = skills_dir / "research-coordinator"
    if coordinator_path.exists():
        print_success("Research Coordinator: Installed")
        skill_file = coordinator_path / "SKILL.md"
        if skill_file.exists():
            try:
                content = skill_file.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    if line.strip().startswith("version:"):
                        version = line.split(":", 1)[1].strip().strip('"')
                        print(f"        Version: {version}")
                        break
            except Exception:
                pass
    else:
        print_error("Research Coordinator: Not installed")
        print("        Run: python scripts/install.py or ./scripts/install.sh")

    # Check agents
    agents_path = skills_dir / "research-agents"
    if agents_path.exists():
        agent_count = len([d for d in agents_path.iterdir() if d.is_dir()])
        print_success(f"Research Agents: {agent_count} agents installed")
    else:
        print_error("Research Agents: Not installed")

    # Check Python
    print_success(f"Python: {sys.version.split()[0]}")

    print()


def cmd_list() -> None:
    """List all available agents."""
    print_header()

    paths = get_paths()
    agents_dir = paths["agents_dir"]

    if not agents_dir.exists():
        print_error(f"Agents directory not found: {agents_dir}")
        return

    # Count agents dynamically
    agent_count = len([d for d in agents_dir.iterdir() if d.is_dir()])
    print(f"Available Agents ({agent_count})")
    print("───────────────────────────────────────────────────────")
    print()

    categories = {
        "A": ("Theory & Research Design", range(1, 5)),
        "B": ("Literature & Evidence", range(5, 9)),
        "C": ("Methodology & Analysis", range(9, 13)),
        "D": ("Quality & Validation", range(13, 17)),
        "E": ("Publication & Communication", range(17, 22)),
    }

    for cat_id, (cat_name, num_range) in categories.items():
        print(f"{Colors.CYAN}Category {cat_id}: {cat_name}{Colors.NC}")

        for agent_dir in sorted(agents_dir.iterdir()):
            if not agent_dir.is_dir():
                continue

            name = agent_dir.name
            try:
                agent_num = int(name.split("-")[0])
            except (ValueError, IndexError):
                continue

            if agent_num not in num_range:
                continue

            skill_file = agent_dir / "SKILL.md"
            level = "UNKNOWN"
            if skill_file.exists():
                try:
                    content = skill_file.read_text(encoding="utf-8")
                    for line in content.split("\n"):
                        if line.strip().startswith("upgrade_level:"):
                            level = line.split(":", 1)[1].strip()
                            break
                except Exception:
                    pass

            print(f"  {name:<40} [{level}]")

        print()

    print("───────────────────────────────────────────────────────")
    print("Legend: [FULL] Full VS | [ENHANCED] Enhanced VS | [LIGHT] Light VS")


def cmd_validate(agent_id: Optional[str] = None) -> int:
    """Validate agent contracts."""
    print_header()

    paths = get_paths()
    validator_script = paths["script_dir"] / "validate_agents.py"

    if not validator_script.exists():
        print_error(f"Validation script not found: {validator_script}")
        return 1

    cmd = [sys.executable, str(validator_script), "--verbose"]
    if agent_id:
        cmd.extend(["--agent", agent_id])

    result = subprocess.run(cmd, cwd=paths["repo_dir"])
    return result.returncode


def cmd_info(agent_id: str) -> None:
    """Show agent details."""
    if not agent_id:
        print_error("Usage: python rc.py info <agent_id>")
        print("Example: python rc.py info 02")
        return

    print_header()

    paths = get_paths()
    agents_dir = paths["agents_dir"]

    # Find agent directory
    agent_dir = None
    for d in agents_dir.iterdir():
        if d.is_dir() and agent_id in d.name:
            agent_dir = d
            break

    if not agent_dir:
        print_error(f"Agent not found: {agent_id}")
        print("Use 'python rc.py list' to see available agents")
        return

    skill_file = agent_dir / "SKILL.md"
    name = agent_dir.name

    print(f"Agent Information: {name}")
    print("───────────────────────────────────────────────────────")

    if skill_file.exists():
        try:
            content = skill_file.read_text(encoding="utf-8")

            # Parse basic info from frontmatter
            version = "unknown"
            level = "unknown"
            dynamic_ts = "unknown"

            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("version:"):
                    version = stripped.split(":", 1)[1].strip().strip('"')
                elif stripped.startswith("upgrade_level:"):
                    level = stripped.split(":", 1)[1].strip()
                elif stripped.startswith("dynamic_t_score:"):
                    dynamic_ts = stripped.split(":", 1)[1].strip()

            print()
            print(f"{Colors.CYAN}Basic Info{Colors.NC}")
            print(f"  Name:            {name}")
            print(f"  Version:         {version}")
            print(f"  Upgrade Level:   {level}")
            print(f"  Dynamic T-Score: {dynamic_ts}")
            print()

            # Extract first section content
            print(f"{Colors.CYAN}Description{Colors.NC}")
            in_content = False
            line_count = 0
            for line in content.split("\n"):
                if line.startswith("---") and in_content:
                    in_content = False
                    continue
                if line.startswith("---"):
                    in_content = True
                    continue
                if in_content:
                    continue
                if line.startswith("#") and line_count < 5:
                    print(f"  {line}")
                    line_count += 1

            print()
            print("───────────────────────────────────────────────────────")
            print(f"Full documentation: {skill_file}")
        except Exception as e:
            print_error(f"Error reading SKILL.md: {e}")
    else:
        print_error(f"SKILL.md not found: {skill_file}")


def cmd_doctor() -> None:
    """Diagnose installation issues."""
    print_header()
    print("Diagnosing Installation...")
    print("───────────────────────────────────────────────────────")

    paths = get_paths()
    issues = 0

    # Check 1: Skills directory
    print()
    print("Checking skills directory...")
    if paths["skills_dir"].exists():
        print_success(f"Skills directory exists: {paths['skills_dir']}")
    else:
        print_error(f"Skills directory missing: {paths['skills_dir']}")
        print(f"  Fix: Create directory manually")
        issues += 1

    # Check 2: Coordinator
    print()
    print("Checking coordinator installation...")
    coordinator_path = paths["skills_dir"] / "research-coordinator"
    if coordinator_path.exists():
        if coordinator_path.is_symlink():
            target = coordinator_path.resolve()
            if target.exists():
                print_success(f"Coordinator symlink valid: {target}")
            else:
                print_error(f"Coordinator symlink broken: {target}")
                issues += 1
        else:
            print_success("Coordinator directory exists")
    else:
        print_error("Coordinator not installed")
        issues += 1

    # Check 3: Agents
    print()
    print("Checking agents installation...")
    agents_path = paths["skills_dir"] / "research-agents"
    if agents_path.exists():
        agent_count = len([d for d in agents_path.iterdir() if d.is_dir()])
        print_success(f"Agents installed: {agent_count} agents")
    else:
        print_error("Agents not installed")
        issues += 1

    # Check 4: SKILL.md files
    print()
    print("Checking SKILL.md files...")
    missing_skills = 0
    if paths["agents_dir"].exists():
        for agent_dir in paths["agents_dir"].iterdir():
            if agent_dir.is_dir():
                skill_file = agent_dir / "SKILL.md"
                if not skill_file.exists():
                    print_error(f"Missing SKILL.md: {agent_dir}")
                    missing_skills += 1

    if missing_skills == 0:
        print_success("All agents have SKILL.md files")
    else:
        issues += missing_skills

    # Summary
    print()
    print("───────────────────────────────────────────────────────")
    if issues == 0:
        print_success("No issues found! Installation is healthy.")
    else:
        print_error(f"Found {issues} issue(s)")
        print()
        if sys.platform == "win32":
            print("Quick fix: Run 'python scripts\\install.py' to reinstall")
        else:
            print("Quick fix: Run './scripts/install.sh' to reinstall")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Research Coordinator CLI",
        add_help=False
    )
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("args", nargs="*")

    args = parser.parse_args()

    commands = {
        "help": lambda: cmd_help(),
        "--help": lambda: cmd_help(),
        "-h": lambda: cmd_help(),
        "status": lambda: cmd_status(),
        "list": lambda: cmd_list(),
        "ls": lambda: cmd_list(),
        "validate": lambda: cmd_validate(args.args[0] if args.args else None),
        "check": lambda: cmd_validate(args.args[0] if args.args else None),
        "info": lambda: cmd_info(args.args[0] if args.args else ""),
        "show": lambda: cmd_info(args.args[0] if args.args else ""),
        "doctor": lambda: cmd_doctor(),
        "diagnose": lambda: cmd_doctor(),
        "version": lambda: print(f"Research Coordinator CLI v{VERSION}"),
        "--version": lambda: print(f"Research Coordinator CLI v{VERSION}"),
        "-v": lambda: print(f"Research Coordinator CLI v{VERSION}"),
    }

    if args.command in commands:
        result = commands[args.command]()
        return result if isinstance(result, int) else 0
    else:
        print_error(f"Unknown command: {args.command}")
        print("Run 'python rc.py help' for usage")
        return 1


if __name__ == "__main__":
    sys.exit(main())
