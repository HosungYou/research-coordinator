"""
Diverga Memory System v7.0 - Artifact Generator

This module generates research artifacts (protocols, reports, documentation)
from templates with dependency management and validation.

Author: Diverga Project
Version: 7.0.0
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import json
import yaml

try:
    from .templates import TemplateEngine
except ImportError:
    from templates import TemplateEngine


class ResearchSchema:
    """
    Schema definition for research artifacts with dependency tracking.

    Defines:
    - Available artifacts and their dependencies
    - Template mappings
    - Generation rules
    - Validation requirements
    """

    def __init__(self, schema_file: Optional[Path] = None):
        """
        Initialize research schema.

        Args:
            schema_file: Path to YAML schema definition (optional)
        """
        self.artifacts: Dict[str, Dict[str, Any]] = {}

        if schema_file and schema_file.exists():
            self._load_schema(schema_file)
        else:
            self._load_default_schema()

    def _load_schema(self, schema_file: Path) -> None:
        """Load schema from YAML file."""
        with open(schema_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            self.artifacts = data.get('artifacts', {})

    def _load_default_schema(self) -> None:
        """Load default artifact schema."""
        self.artifacts = {
            'research_protocol': {
                'name': 'Research Protocol',
                'template': 'protocol',
                'generates': 'protocol.md',
                'depends_on': [],
                'required_context': [
                    'project_name',
                    'research_question',
                    'paradigm',
                    'current_stage'
                ]
            },
            'search_strategy': {
                'name': 'Literature Search Strategy',
                'template': 'search_strategy',
                'generates': 'search_strategy.md',
                'depends_on': ['research_protocol'],
                'required_context': [
                    'research_question',
                    'databases',
                    'primary_terms',
                    'boolean_query'
                ]
            },
            'inclusion_criteria': {
                'name': 'Inclusion/Exclusion Criteria',
                'template': 'inclusion_criteria',
                'generates': 'inclusion_criteria.md',
                'depends_on': ['research_protocol'],
                'required_context': [
                    'research_question',
                    'inclusion_criteria',
                    'exclusion_criteria'
                ]
            },
            'prisma_stage_report': {
                'name': 'PRISMA Stage Report',
                'template': 'prisma_stage',
                'generates': 'prisma_stage_{stage_name}.md',
                'depends_on': ['search_strategy', 'inclusion_criteria'],
                'required_context': [
                    'stage_name',
                    'input_count',
                    'output_count',
                    'process_description'
                ]
            }
        }

    def get_artifact(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """Get artifact definition by ID."""
        return self.artifacts.get(artifact_id)

    def list_artifacts(self) -> List[str]:
        """List all artifact IDs."""
        return list(self.artifacts.keys())


class ArtifactGenerator:
    """
    Generator for research artifacts with dependency tracking and validation.
    """

    def __init__(
        self,
        project_root: Path,
        schema: ResearchSchema,
        templates: TemplateEngine
    ):
        """
        Initialize artifact generator.

        Args:
            project_root: Root directory of research project
            schema: Research schema with artifact definitions
            templates: Template engine for rendering
        """
        self.project_root = Path(project_root)
        self.schema = schema
        self.templates = templates

        # Initialize output directories
        self.changes_dir = self.project_root / ".research" / "changes" / "current"
        self.changes_dir.mkdir(parents=True, exist_ok=True)

        # Track generated artifacts
        self.status_file = self.changes_dir / ".artifact_status.json"
        self._load_status()

    def generate(self, artifact_id: str, context: Optional[Dict[str, Any]] = None) -> Path:
        """
        Generate artifact from template.

        Args:
            artifact_id: Artifact identifier
            context: Override context (if not provided, loads from project state)

        Returns:
            Path to generated artifact file

        Raises:
            ValueError: If artifact not found or dependencies missing
            KeyError: If required context variables missing
        """
        # Get artifact definition
        artifact = self.schema.get_artifact(artifact_id)
        if not artifact:
            raise ValueError(f"Unknown artifact: {artifact_id}")

        # Check dependencies
        dependencies_met, missing = self.check_dependencies(artifact_id)
        if not dependencies_met:
            raise ValueError(
                f"Cannot generate '{artifact_id}': missing dependencies {missing}"
            )

        # Load research context
        if context is None:
            context = self._load_research_context()

        # Validate required context variables
        self._validate_context(artifact, context)

        # Render template
        template_name = artifact['template']
        rendered_content = self.templates.render(template_name, context)

        # Determine output filename
        output_filename = artifact['generates']
        # Support dynamic filenames like "prisma_stage_{stage_name}.md"
        output_filename = output_filename.format(**context)

        # Write to file
        output_path = self.changes_dir / output_filename
        output_path.write_text(rendered_content, encoding='utf-8')

        # Update status
        self._mark_generated(artifact_id, output_path)

        return output_path

    def check_dependencies(self, artifact_id: str) -> Tuple[bool, List[str]]:
        """
        Check if all required dependencies are met.

        Args:
            artifact_id: Artifact to check

        Returns:
            Tuple of (all_met, missing_dependencies)
        """
        artifact = self.schema.get_artifact(artifact_id)
        if not artifact:
            return False, [f"Unknown artifact: {artifact_id}"]

        depends_on = artifact.get('depends_on', [])
        missing = []

        for dep in depends_on:
            if dep not in self.generated_artifacts:
                missing.append(dep)

        return len(missing) == 0, missing

    def get_unlocked_artifacts(self) -> List[str]:
        """
        Get artifacts that can now be generated.

        Returns:
            List of artifact IDs ready for generation
        """
        unlocked = []

        for artifact_id in self.schema.list_artifacts():
            # Skip already generated
            if artifact_id in self.generated_artifacts:
                continue

            # Check if dependencies met
            dependencies_met, _ = self.check_dependencies(artifact_id)
            if dependencies_met:
                unlocked.append(artifact_id)

        return unlocked

    def get_generation_status(self) -> Dict[str, List[str]]:
        """
        Get status of all artifacts.

        Returns:
            Dictionary with 'generated', 'pending', and 'blocked' lists
        """
        all_artifacts = self.schema.list_artifacts()
        generated = list(self.generated_artifacts.keys())
        unlocked = self.get_unlocked_artifacts()

        # Blocked = not generated and not unlocked
        blocked = [
            aid for aid in all_artifacts
            if aid not in generated and aid not in unlocked
        ]

        return {
            'generated': generated,
            'pending': unlocked,
            'blocked': blocked
        }

    def regenerate(
        self,
        artifact_id: str,
        context: Optional[Dict[str, Any]] = None,
        force: bool = False
    ) -> Path:
        """
        Regenerate existing artifact.

        Args:
            artifact_id: Artifact to regenerate
            context: Override context (if not provided, loads from project state)
            force: If True, regenerate even if dependencies changed

        Returns:
            Path to regenerated artifact

        Raises:
            ValueError: If force=False and dependencies not met
        """
        if not force:
            dependencies_met, missing = self.check_dependencies(artifact_id)
            if not dependencies_met:
                raise ValueError(
                    f"Cannot regenerate '{artifact_id}': dependencies changed. "
                    f"Missing: {missing}. Use force=True to override."
                )

        # Remove from generated list to allow re-generation
        if artifact_id in self.generated_artifacts:
            del self.generated_artifacts[artifact_id]
            self._save_status()

        return self.generate(artifact_id, context)

    def _load_research_context(self) -> Dict[str, Any]:
        """
        Load research context from project state files.

        Returns:
            Dictionary of context variables
        """
        context = {}

        # Load from project-state.yaml
        state_file = self.project_root / ".research" / "project-state.yaml"
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = yaml.safe_load(f)
                context.update(state_data)

        # Load from decision-log.yaml
        decision_file = self.project_root / ".research" / "decision-log.yaml"
        if decision_file.exists():
            with open(decision_file, 'r', encoding='utf-8') as f:
                decision_data = yaml.safe_load(f)
                # Extract key decisions into context
                if 'decisions' in decision_data:
                    context['decisions'] = decision_data['decisions']

        # Add timestamp
        context['generated_at'] = datetime.utcnow().isoformat()

        return context

    def _validate_context(self, artifact: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        Validate that all required context variables are present.

        Args:
            artifact: Artifact definition
            context: Context dictionary

        Raises:
            KeyError: If required variables missing
        """
        required = artifact.get('required_context', [])
        missing = []

        for key in required:
            # Support nested keys like "project.name"
            if '.' in key:
                parts = key.split('.')
                value = context
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        missing.append(key)
                        break
            else:
                if key not in context:
                    missing.append(key)

        if missing:
            raise KeyError(
                f"Missing required context variables for '{artifact['name']}': {missing}"
            )

    def _load_status(self) -> None:
        """Load artifact generation status."""
        if self.status_file.exists():
            with open(self.status_file, 'r', encoding='utf-8') as f:
                self.generated_artifacts = json.load(f)
        else:
            self.generated_artifacts = {}

    def _save_status(self) -> None:
        """Save artifact generation status."""
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(self.generated_artifacts, f, indent=2)

    def _mark_generated(self, artifact_id: str, output_path: Path) -> None:
        """Mark artifact as generated."""
        self.generated_artifacts[artifact_id] = {
            'path': str(output_path.relative_to(self.project_root)),
            'generated_at': datetime.utcnow().isoformat()
        }
        self._save_status()
