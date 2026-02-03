"""
Diverga Memory System v7.0 - Archive Manager

This module manages archiving of completed research stages, providing
historical tracking and the ability to merge completed work into baselines.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import yaml


class ArchiveManager:
    """
    Manage archiving of completed research stages.

    The ArchiveManager handles the lifecycle of research stages by:
    - Archiving completed stages with timestamped snapshots
    - Generating summaries of stage outputs and decisions
    - Validating stage completion before archiving
    - Providing timeline views of project progress
    - Merging archived work into baseline knowledge

    Archives are stored in: .research/changes/archive/{timestamp}-{stage_id}/
    Each archive contains:
    - SUMMARY.md: Stage overview with key decisions and outputs
    - decisions.yaml: Relevant decision entries from this stage
    - All files from .research/changes/current/ at time of archiving
    """

    def __init__(self, project_root: Path):
        """
        Initialize ArchiveManager with project root.

        Args:
            project_root: Path to project root directory
        """
        self.project_root = Path(project_root)
        self.archive_path = self.project_root / ".research" / "changes" / "archive"
        self.current_path = self.project_root / ".research" / "changes" / "current"
        self.decisions_path = self.project_root / ".research" / "decisions.yaml"

        # Create archive directory if it doesn't exist
        self.archive_path.mkdir(parents=True, exist_ok=True)

    def archive_stage(self, stage_id: str, summary: str = None) -> Path:
        """
        Archive the current stage with timestamped directory.

        This creates a permanent snapshot of the current stage's work,
        including all decisions, outputs, and intermediate files.

        Args:
            stage_id: Stage identifier (e.g., 'A', 'B1', 'C2')
            summary: Optional custom summary text

        Returns:
            Path to the created archive directory

        Raises:
            ValueError: If stage validation fails
            FileNotFoundError: If required files are missing
        """
        # Validate stage completion
        is_complete, missing_items = self.validate_stage_completion(stage_id)
        if not is_complete:
            raise ValueError(
                f"Cannot archive incomplete stage {stage_id}. "
                f"Missing: {', '.join(missing_items)}"
            )

        # Create timestamped archive directory
        timestamp = self._get_timestamp()
        archive_dir = self.archive_path / f"{timestamp}-{stage_id}"
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Copy contents from current/ directory
        if self.current_path.exists():
            for item in self.current_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, archive_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, archive_dir / item.name)

        # Copy relevant decision entries
        self._copy_stage_decisions(archive_dir, stage_id)

        # Generate summary
        self.generate_summary(archive_dir, stage_id, custom_summary=summary)

        # Clear current/ directory for next stage
        if self.current_path.exists():
            for item in self.current_path.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)

        return archive_dir

    def generate_summary(
        self,
        archive_dir: Path,
        stage_id: str,
        custom_summary: str = None
    ) -> None:
        """
        Generate SUMMARY.md for the archived stage.

        The summary includes:
        - Stage name and date range
        - Key decisions made
        - Outputs produced
        - Next stage preview

        Args:
            archive_dir: Path to archive directory
            stage_id: Stage identifier
            custom_summary: Optional custom summary text
        """
        # Load stage decisions
        decisions = self._load_stage_decisions(archive_dir)

        # Get stage metadata
        stage_name = self._get_stage_name(stage_id)
        date_str = archive_dir.name.split('-')[0]  # Extract date from directory name

        # Build summary content
        summary_lines = [
            f"# {stage_name} (Stage {stage_id})",
            "",
            f"**Archive Date**: {date_str}",
            "",
            "## Summary",
            "",
        ]

        if custom_summary:
            summary_lines.extend([custom_summary, ""])

        # Add key decisions
        if decisions:
            summary_lines.extend([
                "## Key Decisions",
                "",
            ])
            for decision in decisions:
                checkpoint_id = decision.get('checkpoint_id', 'Unknown')
                selected = decision.get('selected', 'N/A')
                rationale = decision.get('rationale', 'No rationale provided')

                summary_lines.extend([
                    f"### {checkpoint_id}",
                    f"- **Selected**: {selected}",
                    f"- **Rationale**: {rationale}",
                    "",
                ])

        # Add outputs produced
        outputs = self._list_archive_outputs(archive_dir)
        if outputs:
            summary_lines.extend([
                "## Outputs Produced",
                "",
            ])
            for output in outputs:
                summary_lines.append(f"- {output}")
            summary_lines.append("")

        # Add next stage preview
        next_stage = self._get_next_stage(stage_id)
        if next_stage:
            summary_lines.extend([
                "## Next Stage",
                "",
                f"Proceeding to Stage {next_stage}: {self._get_stage_name(next_stage)}",
                "",
            ])

        # Write summary file
        summary_path = archive_dir / "SUMMARY.md"
        summary_path.write_text('\n'.join(summary_lines), encoding='utf-8')

    def list_archives(self) -> List[Path]:
        """
        List all archived stages chronologically.

        Returns:
            List of archive directory paths, sorted by timestamp (oldest first)
        """
        if not self.archive_path.exists():
            return []

        archives = [
            d for d in self.archive_path.iterdir()
            if d.is_dir() and '-' in d.name
        ]

        # Sort by timestamp in directory name
        archives.sort(key=lambda d: d.name.split('-')[0])

        return archives

    def get_archive(self, archive_name: str) -> Optional[Dict[str, Any]]:
        """
        Get archive contents by name or stage ID.

        Args:
            archive_name: Archive directory name or stage ID

        Returns:
            Dictionary with summary, decisions, and file list, or None if not found
        """
        # Find archive directory
        archive_dir = None
        if (self.archive_path / archive_name).exists():
            archive_dir = self.archive_path / archive_name
        else:
            # Search by stage ID
            for archive in self.list_archives():
                if archive.name.endswith(f"-{archive_name}"):
                    archive_dir = archive
                    break

        if not archive_dir:
            return None

        # Load summary
        summary_path = archive_dir / "SUMMARY.md"
        summary = summary_path.read_text(encoding='utf-8') if summary_path.exists() else ""

        # Load decisions
        decisions_path = archive_dir / "decisions.yaml"
        decisions = []
        if decisions_path.exists():
            with open(decisions_path, 'r', encoding='utf-8') as f:
                decisions = yaml.safe_load(f) or []

        # List files
        files = [
            str(f.relative_to(archive_dir))
            for f in archive_dir.rglob('*')
            if f.is_file()
        ]

        return {
            'archive_name': archive_dir.name,
            'summary': summary,
            'decisions': decisions,
            'files': files,
            'path': str(archive_dir),
        }

    def merge_to_baselines(self, archive_path: Path, baseline_category: str) -> bool:
        """
        Merge archived work into baseline knowledge.

        This allows completed stages to contribute to the project's
        persistent baseline knowledge (e.g., approved methods, validated instruments).

        Args:
            archive_path: Path to archive directory
            baseline_category: Category in baselines (e.g., 'methods', 'instruments')

        Returns:
            True if merge succeeded, False otherwise
        """
        baselines_dir = self.project_root / ".research" / "baselines" / baseline_category
        baselines_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Copy relevant files to baselines
            for item in archive_path.iterdir():
                if item.is_file() and item.name != "SUMMARY.md":
                    target = baselines_dir / item.name

                    # Don't overwrite existing baseline files
                    if not target.exists():
                        shutil.copy2(item, target)

            return True
        except Exception:
            return False

    def validate_stage_completion(self, stage_id: str) -> Tuple[bool, List[str]]:
        """
        Validate that a stage is complete and ready for archiving.

        Checks:
        - Required artifacts exist in current/ directory
        - Required checkpoints have been passed

        Args:
            stage_id: Stage identifier

        Returns:
            Tuple of (is_complete, list_of_missing_items)
        """
        missing_items = []

        # Load project state to check checkpoints
        state_path = self.project_root / ".research" / "project-state.yaml"
        if state_path.exists():
            with open(state_path, 'r', encoding='utf-8') as f:
                state = yaml.safe_load(f) or {}

            # Check if current stage matches
            if state.get('current_stage') != stage_id:
                missing_items.append(f"Current stage is {state.get('current_stage')}, not {stage_id}")
        else:
            missing_items.append("project-state.yaml not found")

        # Check for required artifacts based on stage
        required_artifacts = self._get_required_artifacts(stage_id)
        for artifact in required_artifacts:
            artifact_path = self.current_path / artifact
            if not artifact_path.exists():
                missing_items.append(f"Required artifact: {artifact}")

        is_complete = len(missing_items) == 0
        return is_complete, missing_items

    def get_stage_timeline(self) -> List[Dict[str, Any]]:
        """
        Get chronological timeline of all archived stages.

        Returns:
            List of stage timeline entries with metadata
        """
        timeline = []

        for archive_dir in self.list_archives():
            timestamp_str, stage_id = archive_dir.name.split('-', 1)

            # Load summary
            summary_path = archive_dir / "SUMMARY.md"
            summary = ""
            if summary_path.exists():
                summary = summary_path.read_text(encoding='utf-8')

            # Load decisions count
            decisions_path = archive_dir / "decisions.yaml"
            decision_count = 0
            if decisions_path.exists():
                with open(decisions_path, 'r', encoding='utf-8') as f:
                    decisions = yaml.safe_load(f) or []
                    decision_count = len(decisions)

            timeline.append({
                'date': timestamp_str,
                'stage_id': stage_id,
                'stage_name': self._get_stage_name(stage_id),
                'archive_path': str(archive_dir),
                'decision_count': decision_count,
                'summary_preview': summary.split('\n')[0] if summary else "",
            })

        return timeline

    # Helper methods

    def _get_timestamp(self) -> str:
        """
        Get ISO format timestamp for directory names.

        Returns:
            Timestamp string in YYYY-MM-DD format
        """
        return datetime.now().strftime("%Y-%m-%d")

    def _copy_stage_decisions(self, archive_dir: Path, stage_id: str) -> None:
        """
        Copy decisions relevant to this stage to the archive.

        Args:
            archive_dir: Archive directory path
            stage_id: Stage identifier
        """
        if not self.decisions_path.exists():
            return

        with open(self.decisions_path, 'r', encoding='utf-8') as f:
            all_decisions = yaml.safe_load(f) or {}

        # Filter decisions for this stage
        stage_decisions = []
        for decision in all_decisions.get('decisions', []):
            if decision.get('stage') == stage_id:
                stage_decisions.append(decision)

        # Write to archive
        if stage_decisions:
            archive_decisions_path = archive_dir / "decisions.yaml"
            with open(archive_decisions_path, 'w', encoding='utf-8') as f:
                yaml.dump({'decisions': stage_decisions}, f, allow_unicode=True)

    def _load_stage_decisions(self, archive_dir: Path) -> List[Dict[str, Any]]:
        """
        Load decisions from archived stage.

        Args:
            archive_dir: Archive directory path

        Returns:
            List of decision dictionaries
        """
        decisions_path = archive_dir / "decisions.yaml"
        if not decisions_path.exists():
            return []

        with open(decisions_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
            return data.get('decisions', [])

    def _get_stage_name(self, stage_id: str) -> str:
        """
        Get human-readable stage name.

        Args:
            stage_id: Stage identifier

        Returns:
            Stage name
        """
        stage_names = {
            'A': 'Research Foundation',
            'B': 'Evidence & Literature',
            'C': 'Research Design',
            'D': 'Data Collection',
            'E': 'Analysis',
            'F': 'Quality Assurance',
            'G': 'Communication & Publication',
            'H': 'Specialized Methods',
        }

        # Handle substages (e.g., 'B1', 'C2')
        main_stage = stage_id[0] if stage_id else 'Unknown'
        base_name = stage_names.get(main_stage, f'Stage {main_stage}')

        if len(stage_id) > 1:
            return f"{base_name} - Substage {stage_id[1:]}"
        return base_name

    def _list_archive_outputs(self, archive_dir: Path) -> List[str]:
        """
        List output files in archive.

        Args:
            archive_dir: Archive directory path

        Returns:
            List of output file names (excluding SUMMARY.md and decisions.yaml)
        """
        outputs = []

        for item in archive_dir.iterdir():
            if item.is_file() and item.name not in ['SUMMARY.md', 'decisions.yaml']:
                outputs.append(item.name)
            elif item.is_dir():
                outputs.append(f"{item.name}/ (directory)")

        return outputs

    def _get_next_stage(self, stage_id: str) -> Optional[str]:
        """
        Get the next stage in the research pipeline.

        Args:
            stage_id: Current stage identifier

        Returns:
            Next stage identifier, or None if this is the final stage
        """
        stage_sequence = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # Handle substages
        main_stage = stage_id[0] if stage_id else None

        if main_stage in stage_sequence:
            current_idx = stage_sequence.index(main_stage)
            if current_idx < len(stage_sequence) - 1:
                return stage_sequence[current_idx + 1]

        return None

    def _get_required_artifacts(self, stage_id: str) -> List[str]:
        """
        Get list of required artifacts for a stage.

        Args:
            stage_id: Stage identifier

        Returns:
            List of required artifact filenames
        """
        # Stage-specific required artifacts
        artifacts_map = {
            'A': ['research-question.md', 'theoretical-framework.md'],
            'B': ['literature-search.md', 'evidence-summary.md'],
            'C': ['research-design.md', 'methodology.md'],
            'D': ['data-collection-plan.md'],
            'E': ['analysis-plan.md'],
            'F': ['quality-checklist.md'],
            'G': ['manuscript-draft.md'],
            'H': ['specialized-methods.md'],
        }

        # Get main stage (first character)
        main_stage = stage_id[0] if stage_id else None

        return artifacts_map.get(main_stage, [])
