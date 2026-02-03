"""
Diverga Memory System v7.0 - Filesystem State Management

This module manages research project state through filesystem structure,
providing persistent context across Claude Code sessions.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None  # Graceful fallback if PyYAML not available


class FilesystemState:
    """
    Manages project state through filesystem structure.

    The .research/ directory contains all project state information:
    - baselines/: Reference documents (literature, methodology, framework)
    - changes/: Current and archived changes
    - sessions/: Historical session data
    - project-state.yaml: Main project configuration
    - decision-log.yaml: Human decisions at checkpoints
    - checkpoints.yaml: Checkpoint definitions

    Attributes:
        project_root: Root directory of the research project
        research_dir: Path to .research/ directory
        state_file: Path to project-state.yaml
        decision_file: Path to decision-log.yaml
        checkpoints_file: Path to checkpoints.yaml
    """

    def __init__(self, project_root: Path):
        """
        Initialize filesystem state manager.

        Args:
            project_root: Root directory of the research project
        """
        self.project_root = Path(project_root)
        self.research_dir = self.project_root / ".research"
        self.state_file = self.research_dir / "project-state.yaml"
        self.decision_file = self.research_dir / "decision-log.yaml"
        self.checkpoints_file = self.research_dir / "checkpoints.yaml"

    def initialize_project(
        self, project_name: str, research_question: str, paradigm: str
    ) -> bool:
        """
        Create initial directory structure for a new research project.

        Directory structure:
        .research/
        ├── baselines/
        │   ├── literature/
        │   ├── methodology/
        │   └── framework/
        ├── changes/
        │   ├── current/
        │   └── archive/
        ├── sessions/
        ├── project-state.yaml
        ├── decision-log.yaml
        └── checkpoints.yaml

        Args:
            project_name: Name of the research project
            research_question: Primary research question
            paradigm: Research paradigm (quantitative/qualitative/mixed)

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Create directory structure
            directories = [
                self.research_dir / "baselines" / "literature",
                self.research_dir / "baselines" / "methodology",
                self.research_dir / "baselines" / "framework",
                self.research_dir / "changes" / "current",
                self.research_dir / "changes" / "archive",
                self.research_dir / "sessions",
            ]

            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)

            # Initialize project-state.yaml
            initial_state = {
                "project_name": project_name,
                "research_question": research_question,
                "paradigm": paradigm,
                "current_stage": "foundation",  # Stage A: Foundation
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "sessions": [],
                "recent_decisions": [],
                "pending_checkpoints": [],
            }

            if not save_yaml(self.state_file, initial_state):
                return False

            # Initialize decision-log.yaml
            initial_decisions = {
                "decisions": {},
                "amendments": [],
                "last_updated": datetime.utcnow().isoformat(),
            }

            if not save_yaml(self.decision_file, initial_decisions):
                return False

            # Initialize checkpoints.yaml with empty structure
            initial_checkpoints = {
                "checkpoints": {},
                "completed": [],
                "pending": [],
            }

            if not save_yaml(self.checkpoints_file, initial_checkpoints):
                return False

            return True

        except Exception as e:
            print(f"Error initializing project: {e}")
            return False

    def detect_current_stage(self) -> str:
        """
        Detect current research stage from filesystem indicators.

        Checks .research/changes/current/ for indicator files:
        - foundation_*.md → foundation stage (A)
        - evidence_*.md → evidence stage (B)
        - design_*.md → design stage (C)
        - collection_*.md → collection stage (D)
        - analysis_*.md → analysis stage (E)
        - quality_*.md → quality stage (F)
        - communication_*.md → communication stage (G)

        Returns:
            Stage name: foundation, evidence, design, collection,
                       analysis, quality, communication
            Returns 'foundation' if no indicators found
        """
        changes_dir = self.research_dir / "changes" / "current"

        if not changes_dir.exists():
            return "foundation"

        # Check for stage indicator files
        stage_indicators = {
            "foundation": "foundation_*.md",
            "evidence": "evidence_*.md",
            "design": "design_*.md",
            "collection": "collection_*.md",
            "analysis": "analysis_*.md",
            "quality": "quality_*.md",
            "communication": "communication_*.md",
        }

        for stage, pattern in stage_indicators.items():
            if list(changes_dir.glob(pattern)):
                return stage

        # Fallback: check project-state.yaml
        state = self.get_project_state()
        return state.get("current_stage", "foundation")

    def get_project_state(self) -> Dict[str, Any]:
        """
        Load and return full project state from project-state.yaml.

        Returns:
            Dictionary containing project state, or empty dict if not found
        """
        if not self.state_file.exists():
            return {}

        return load_yaml(self.state_file)

    def update_project_state(self, updates: Dict[str, Any]) -> bool:
        """
        Update project-state.yaml with new values.

        Merges updates into existing state and updates timestamp.

        Args:
            updates: Dictionary of fields to update

        Returns:
            True if update successful, False otherwise
        """
        try:
            current_state = self.get_project_state()

            if not current_state:
                print("Warning: Project state file not found. Cannot update.")
                return False

            # Merge updates
            current_state.update(updates)
            current_state["updated_at"] = datetime.utcnow().isoformat()

            return save_yaml(self.state_file, current_state)

        except Exception as e:
            print(f"Error updating project state: {e}")
            return False

    def get_session_files(self) -> List[Path]:
        """
        List all session files in .research/sessions/.

        Returns:
            List of Path objects for session files, sorted by modification time
        """
        sessions_dir = self.research_dir / "sessions"

        if not sessions_dir.exists():
            return []

        # Get all .yaml and .json files
        session_files = list(sessions_dir.glob("*.yaml")) + list(
            sessions_dir.glob("*.json")
        )

        # Sort by modification time (most recent first)
        session_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        return session_files

    def is_initialized(self) -> bool:
        """
        Check if project has .research/ directory and required files.

        Returns:
            True if project is initialized, False otherwise
        """
        if not self.research_dir.exists():
            return False

        # Check for required files
        required_files = [self.state_file]

        return all(f.exists() for f in required_files)

    def get_baselines(self) -> Dict[str, List[Path]]:
        """
        Get baseline document paths organized by category.

        Returns:
            Dictionary with keys: literature, methodology, framework
            Each value is a list of Path objects
        """
        baselines_dir = self.research_dir / "baselines"

        if not baselines_dir.exists():
            return {"literature": [], "methodology": [], "framework": []}

        result = {}

        for category in ["literature", "methodology", "framework"]:
            category_dir = baselines_dir / category
            if category_dir.exists():
                # Get all files in category directory
                result[category] = list(category_dir.glob("*"))
            else:
                result[category] = []

        return result

    def get_current_changes(self) -> List[Path]:
        """
        List files in .research/changes/current/.

        Returns:
            List of Path objects for current change files
        """
        current_dir = self.research_dir / "changes" / "current"

        if not current_dir.exists():
            return []

        # Get all files (not directories)
        return [f for f in current_dir.iterdir() if f.is_file()]


