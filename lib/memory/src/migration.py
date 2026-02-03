"""
Diverga Memory System v6.8 → v7.0 Migration Script

This module provides migration utilities to upgrade existing Diverga research projects
from Memory System v6.8 to v7.0.

Key changes in v7.0:
- New directory structure: baselines/, changes/, sessions/
- Enhanced project-state.yaml schema with version tracking
- Updated decision-log.yaml format with context and metadata
- Expanded checkpoint definitions
- Session tracking and summary fields

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None


class MigrationError(Exception):
    """Raised when migration encounters an error."""
    pass


class MigrationLogger:
    """Simple logger for migration operations."""

    def __init__(self):
        self.logs: List[Dict[str, str]] = []

    def info(self, message: str) -> None:
        """Log info message."""
        self.logs.append({"level": "INFO", "message": message, "timestamp": datetime.utcnow().isoformat()})
        print(f"[INFO] {message}")

    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logs.append({"level": "WARNING", "message": message, "timestamp": datetime.utcnow().isoformat()})
        print(f"[WARNING] {message}")

    def error(self, message: str) -> None:
        """Log error message."""
        self.logs.append({"level": "ERROR", "message": message, "timestamp": datetime.utcnow().isoformat()})
        print(f"[ERROR] {message}")

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of migration logs."""
        return {
            "total_logs": len(self.logs),
            "errors": len([l for l in self.logs if l["level"] == "ERROR"]),
            "warnings": len([l for l in self.logs if l["level"] == "WARNING"]),
            "logs": self.logs
        }


def detect_version(project_root: Path) -> str:
    """
    Detect the current version of Diverga Memory System in use.

    Checks for .research/project-state.yaml and looks for version field.
    If no version found, defaults to "6.8" (pre-versioning).

    Args:
        project_root: Root directory of the research project

    Returns:
        Version string (e.g., "6.8", "7.0")
    """
    if yaml is None:
        raise MigrationError("PyYAML is required for migration. Install with: pip install pyyaml")

    research_dir = project_root / ".research"
    state_file = research_dir / "project-state.yaml"

    # No .research directory = no Diverga project
    if not research_dir.exists():
        return "none"

    # No project-state.yaml = very old or corrupted
    if not state_file.exists():
        return "unknown"

    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f) or {}

        # Check for version field
        version = state.get("version")
        if version:
            return str(version)

        # No version field = pre-v7.0 (assume 6.8)
        return "6.8"

    except Exception as e:
        raise MigrationError(f"Failed to read project-state.yaml: {e}")


def needs_migration(project_root: Path) -> bool:
    """
    Check if a project needs migration to v7.0.

    Args:
        project_root: Root directory of the research project

    Returns:
        True if migration is needed, False otherwise
    """
    version = detect_version(project_root)

    # No project or unknown version
    if version in ["none", "unknown"]:
        return False

    # Already at v7.0 or higher
    if version >= "7.0":
        return False

    # v6.8 or lower needs migration
    return True


def create_backup(project_root: Path) -> Path:
    """
    Create a backup of the .research/ directory before migration.

    Creates .research-backup-v68/ directory with timestamp.

    Args:
        project_root: Root directory of the research project

    Returns:
        Path to the backup directory

    Raises:
        MigrationError: If backup creation fails
    """
    research_dir = project_root / ".research"

    if not research_dir.exists():
        raise MigrationError("No .research/ directory found to backup")

    # Create timestamped backup directory
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_dir = project_root / f".research-backup-v68-{timestamp}"

    try:
        # Copy entire .research/ directory
        shutil.copytree(research_dir, backup_dir)
        return backup_dir

    except Exception as e:
        raise MigrationError(f"Failed to create backup: {e}")


def _ensure_field(data: dict, field: str, default: Any) -> bool:
    """
    Ensure a field exists in a dictionary with a default value.

    Args:
        data: Dictionary to check
        field: Field name
        default: Default value if field is missing

    Returns:
        True if field was added, False if it already existed
    """
    if field not in data:
        data[field] = default
        return True
    return False


