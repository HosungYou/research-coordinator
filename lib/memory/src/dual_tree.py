"""
Dual-Tree Structure Management for Diverga Memory System v7.0

Separates research artifacts into:
- STABLE TREE (baselines/): Verified, stable research foundations
- WORKING TREE (changes/): In-progress work with deltas

This architecture enables:
- Atomic verification of research changes
- Clear separation between stable knowledge and active exploration
- Delta-based tracking of conceptual evolution
"""

from pathlib import Path
from typing import Optional, List
import json
from datetime import datetime


class DualTreeManager:
    """
    Manages dual-tree structure for research artifact versioning.

    Directory Structure:
        .research/
            baselines/
                literature/     # Verified literature reviews
                methodology/    # Stable research methods
                framework/      # Established theoretical frameworks
            changes/
                current/        # Active working files
                archive/        # Previous change sessions
    """

    def __init__(self, project_root: Path):
        """
        Initialize dual-tree manager.

        Args:
            project_root: Root directory of the research project
        """
        self.project_root = Path(project_root)
        self.research_dir = self.project_root / ".research"

        # Stable tree paths
        self.baselines_dir = self.research_dir / "baselines"
        self.baseline_categories = {
            "literature": self.baselines_dir / "literature",
            "methodology": self.baselines_dir / "methodology",
            "framework": self.baselines_dir / "framework"
        }

        # Working tree paths
        self.changes_dir = self.research_dir / "changes"
        self.current_changes_dir = self.changes_dir / "current"
        self.archive_changes_dir = self.changes_dir / "archive"

        # Ensure directory structure exists
        self._initialize_directories()

    def _initialize_directories(self) -> None:
        """Create all required directories if they don't exist."""
        # Create baseline category directories
        for category_dir in self.baseline_categories.values():
            category_dir.mkdir(parents=True, exist_ok=True)

        # Create changes directories
        self.current_changes_dir.mkdir(parents=True, exist_ok=True)
        self.archive_changes_dir.mkdir(parents=True, exist_ok=True)

    def create_baseline(self, category: str, filename: str, content: str) -> Path:
        """
        Create or update a baseline document in the stable tree.

        Args:
            category: Baseline category (literature, methodology, framework)
            filename: Name of the baseline file
            content: Content to write

        Returns:
            Path to the created/updated baseline file

        Raises:
            ValueError: If category is invalid
        """
        if category not in self.baseline_categories:
            raise ValueError(
                f"Invalid category '{category}'. "
                f"Must be one of: {list(self.baseline_categories.keys())}"
            )

        baseline_path = self.baseline_categories[category] / filename
        baseline_path.write_text(content, encoding="utf-8")

        # Add metadata
        self._add_baseline_metadata(baseline_path, category)

        return baseline_path

    def _add_baseline_metadata(self, baseline_path: Path, category: str) -> None:
        """Add metadata file for baseline tracking."""
        metadata_path = baseline_path.with_suffix(baseline_path.suffix + ".meta.json")
        metadata = {
            "category": category,
            "filename": baseline_path.name,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "status": "stable"
        }
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def create_change(self, filename: str, content: str) -> Path:
        """
        Create a new file in the current changes directory.

        Args:
            filename: Name of the change file
            content: Content to write

        Returns:
            Path to the created change file
        """
        change_path = self.current_changes_dir / filename
        change_path.write_text(content, encoding="utf-8")

        # Add change metadata
        self._add_change_metadata(change_path)

        return change_path

    def _add_change_metadata(self, change_path: Path) -> None:
        """Add metadata file for change tracking."""
        metadata_path = change_path.with_suffix(change_path.suffix + ".meta.json")
        metadata = {
            "filename": change_path.name,
            "created_at": datetime.now().isoformat(),
            "status": "in_progress",
            "verified": False
        }
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def apply_delta(self, source_baseline: Path, delta_content: str) -> str:
        """
        Apply delta changes to baseline content.

        This is a simple concatenation approach. For more sophisticated
        delta application (e.g., line-level diffs), extend this method.

        Args:
            source_baseline: Path to the baseline file
            delta_content: Delta content to apply

        Returns:
            Combined content (baseline + delta)

        Raises:
            FileNotFoundError: If source baseline doesn't exist
        """
        if not source_baseline.exists():
            raise FileNotFoundError(f"Baseline not found: {source_baseline}")

        baseline_content = source_baseline.read_text(encoding="utf-8")

        # Simple delta application: append with separator
        combined_content = (
            f"{baseline_content}\n\n"
            f"--- DELTA APPLIED ({datetime.now().isoformat()}) ---\n\n"
            f"{delta_content}"
        )

        return combined_content

    def get_baseline(self, category: str, filename: str) -> Optional[str]:
        """
        Read baseline content.

        Args:
            category: Baseline category
            filename: Name of the baseline file

        Returns:
            File content if exists, None otherwise
        """
        if category not in self.baseline_categories:
            return None

        baseline_path = self.baseline_categories[category] / filename

        if not baseline_path.exists():
            return None

        return baseline_path.read_text(encoding="utf-8")

    def get_current_change(self, filename: str) -> Optional[str]:
        """
        Read current change content.

        Args:
            filename: Name of the change file

        Returns:
            File content if exists, None otherwise
        """
        change_path = self.current_changes_dir / filename

        if not change_path.exists():
            return None

        return change_path.read_text(encoding="utf-8")

    def list_baselines(self, category: str = None) -> List[Path]:
        """
        List all baseline files, optionally filtered by category.

        Args:
            category: Optional category filter

        Returns:
            List of baseline file paths
        """
        baselines = []

        if category:
            if category not in self.baseline_categories:
                return []

            category_dir = self.baseline_categories[category]
            baselines.extend([
                f for f in category_dir.iterdir()
                if f.is_file() and not f.name.endswith(".meta.json")
            ])
        else:
            # List all categories
            for category_dir in self.baseline_categories.values():
                baselines.extend([
                    f for f in category_dir.iterdir()
                    if f.is_file() and not f.name.endswith(".meta.json")
                ])

        return sorted(baselines)

    def list_current_changes(self) -> List[Path]:
        """
        List all files in current changes directory.

        Returns:
            List of change file paths
        """
        if not self.current_changes_dir.exists():
            return []

        changes = [
            f for f in self.current_changes_dir.iterdir()
            if f.is_file() and not f.name.endswith(".meta.json")
        ]

        return sorted(changes)

    def promote_to_baseline(self, change_path: Path, category: str) -> Path:
        """
        Move a verified change file to the baseline tree.

        Args:
            change_path: Path to the change file
            category: Target baseline category

        Returns:
            Path to the new baseline file

        Raises:
            ValueError: If category is invalid or file doesn't exist
        """
        if not change_path.exists():
            raise ValueError(f"Change file not found: {change_path}")

        if category not in self.baseline_categories:
            raise ValueError(
                f"Invalid category '{category}'. "
                f"Must be one of: {list(self.baseline_categories.keys())}"
            )

        # Read change content
        content = change_path.read_text(encoding="utf-8")

        # Create baseline
        baseline_path = self.create_baseline(category, change_path.name, content)

        # Archive the change file
        archive_path = self.archive_changes_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{change_path.name}"
        change_path.rename(archive_path)

        # Move metadata if exists
        metadata_path = change_path.with_suffix(change_path.suffix + ".meta.json")
        if metadata_path.exists():
            archive_metadata_path = archive_path.with_suffix(archive_path.suffix + ".meta.json")
            metadata_path.rename(archive_metadata_path)

        return baseline_path

    def has_unsaved_changes(self) -> bool:
        """
        Check if there are uncommitted files in current changes.

        Returns:
            True if current/ directory has files, False otherwise
        """
        if not self.current_changes_dir.exists():
            return False

        # Check for non-metadata files
        changes = [
            f for f in self.current_changes_dir.iterdir()
            if f.is_file() and not f.name.endswith(".meta.json")
        ]

        return len(changes) > 0

    def get_status_summary(self) -> dict:
        """
        Get summary of dual-tree status.

        Returns:
            Dictionary with baseline and change counts
        """
        baseline_counts = {
            category: len(list(cat_dir.glob("*"))) - len(list(cat_dir.glob("*.meta.json")))
            for category, cat_dir in self.baseline_categories.items()
        }

        current_changes_count = len(self.list_current_changes())

        return {
            "baselines": baseline_counts,
            "total_baselines": sum(baseline_counts.values()),
            "current_changes": current_changes_count,
            "has_unsaved_changes": self.has_unsaved_changes()
        }
