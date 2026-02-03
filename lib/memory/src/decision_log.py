"""
Diverga Memory System v7.0 - Decision Audit Trail Module

This module implements version-controlled decision tracking for research projects.
All decisions are APPEND-ONLY and immutable, preserving complete audit history.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class DecisionLog:
    """
    Decision audit trail with version control and amendment tracking.

    Decisions are APPEND-ONLY and immutable. Amendments create new decision
    entries that reference the original decision.

    Attributes:
        project_root: Root directory of the research project
        log_file: Path to decision-log.yaml
        log_data: Loaded log data structure
    """

    def __init__(self, project_root: Path):
        """
        Initialize DecisionLog with project root.

        Args:
            project_root: Root directory of the research project
        """
        self.project_root = Path(project_root)
        self.log_file = self.project_root / ".research" / "decision-log.yaml"
        self.log_data = self._load_or_create()

    def add_decision(self, decision: dict) -> str:
        """
        Add new decision to the log (APPEND-ONLY, immutable).

        Args:
            decision: Decision dictionary with keys:
                - checkpoint: Checkpoint ID (e.g., "CP_RESEARCH_DIRECTION")
                - stage: Research stage (e.g., "foundation", "evidence")
                - agent: Agent ID that facilitated the decision
                - decision: Dictionary with 'selected' and 'alternatives'
                - rationale: Explanation for the choice
                - metadata: Optional metadata (e.g., user_confirmed)

        Returns:
            decision_id: Unique ID of the created decision (e.g., "dec-001")
        """
        # Generate unique ID
        decision_id = self._generate_decision_id()

        # Add timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Add context
        current_rq = self._get_current_rq()
        prior_decision_ids = self._get_prior_decision_ids()

        # Get session_id from metadata or generate default
        session_id = decision.get('metadata', {}).get('session_id',
                                                      self._get_current_session_id())

        # Build complete decision entry
        decision_entry = {
            'id': decision_id,
            'timestamp': timestamp,
            'checkpoint': decision.get('checkpoint', ''),
            'stage': decision.get('stage', ''),
            'agent': decision.get('agent', ''),
            'decision': {
                'selected': decision.get('decision', {}).get('selected', ''),
                'alternatives': decision.get('decision', {}).get('alternatives', [])
            },
            'rationale': decision.get('rationale', ''),
            'context': {
                'research_question': current_rq,
                'prior_decisions': prior_decision_ids
            },
            'metadata': {
                'session_id': session_id,
                'user_confirmed': decision.get('metadata', {}).get('user_confirmed', True)
            }
        }

        # Append to decisions list (IMMUTABLE - never modify existing)
        self.log_data['decisions'].append(decision_entry)

        # Update last_updated timestamp
        self.log_data['last_updated'] = timestamp

        # Save immediately
        self._save()

        return decision_id

    def amend_decision(self, decision_id: str, new_selected: str,
                      new_rationale: str) -> str:
        """
        Amend an existing decision by creating a new decision entry.

        DO NOT modify original decision. Create NEW decision that references
        original via 'amends' field.

        Args:
            decision_id: ID of the decision being amended
            new_selected: Updated selection
            new_rationale: Explanation for the change

        Returns:
            new_decision_id: ID of the new (amendment) decision
        """
        # Find original decision
        original_decision = self.get_decision(decision_id)
        if not original_decision:
            raise ValueError(f"Decision {decision_id} not found")

        # Create new decision that references original
        new_decision_id = self._generate_decision_id()
        timestamp = datetime.utcnow().isoformat() + "Z"

        amendment_entry = {
            'id': new_decision_id,
            'timestamp': timestamp,
            'checkpoint': original_decision['checkpoint'],
            'stage': original_decision['stage'],
            'agent': original_decision['agent'],
            'decision': {
                'selected': new_selected,
                'alternatives': original_decision['decision']['alternatives']
            },
            'rationale': new_rationale,
            'amends': decision_id,  # Reference to original decision
            'context': {
                'research_question': self._get_current_rq(),
                'prior_decisions': self._get_prior_decision_ids()
            },
            'metadata': {
                'session_id': self._get_current_session_id(),
                'user_confirmed': True,
                'is_amendment': True
            }
        }

        # Append new decision (DO NOT modify original)
        self.log_data['decisions'].append(amendment_entry)
        self.log_data['last_updated'] = timestamp

        # Save immediately
        self._save()

        return new_decision_id

    def get_decision(self, decision_id: str) -> Optional[dict]:
        """
        Get specific decision by ID.

        Args:
            decision_id: Decision ID to retrieve

        Returns:
            Decision dictionary if found, None otherwise
        """
        for decision in self.log_data['decisions']:
            if decision.get('id') == decision_id:
                return decision
        return None

    def get_decision_history(self, checkpoint_id: str) -> List[dict]:
        """
        Get all decisions for a specific checkpoint.

        Args:
            checkpoint_id: Checkpoint ID (e.g., "CP_RESEARCH_DIRECTION")

        Returns:
            List of decisions for this checkpoint, ordered by timestamp
        """
        decisions = [
            d for d in self.log_data['decisions']
            if d.get('checkpoint') == checkpoint_id
        ]
        # Sort by timestamp (oldest first)
        decisions.sort(key=lambda d: d.get('timestamp', ''))
        return decisions

    def get_stage_decisions(self, stage: str) -> List[dict]:
        """
        Get all decisions for a specific research stage.

        Args:
            stage: Research stage (e.g., "foundation", "evidence", "design")

        Returns:
            List of decisions from that stage, ordered by timestamp
        """
        decisions = [
            d for d in self.log_data['decisions']
            if d.get('stage') == stage
        ]
        decisions.sort(key=lambda d: d.get('timestamp', ''))
        return decisions

    def get_recent_decisions(self, limit: int = 5) -> List[dict]:
        """
        Get most recent decisions.

        Args:
            limit: Maximum number of decisions to return

        Returns:
            List of most recent decisions, ordered by timestamp (newest first)
        """
        decisions = self.log_data['decisions'].copy()
        decisions.sort(key=lambda d: d.get('timestamp', ''), reverse=True)
        return decisions[:limit]

    def get_amended_decisions(self) -> List[dict]:
        """
        Get all decisions that have been amended.

        Returns:
            List of original decisions that have amendments
        """
        # Find all amendment decision IDs
        amendment_refs = set()
        for decision in self.log_data['decisions']:
            if 'amends' in decision:
                amendment_refs.add(decision['amends'])

        # Get original decisions that have amendments
        amended = [
            d for d in self.log_data['decisions']
            if d.get('id') in amendment_refs
        ]

        return amended

    def _load_or_create(self) -> dict:
        """
        Load log file or create empty structure.

        Returns:
            Log data dictionary
        """
        if not self.log_file.exists():
            # Create default structure
            return self._create_default_structure()

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}

            # Ensure required fields exist
            if 'decisions' not in data:
                data['decisions'] = []
            if 'version' not in data:
                data['version'] = "7.0"

            return data
        except Exception as e:
            print(f"Warning: Failed to load decision log: {e}")
            return self._create_default_structure()

    def _create_default_structure(self) -> dict:
        """
        Create default log structure.

        Returns:
            Default log data dictionary
        """
        # Try to get project name from project-state.yaml
        project_name = "Unknown Project"
        state_file = self.project_root / ".research" / "project-state.yaml"
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state_data = yaml.safe_load(f) or {}
                    project_name = state_data.get('project_name', project_name)
            except Exception:
                pass

        return {
            'version': "7.0",
            'project': project_name,
            'created': datetime.utcnow().isoformat() + "Z",
            'last_updated': datetime.utcnow().isoformat() + "Z",
            'decisions': []
        }

    def _save(self) -> bool:
        """
        Save log file with proper formatting.

        Returns:
            True if save successful, False otherwise
        """
        # Ensure directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                # Add header comment
                f.write("# Diverga Decision Log v7.0\n")
                f.write("# This file records all human decisions made during the research process\n")
                f.write("# Decisions are APPEND-ONLY and immutable\n\n")

                # Write YAML with proper formatting
                yaml.dump(
                    self.log_data,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2
                )
            return True
        except Exception as e:
            print(f"Warning: Failed to save decision log: {e}")
            return False

    def _get_current_rq(self) -> str:
        """
        Get current research question from project-state.yaml.

        Returns:
            Research question string, or empty string if not found
        """
        state_file = self.project_root / ".research" / "project-state.yaml"
        if not state_file.exists():
            return ""

        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = yaml.safe_load(f) or {}
                return state_data.get('research_question', '')
        except Exception:
            return ""

    def _get_prior_decision_ids(self) -> List[str]:
        """
        Get list of prior decision IDs.

        Returns:
            List of decision IDs in chronological order
        """
        return [d.get('id', '') for d in self.log_data['decisions']]

    def _generate_decision_id(self) -> str:
        """
        Generate unique decision ID.

        Returns:
            Decision ID in format "dec-XXX" where XXX is zero-padded sequence
        """
        # Get highest existing sequence number
        max_seq = 0
        for decision in self.log_data['decisions']:
            decision_id = decision.get('id', '')
            if decision_id.startswith('dec-'):
                try:
                    seq = int(decision_id.split('-')[1])
                    max_seq = max(max_seq, seq)
                except (ValueError, IndexError):
                    pass

        # Generate next ID
        next_seq = max_seq + 1
        return f"dec-{next_seq:03d}"

    def _get_current_session_id(self) -> str:
        """
        Get current session ID from project state or generate default.

        Returns:
            Session ID string
        """
        state_file = self.project_root / ".research" / "project-state.yaml"
        if not state_file.exists():
            return f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = yaml.safe_load(f) or {}
                # Look for session_id in metadata or generate from timestamp
                metadata = state_data.get('metadata', {})
                session_id = metadata.get('session_id')
                if session_id:
                    return session_id

                # Generate from last_updated timestamp
                last_updated = state_data.get('last_updated', '')
                if last_updated:
                    # Convert ISO timestamp to session ID
                    try:
                        dt = datetime.fromisoformat(last_updated.replace('Z', ''))
                        return f"session_{dt.strftime('%Y%m%d_%H%M%S')}"
                    except Exception:
                        pass

                return f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        except Exception:
            return f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