def _copy_with_transform(src: Path, dst: Path, transform_fn: callable) -> None:
    """
    Copy a file and apply a transformation function.

    Args:
        src: Source file path
        dst: Destination file path
        transform_fn: Function that takes data dict and returns transformed dict
    """
    if yaml is None:
        raise MigrationError("PyYAML is required")

    # Read source
    with open(src, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    # Transform
    transformed = transform_fn(data)

    # Write destination
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        yaml.safe_dump(transformed, f, default_flow_style=False, allow_unicode=True)


def migrate_project_state(project_root: Path, logger: MigrationLogger) -> dict:
    """
    Migrate project-state.yaml to v7.0 schema.

    Changes:
    - Add version: "7.0" field
    - Add last_session_summary field if missing
    - Add sessions array if missing
    - Ensure updated_at exists

    Args:
        project_root: Root directory of the research project
        logger: Migration logger

    Returns:
        Dictionary with changes made
    """
    if yaml is None:
        raise MigrationError("PyYAML is required")

    state_file = project_root / ".research" / "project-state.yaml"
    changes = {
        "fields_added": [],
        "fields_updated": []
    }

    if not state_file.exists():
        logger.warning("project-state.yaml not found, skipping migration")
        return changes

    try:
        # Read current state
        with open(state_file, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f) or {}

        # Add version field
        if _ensure_field(state, "version", "7.0"):
            changes["fields_added"].append("version")
            logger.info("Added version field: 7.0")
        else:
            state["version"] = "7.0"
            changes["fields_updated"].append("version")
            logger.info("Updated version to 7.0")

        # Add last_session_summary
        if _ensure_field(state, "last_session_summary", ""):
            changes["fields_added"].append("last_session_summary")
            logger.info("Added last_session_summary field")

        # Add sessions array
        if _ensure_field(state, "sessions", []):
            changes["fields_added"].append("sessions")
            logger.info("Added sessions array")

        # Ensure updated_at exists
        if _ensure_field(state, "updated_at", datetime.utcnow().isoformat()):
            changes["fields_added"].append("updated_at")
            logger.info("Added updated_at timestamp")

        # Ensure all_decisions exists as dict
        if _ensure_field(state, "all_decisions", {}):
            changes["fields_added"].append("all_decisions")
            logger.info("Added all_decisions dictionary")

        # Write updated state
        with open(state_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)

        logger.info("project-state.yaml migration complete")
        return changes

    except Exception as e:
        logger.error(f"Failed to migrate project-state.yaml: {e}")
        raise MigrationError(f"project-state.yaml migration failed: {e}")


def migrate_decisions(project_root: Path, logger: MigrationLogger) -> dict:
    """
    Migrate decision-log.yaml to v7.0 schema.

    Changes:
    - Add context field to each decision
    - Add metadata section to each decision
    - Ensure amendments field exists (list)
    - Add timestamp if missing

    Args:
        project_root: Root directory of the research project
        logger: Migration logger

    Returns:
        Dictionary with changes made
    """
    if yaml is None:
        raise MigrationError("PyYAML is required")

    decision_file = project_root / ".research" / "decision-log.yaml"
    changes = {
        "decisions_migrated": 0,
        "fields_added": []
    }

    if not decision_file.exists():
        logger.warning("decision-log.yaml not found, creating new file")
        decision_file.parent.mkdir(parents=True, exist_ok=True)
        with open(decision_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump({"decisions": []}, f)
        return changes

    try:
        # Read current decisions
        with open(decision_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        decisions = data.get("decisions", [])

        # Migrate each decision
        for decision in decisions:
            modified = False

            # Add context field
            if _ensure_field(decision, "context", ""):
                changes["fields_added"].append("context")
                modified = True

            # Add metadata section
            if _ensure_field(decision, "metadata", {}):
                changes["fields_added"].append("metadata")
                modified = True

            # Populate metadata if empty
            if not decision["metadata"]:
                decision["metadata"] = {
                    "migrated_from": "6.8",
                    "migration_timestamp": datetime.utcnow().isoformat()
                }
                modified = True

            # Ensure amendments field exists
            if _ensure_field(decision, "amendments", []):
                changes["fields_added"].append("amendments")
                modified = True

            # Add timestamp if missing
            if _ensure_field(decision, "timestamp", datetime.utcnow().isoformat()):
                changes["fields_added"].append("timestamp")
                modified = True

            if modified:
                changes["decisions_migrated"] += 1

        # Write updated decisions
        with open(decision_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)

        logger.info(f"Migrated {changes['decisions_migrated']} decisions")
        return changes

    except Exception as e:
        logger.error(f"Failed to migrate decision-log.yaml: {e}")
        raise MigrationError(f"decision-log.yaml migration failed: {e}")


def migrate_checkpoints(project_root: Path, logger: MigrationLogger) -> dict:
    """
    Migrate checkpoints.yaml to v7.0 schema.

    Changes:
    - Update trigger format to new CheckpointTrigger structure
    - Add new checkpoint definitions if missing
    - Ensure all required fields exist

    Args:
        project_root: Root directory of the research project
        logger: Migration logger

    Returns:
        Dictionary with changes made
    """
    if yaml is None:
        raise MigrationError("PyYAML is required")

    checkpoints_file = project_root / ".research" / "checkpoints.yaml"
    changes = {
        "checkpoints_added": 0,
        "checkpoints_updated": 0
    }

    # Create default checkpoints if file doesn't exist
    if not checkpoints_file.exists():
        logger.warning("checkpoints.yaml not found, creating with default checkpoints")
        default_checkpoints = {
            "checkpoints": [
                {
                    "id": "RESEARCH_DIRECTION",
                    "name": "Research Direction Selection",
                    "level": "required",
                    "icon": "🔴",
                    "stage": "A",
                    "agents": ["a1", "a2"],
                    "triggers": [{"type": "decision", "decision_key": "research_question"}],
                    "validation": {"required_fields": ["research_question"]},
                    "persistence": "both"
                },
                {
                    "id": "PARADIGM_SELECTION",
                    "name": "Research Paradigm Selection",
                    "level": "required",
                    "icon": "🔴",
                    "stage": "A",
                    "agents": ["a5"],
                    "triggers": [{"type": "decision", "decision_key": "paradigm"}],
                    "validation": {"required_fields": ["paradigm"]},
                    "persistence": "both"
                }
            ]
        }
        checkpoints_file.parent.mkdir(parents=True, exist_ok=True)
        with open(checkpoints_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(default_checkpoints, f, default_flow_style=False, allow_unicode=True)
        changes["checkpoints_added"] = len(default_checkpoints["checkpoints"])
        logger.info(f"Created checkpoints.yaml with {changes['checkpoints_added']} default checkpoints")
        return changes

    try:
        # Read current checkpoints
        with open(checkpoints_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        checkpoints = data.get("checkpoints", [])

        # Update each checkpoint
        for checkpoint in checkpoints:
            modified = False

            # Ensure triggers is a list of dicts
            if "triggers" in checkpoint:
                if not isinstance(checkpoint["triggers"], list):
                    checkpoint["triggers"] = [{"type": "manual"}]
                    modified = True
                else:
                    # Update old string triggers to dict format
                    new_triggers = []
                    for trigger in checkpoint["triggers"]:
                        if isinstance(trigger, str):
                            new_triggers.append({"type": trigger})
                            modified = True
                        elif isinstance(trigger, dict):
                            new_triggers.append(trigger)
                    if modified:
                        checkpoint["triggers"] = new_triggers
            else:
                checkpoint["triggers"] = [{"type": "manual"}]
                modified = True

            # Ensure persistence field
            if _ensure_field(checkpoint, "persistence", "memory"):
                modified = True

            # Ensure validation field
            if _ensure_field(checkpoint, "validation", {}):
                modified = True

            if modified:
                changes["checkpoints_updated"] += 1

        # Write updated checkpoints
        with open(checkpoints_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)

        logger.info(f"Updated {changes['checkpoints_updated']} checkpoints")
        return changes

    except Exception as e:
        logger.error(f"Failed to migrate checkpoints.yaml: {e}")
        raise MigrationError(f"checkpoints.yaml migration failed: {e}")


def migrate_directory_structure(project_root: Path, logger: MigrationLogger) -> dict:
    """
    Migrate directory structure to v7.0 format.

    Creates new directories:
    - baselines/literature/
    - baselines/methodology/
    - baselines/framework/
    - changes/current/
    - changes/archive/
    - sessions/

    Args:
        project_root: Root directory of the research project
        logger: Migration logger

    Returns:
        Dictionary with changes made
    """
    research_dir = project_root / ".research"
    changes = {
        "directories_created": []
    }

    # Define new directory structure
    new_directories = [
        research_dir / "baselines" / "literature",
        research_dir / "baselines" / "methodology",
        research_dir / "baselines" / "framework",
        research_dir / "changes" / "current",
        research_dir / "changes" / "archive",
        research_dir / "sessions",
    ]

    # Create directories
    for directory in new_directories:
        if not directory.exists():
            try:
                directory.mkdir(parents=True, exist_ok=True)
                changes["directories_created"].append(str(directory.relative_to(project_root)))
                logger.info(f"Created directory: {directory.relative_to(project_root)}")
            except Exception as e:
                logger.error(f"Failed to create directory {directory}: {e}")

    return changes


def update_version(project_root: Path, version: str) -> None:
    """
    Update the version field in project-state.yaml.

    Args:
        project_root: Root directory of the research project
        version: Version string to set
    """
    if yaml is None:
        raise MigrationError("PyYAML is required")

    state_file = project_root / ".research" / "project-state.yaml"

    if not state_file.exists():
        raise MigrationError("project-state.yaml not found")

    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f) or {}

        state["version"] = version
        state["updated_at"] = datetime.utcnow().isoformat()

        with open(state_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)

    except Exception as e:
        raise MigrationError(f"Failed to update version: {e}")


def rollback(project_root: Path, backup_path: Path) -> bool:
    """
    Rollback migration by restoring from backup.

    Args:
        project_root: Root directory of the research project
        backup_path: Path to the backup directory

    Returns:
        True if rollback successful, False otherwise
    """
    research_dir = project_root / ".research"

    if not backup_path.exists():
        print(f"[ERROR] Backup directory not found: {backup_path}")
        return False

    try:
        # Remove current .research/ directory
        if research_dir.exists():
            shutil.rmtree(research_dir)

        # Restore from backup
        shutil.copytree(backup_path, research_dir)

        print(f"[SUCCESS] Rolled back to backup: {backup_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Rollback failed: {e}")
        return False


def migrate_v68_to_v70(project_root: Path, dry_run: bool = False) -> dict:
    """
    Main migration function from v6.8 to v7.0.

    Migration steps:
    1. Detect current version
    2. Create backup
    3. Migrate directory structure
    4. Migrate project-state.yaml
    5. Migrate decision-log.yaml
    6. Migrate checkpoints.yaml
    7. Update version to 7.0

    Args:
        project_root: Root directory of the research project
        dry_run: If True, only show what would change without making changes

    Returns:
        Dictionary with migration results
    """
    project_root = Path(project_root)
    logger = MigrationLogger()

    results = {
        "success": False,
        "dry_run": dry_run,
        "version_from": None,
        "version_to": "7.0",
        "backup_path": None,
        "changes": {},
        "errors": [],
        "logs": []
    }

    try:
        # Step 1: Detect version
        logger.info("Starting migration from v6.8 to v7.0")
        current_version = detect_version(project_root)
        results["version_from"] = current_version

        if current_version == "none":
            logger.error("No .research/ directory found - not a Diverga project")
            results["errors"].append("Not a Diverga project")
            results["logs"] = logger.get_summary()
            return results

        if current_version >= "7.0":
            logger.info(f"Project already at version {current_version}, no migration needed")
            results["success"] = True
            results["logs"] = logger.get_summary()
            return results

        logger.info(f"Detected version: {current_version}")

        # Step 2: Create backup (skip in dry_run)
        if not dry_run:
            logger.info("Creating backup...")
            backup_path = create_backup(project_root)
            results["backup_path"] = str(backup_path)
            logger.info(f"Backup created: {backup_path}")
        else:
            logger.info("[DRY RUN] Would create backup")

        # Step 3: Migrate directory structure
        logger.info("Migrating directory structure...")
        if not dry_run:
            dir_changes = migrate_directory_structure(project_root, logger)
            results["changes"]["directory_structure"] = dir_changes
        else:
            logger.info("[DRY RUN] Would create: baselines/, changes/, sessions/")

        # Step 4: Migrate project-state.yaml
        logger.info("Migrating project-state.yaml...")
        if not dry_run:
            state_changes = migrate_project_state(project_root, logger)
            results["changes"]["project_state"] = state_changes
        else:
            logger.info("[DRY RUN] Would add: version, last_session_summary, sessions")

        # Step 5: Migrate decision-log.yaml
        logger.info("Migrating decision-log.yaml...")
        if not dry_run:
            decision_changes = migrate_decisions(project_root, logger)
            results["changes"]["decisions"] = decision_changes
        else:
            logger.info("[DRY RUN] Would add: context, metadata, amendments to decisions")

        # Step 6: Migrate checkpoints.yaml
        logger.info("Migrating checkpoints.yaml...")
        if not dry_run:
            checkpoint_changes = migrate_checkpoints(project_root, logger)
            results["changes"]["checkpoints"] = checkpoint_changes
        else:
            logger.info("[DRY RUN] Would update checkpoint trigger format")

        # Step 7: Update version
        if not dry_run:
            logger.info("Updating version to 7.0...")
            update_version(project_root, "7.0")
            logger.info("Migration complete!")
        else:
            logger.info("[DRY RUN] Would update version to 7.0")

        results["success"] = True
        results["logs"] = logger.get_summary()

        return results

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        results["errors"].append(str(e))
        results["logs"] = logger.get_summary()
        return results


def print_migration_report(results: dict) -> None:
    """
    Print a formatted migration report.

    Args:
        results: Migration results dictionary
    """
    print("\n" + "=" * 70)
    print("Diverga Memory System Migration Report")
    print("=" * 70)

    if results["dry_run"]:
        print("MODE: DRY RUN (no changes made)")
    else:
        print("MODE: LIVE MIGRATION")

    print(f"\nVersion: {results['version_from']} → {results['version_to']}")

    if results["success"]:
        print("\nSTATUS: ✓ SUCCESS")
    else:
        print("\nSTATUS: ✗ FAILED")

    if results.get("backup_path"):
        print(f"\nBackup: {results['backup_path']}")

    if results.get("changes"):
        print("\nChanges Made:")
        for category, changes in results["changes"].items():
            print(f"\n  {category}:")
            if isinstance(changes, dict):
                for key, value in changes.items():
                    if isinstance(value, list) and len(value) > 0:
                        print(f"    - {key}: {len(value)} items")
                    elif isinstance(value, (int, str)):
                        print(f"    - {key}: {value}")
            else:
                print(f"    {changes}")

    if results.get("errors"):
        print("\nErrors:")
        for error in results["errors"]:
            print(f"  ✗ {error}")

    log_summary = results.get("logs", {})
    if log_summary:
        print(f"\nLogs: {log_summary.get('total_logs', 0)} total")
        print(f"  Errors: {log_summary.get('errors', 0)}")
        print(f"  Warnings: {log_summary.get('warnings', 0)}")

    print("\n" + "=" * 70 + "\n")


# CLI interface
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate Diverga Memory System from v6.8 to v7.0"
    )
    parser.add_argument(
        "project_root",
        type=str,
        help="Path to research project root directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
    )
    parser.add_argument(
        "--rollback",
        type=str,
        help="Rollback using specified backup directory"
    )

    args = parser.parse_args()

    project_root = Path(args.project_root)

    # Rollback mode
    if args.rollback:
        backup_path = Path(args.rollback)
        print(f"Rolling back to: {backup_path}")
        success = rollback(project_root, backup_path)
        sys.exit(0 if success else 1)

    # Migration mode
    results = migrate_v68_to_v70(project_root, dry_run=args.dry_run)
    print_migration_report(results)

    sys.exit(0 if results["success"] else 1)
