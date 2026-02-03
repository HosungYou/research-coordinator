"""
Diverga Memory System v7.0 - Research Schema Manager

This module provides research type schema management for the Diverga Memory System.
Schemas define the structure of research pipelines including stages, artifacts,
checkpoints, and dependencies.

Author: Diverga Project
Version: 7.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


# Default schema for systematic literature review
SYSTEMATIC_REVIEW_SCHEMA = {
    "name": "systematic-review",
    "version": "1.0",
    "description": "PRISMA 2020-compliant systematic literature review pipeline",
    "stages": [
        {
            "id": "identification",
            "name": "Stage 1: Identification",
            "description": "Define research protocol and search strategy",
            "artifacts": [
                {
                    "id": "protocol",
                    "name": "Research Protocol",
                    "generates": "protocol.md",
                    "template": "templates/protocol.md",
                    "requires": [],
                    "validation": {
                        "required_fields": [
                            "research_question",
                            "databases",
                            "search_terms"
                        ]
                    }
                },
                {
                    "id": "search-strategy",
                    "name": "Search Strategy",
                    "generates": "search-strategy.md",
                    "template": "templates/search-strategy.md",
                    "requires": ["protocol"],
                    "validation": {
                        "required_fields": ["databases", "search_string"]
                    }
                }
            ],
            "checkpoints": ["CP_RESEARCH_DIRECTION", "CP_DATABASE_SELECTION"]
        },
        {
            "id": "screening",
            "name": "Stage 2: Screening",
            "description": "Define inclusion/exclusion criteria and screen papers",
            "artifacts": [
                {
                    "id": "inclusion-criteria",
                    "name": "Inclusion/Exclusion Criteria",
                    "generates": "inclusion-criteria.md",
                    "template": "templates/inclusion-criteria.md",
                    "requires": ["search-strategy"],
                    "validation": {
                        "required_fields": ["inclusion_criteria", "exclusion_criteria"]
                    }
                },
                {
                    "id": "screening-results",
                    "name": "Screening Results",
                    "generates": "data/screening-results.csv",
                    "requires": ["inclusion-criteria"],
                    "validation": {
                        "min_screened": 10
                    }
                }
            ],
            "checkpoints": ["CP_SCREENING_CRITERIA"]
        },
        {
            "id": "eligibility",
            "name": "Stage 3: Eligibility Assessment",
            "description": "Full-text review and quality assessment",
            "artifacts": [
                {
                    "id": "quality-assessment",
                    "name": "Quality Assessment",
                    "generates": "data/quality-assessment.csv",
                    "requires": ["screening-results"],
                    "validation": {
                        "required_fields": ["study_id", "quality_score", "bias_risk"]
                    }
                },
                {
                    "id": "data-extraction",
                    "name": "Data Extraction Form",
                    "generates": "data-extraction-form.xlsx",
                    "template": "templates/extraction-form.xlsx",
                    "requires": ["quality-assessment"],
                    "validation": {
                        "required_fields": ["study_characteristics", "outcomes"]
                    }
                }
            ],
            "checkpoints": ["CP_QUALITY_CRITERIA"]
        },
        {
            "id": "synthesis",
            "name": "Stage 4: Evidence Synthesis",
            "description": "Synthesize findings and prepare analysis",
            "artifacts": [
                {
                    "id": "extracted-data",
                    "name": "Extracted Data",
                    "generates": "data/extracted-data.csv",
                    "requires": ["data-extraction"],
                    "validation": {
                        "min_studies": 5
                    }
                },
                {
                    "id": "synthesis-plan",
                    "name": "Synthesis Plan",
                    "generates": "synthesis-plan.md",
                    "requires": ["extracted-data"],
                    "validation": {
                        "required_fields": ["synthesis_method", "heterogeneity_plan"]
                    }
                }
            ],
            "checkpoints": ["CP_SYNTHESIS_APPROACH"]
        },
        {
            "id": "reporting",
            "name": "Stage 5: Reporting",
            "description": "Prepare manuscript and PRISMA flow diagram",
            "artifacts": [
                {
                    "id": "prisma-diagram",
                    "name": "PRISMA Flow Diagram",
                    "generates": "outputs/prisma-diagram.png",
                    "requires": ["synthesis-plan"],
                    "validation": {
                        "file_exists": True
                    }
                },
                {
                    "id": "manuscript",
                    "name": "Manuscript Draft",
                    "generates": "outputs/manuscript.docx",
                    "requires": ["prisma-diagram"],
                    "validation": {
                        "min_word_count": 3000
                    }
                }
            ],
            "checkpoints": ["CP_REPORTING_COMPLETE"]
        }
    ]
}


# Default schema for meta-analysis
META_ANALYSIS_SCHEMA = {
    "name": "meta-analysis",
    "version": "1.0",
    "description": "Meta-analysis pipeline with effect size extraction and pooling",
    "stages": [
        {
            "id": "planning",
            "name": "Stage 1: Meta-Analysis Planning",
            "description": "Define research question and analysis plan",
            "artifacts": [
                {
                    "id": "ma-protocol",
                    "name": "Meta-Analysis Protocol",
                    "generates": "protocol.md",
                    "template": "templates/ma-protocol.md",
                    "requires": [],
                    "validation": {
                        "required_fields": [
                            "research_question",
                            "effect_size_metric",
                            "pooling_method"
                        ]
                    }
                }
            ],
            "checkpoints": ["CP_RESEARCH_DIRECTION", "CP_EFFECT_SIZE_METRIC"]
        },
        {
            "id": "identification",
            "name": "Stage 2: Study Identification",
            "description": "Search and screen studies",
            "artifacts": [
                {
                    "id": "search-strategy",
                    "name": "Search Strategy",
                    "generates": "search-strategy.md",
                    "requires": ["ma-protocol"],
                    "validation": {
                        "required_fields": ["databases", "search_string"]
                    }
                },
                {
                    "id": "screening-results",
                    "name": "Screening Results",
                    "generates": "data/screening-results.csv",
                    "requires": ["search-strategy"],
                    "validation": {
                        "min_screened": 20
                    }
                }
            ],
            "checkpoints": ["CP_DATABASE_SELECTION", "CP_SCREENING_CRITERIA"]
        },
        {
            "id": "extraction",
            "name": "Stage 3: Data Extraction",
            "description": "Extract effect sizes and study characteristics",
            "artifacts": [
                {
                    "id": "extraction-form",
                    "name": "Data Extraction Form",
                    "generates": "extraction-form.xlsx",
                    "template": "templates/ma-extraction-form.xlsx",
                    "requires": ["screening-results"],
                    "validation": {
                        "required_fields": [
                            "study_id",
                            "effect_size",
                            "sample_size",
                            "moderators"
                        ]
                    }
                },
                {
                    "id": "extracted-effects",
                    "name": "Extracted Effect Sizes",
                    "generates": "data/effect-sizes.csv",
                    "requires": ["extraction-form"],
                    "validation": {
                        "min_studies": 5,
                        "required_fields": ["effect_size", "variance", "sample_size"]
                    }
                }
            ],
            "checkpoints": ["CP_EXTRACTION_COMPLETE", "CP_DATA_INTEGRITY"]
        },
        {
            "id": "analysis",
            "name": "Stage 4: Meta-Analytic Analysis",
            "description": "Pool effect sizes and conduct moderator analyses",
            "artifacts": [
                {
                    "id": "pooled-effects",
                    "name": "Pooled Effect Sizes",
                    "generates": "data/pooled-effects.csv",
                    "requires": ["extracted-effects"],
                    "validation": {
                        "required_fields": ["pooled_effect", "ci_lower", "ci_upper", "heterogeneity"]
                    }
                },
                {
                    "id": "forest-plot",
                    "name": "Forest Plot",
                    "generates": "outputs/forest-plot.png",
                    "requires": ["pooled-effects"],
                    "validation": {
                        "file_exists": True
                    }
                }
            ],
            "checkpoints": ["CP_HETEROGENEITY_HANDLED", "CP_SENSITIVITY_COMPLETE"]
        },
        {
            "id": "reporting",
            "name": "Stage 5: Meta-Analysis Reporting",
            "description": "Prepare manuscript and supplementary materials",
            "artifacts": [
                {
                    "id": "prisma-diagram",
                    "name": "PRISMA Flow Diagram",
                    "generates": "outputs/prisma-diagram.png",
                    "requires": ["pooled-effects"],
                    "validation": {
                        "file_exists": True
                    }
                },
                {
                    "id": "manuscript",
                    "name": "Meta-Analysis Manuscript",
                    "generates": "outputs/manuscript.docx",
                    "requires": ["prisma-diagram", "forest-plot"],
                    "validation": {
                        "min_word_count": 4000
                    }
                }
            ],
            "checkpoints": ["CP_REPORTING_COMPLETE"]
        }
    ]
}


@dataclass
class ResearchSchema:
    """
    Manager for research type schemas.

    Provides methods to load, query, and validate research pipeline schemas
    that define stages, artifacts, checkpoints, and dependencies.

    Attributes:
        schema: The loaded schema dictionary
        schema_path: Path to the schema file (if loaded from file)
    """

    schema: Dict[str, Any] = field(default_factory=dict)
    schema_path: Optional[Path] = None

    def __init__(self, schema_path: Optional[Path] = None, schema_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize the schema manager.

        Args:
            schema_path: Path to YAML schema file (optional)
            schema_dict: Schema dictionary to use directly (optional)

        If neither argument is provided, uses default SYSTEMATIC_REVIEW_SCHEMA.
        """
        if schema_path is not None:
            self.schema_path = Path(schema_path)
            self.schema = self._load_from_file(self.schema_path)
        elif schema_dict is not None:
            self.schema = schema_dict
            self.schema_path = None
        else:
            # Use default systematic review schema
            self.schema = SYSTEMATIC_REVIEW_SCHEMA.copy()
            self.schema_path = None

    def _load_from_file(self, path: Path) -> Dict[str, Any]:
        """
        Load schema from YAML file.

        Args:
            path: Path to YAML file

        Returns:
            Schema dictionary

        Raises:
            FileNotFoundError: If schema file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_stages(self) -> List[dict]:
        """
        Get all stages defined in the schema.

        Returns:
            List of stage dictionaries
        """
        return self.schema.get('stages', [])

    def get_stage(self, stage_id: str) -> Optional[dict]:
        """
        Get a specific stage definition.

        Args:
            stage_id: Unique stage identifier

        Returns:
            Stage dictionary if found, None otherwise
        """
        for stage in self.get_stages():
            if stage.get('id') == stage_id:
                return stage
        return None

    def get_artifact(self, artifact_id: str) -> Optional[dict]:
        """
        Get artifact definition across all stages.

        Args:
            artifact_id: Unique artifact identifier

        Returns:
            Artifact dictionary if found, None otherwise
        """
        for stage in self.get_stages():
            for artifact in stage.get('artifacts', []):
                if artifact.get('id') == artifact_id:
                    return artifact
        return None

    def get_stage_artifacts(self, stage_id: str) -> List[dict]:
        """
        Get all artifacts for a specific stage.

        Args:
            stage_id: Stage identifier

        Returns:
            List of artifact dictionaries for the stage
        """
        stage = self.get_stage(stage_id)
        if stage is None:
            return []
        return stage.get('artifacts', [])

    def get_checkpoints_for_stage(self, stage_id: str) -> List[str]:
        """
        Get checkpoint IDs for a specific stage.

        Args:
            stage_id: Stage identifier

        Returns:
            List of checkpoint ID strings
        """
        stage = self.get_stage(stage_id)
        if stage is None:
            return []
        return stage.get('checkpoints', [])

    def validate_artifact_dependencies(self, artifact_id: str, completed_artifacts: Optional[List[str]] = None) -> Tuple[bool, List[str]]:
        """
        Check if artifact dependencies are met.

        Args:
            artifact_id: Artifact identifier to check
            completed_artifacts: List of completed artifact IDs (default: empty)

        Returns:
            Tuple of (dependencies_met: bool, missing_dependencies: List[str])
        """
        if completed_artifacts is None:
            completed_artifacts = []

        artifact = self.get_artifact(artifact_id)
        if artifact is None:
            return False, [f"Artifact '{artifact_id}' not found"]

        required = artifact.get('requires', [])
        missing = [dep for dep in required if dep not in completed_artifacts]

        return len(missing) == 0, missing

    def get_next_stage(self, current_stage_id: str) -> Optional[str]:
        """
        Get the next stage ID in the pipeline.

        Args:
            current_stage_id: Current stage identifier

        Returns:
            Next stage ID if exists, None if current is last stage
        """
        stages = self.get_stages()
        stage_ids = [s.get('id') for s in stages]

        try:
            current_index = stage_ids.index(current_stage_id)
            if current_index < len(stage_ids) - 1:
                return stage_ids[current_index + 1]
        except ValueError:
            pass

        return None

    def get_stage_progress(self, stage_id: str, completed_artifacts: List[str]) -> float:
        """
        Calculate completion percentage for a stage.

        Args:
            stage_id: Stage identifier
            completed_artifacts: List of completed artifact IDs

        Returns:
            Completion percentage (0.0 to 1.0)
        """
        artifacts = self.get_stage_artifacts(stage_id)
        if not artifacts:
            return 0.0

        artifact_ids = [a.get('id') for a in artifacts]
        completed_count = sum(1 for aid in artifact_ids if aid in completed_artifacts)

        return completed_count / len(artifact_ids)

    def get_all_checkpoints(self) -> List[str]:
        """
        Get all unique checkpoint IDs across all stages.

        Returns:
            List of unique checkpoint IDs
        """
        checkpoints = set()
        for stage in self.get_stages():
            for cp in stage.get('checkpoints', []):
                checkpoints.add(cp)
        return sorted(list(checkpoints))

    def get_artifact_by_path(self, file_path: str) -> Optional[dict]:
        """
        Find artifact definition by generated file path.

        Args:
            file_path: File path that artifact generates

        Returns:
            Artifact dictionary if found, None otherwise
        """
        for stage in self.get_stages():
            for artifact in stage.get('artifacts', []):
                if artifact.get('generates') == file_path:
                    return artifact
        return None

    def export_as_yaml(self) -> str:
        """
        Export schema to YAML format string.

        Returns:
            YAML-formatted schema string
        """
        return yaml.dump(self.schema, default_flow_style=False, sort_keys=False)

    def save_to_file(self, path: Path) -> None:
        """
        Save schema to YAML file.

        Args:
            path: Output file path
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.export_as_yaml())

    def get_schema_info(self) -> Dict[str, Any]:
        """
        Get schema metadata and statistics.

        Returns:
            Dictionary with schema name, version, stage count, etc.
        """
        stages = self.get_stages()
        total_artifacts = sum(len(s.get('artifacts', [])) for s in stages)
        total_checkpoints = len(self.get_all_checkpoints())

        return {
            'name': self.schema.get('name', 'unknown'),
            'version': self.schema.get('version', 'unknown'),
            'description': self.schema.get('description', ''),
            'stage_count': len(stages),
            'artifact_count': total_artifacts,
            'checkpoint_count': total_checkpoints,
            'stages': [s.get('id') for s in stages]
        }

    @classmethod
    def from_research_type(cls, research_type: str) -> ResearchSchema:
        """
        Create schema from research type name.

        Args:
            research_type: Type of research ('systematic-review', 'meta-analysis', etc.)

        Returns:
            ResearchSchema instance with appropriate default schema

        Raises:
            ValueError: If research type is not recognized
        """
        research_type = research_type.lower()

        if research_type in ('systematic-review', 'systematic_review', 'prisma'):
            return cls(schema_dict=SYSTEMATIC_REVIEW_SCHEMA)
        elif research_type in ('meta-analysis', 'meta_analysis', 'meta'):
            return cls(schema_dict=META_ANALYSIS_SCHEMA)
        else:
            raise ValueError(
                f"Unknown research type: {research_type}. "
                f"Supported types: systematic-review, meta-analysis"
            )