# Helper Functions


def load_yaml(path: Path) -> Dict[str, Any]:
    """
    Safe YAML loading with error handling.

    Supports both PyYAML (preferred) and simple fallback parser.
    Handles UTF-8 encoding for Korean text.

    Args:
        path: Path to YAML file

    Returns:
        Dictionary with loaded data, or empty dict if error
    """
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            if yaml is None:
                # Fallback: simple JSON-like parsing
                # This is NOT a full YAML parser, just handles basic key-value
                content = f.read()
                # Try parsing as JSON first (YAML is superset of JSON)
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Very simple key-value parser for basic YAML
                    return _parse_simple_yaml(content)
            else:
                return yaml.safe_load(f) or {}

    except Exception as e:
        print(f"Error loading YAML from {path}: {e}")
        return {}


def save_yaml(path: Path, data: Dict[str, Any]) -> bool:
    """
    Save YAML with proper formatting.

    Uses PyYAML if available, falls back to JSON.
    Handles UTF-8 encoding for Korean text.

    Args:
        path: Path to save YAML file
        data: Dictionary to save

    Returns:
        True if save successful, False otherwise
    """
    try:
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            if yaml is None:
                # Fallback: save as JSON with indentation
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                yaml.safe_dump(
                    data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

        return True

    except Exception as e:
        print(f"Error saving YAML to {path}: {e}")
        return False


def _parse_simple_yaml(content: str) -> Dict[str, Any]:
    """
    Very simple YAML parser for basic key-value structures.

    This is a fallback when PyYAML is not available.
    Only handles simple dictionaries, lists, and scalar values.

    Args:
        content: YAML content as string

    Returns:
        Parsed dictionary
    """
    result = {}
    current_key = None
    current_list = None

    for line in content.split("\n"):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        # Handle key-value pairs
        if ":" in stripped and not stripped.startswith("-"):
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Handle empty values
            if not value:
                current_key = key
                current_list = []
                result[key] = current_list
            else:
                # Try to parse value
                result[key] = _parse_yaml_value(value)
                current_key = None
                current_list = None

        # Handle list items
        elif stripped.startswith("-") and current_list is not None:
            item = stripped[1:].strip()
            current_list.append(_parse_yaml_value(item))

    return result


def _parse_yaml_value(value: str) -> Any:
    """
    Parse a YAML value string to appropriate Python type.

    Args:
        value: Value string to parse

    Returns:
        Parsed value (str, int, float, bool, or None)
    """
    value = value.strip()

    # None/null
    if value in ("null", "None", "~"):
        return None

    # Boolean
    if value in ("true", "True", "yes", "Yes"):
        return True
    if value in ("false", "False", "no", "No"):
        return False

    # Numbers
    try:
        if "." in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        pass

    # String (remove quotes if present)
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    return value
