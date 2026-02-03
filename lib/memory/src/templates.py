"""
Diverga Memory System v7.0 - Template Engine

This module provides a flexible template rendering system for generating
research artifacts, protocols, and documentation with context substitution.

Author: Diverga Project
Version: 7.0.0
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class TemplateEngine:
    """
    Template engine for rendering research artifacts with context substitution.

    Supports:
    - {{ variable }} syntax for simple substitution
    - {% for item in items %} ... {% endfor %} for loops
    - {% if condition %} ... {% endif %} for conditionals
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize template engine.

        Args:
            templates_dir: Directory containing template files (optional)
        """
        self.templates_dir = templates_dir
        self._templates: Dict[str, str] = {}

        # Register built-in templates
        self._register_builtin_templates()

    def load_template(self, template_name: str) -> str:
        """
        Load template content from file.

        Args:
            template_name: Name of template file (without path)

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        if self.templates_dir is None:
            raise ValueError("templates_dir not set - cannot load from file")

        template_path = self.templates_dir / f"{template_name}.md"

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        return template_path.read_text(encoding='utf-8')

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render template with context variables.

        Args:
            template_name: Template name (from file or registered)
            context: Dictionary of variables to substitute

        Returns:
            Rendered template content

        Raises:
            ValueError: If template not found
        """
        # Try registered templates first
        if template_name in self._templates:
            template_content = self._templates[template_name]
        else:
            # Try loading from file
            template_content = self.load_template(template_name)

        # Process template
        rendered = self._process_template(template_content, context)
        return rendered

    def register_template(self, name: str, content: str) -> None:
        """
        Register an in-memory template.

        Args:
            name: Template identifier
            content: Template content
        """
        self._templates[name] = content

    def list_templates(self) -> List[str]:
        """
        List available templates.

        Returns:
            List of template names (registered + files in templates_dir)
        """
        templates = list(self._templates.keys())

        # Add file-based templates if directory exists
        if self.templates_dir and self.templates_dir.exists():
            for path in self.templates_dir.glob("*.md"):
                templates.append(path.stem)

        return sorted(set(templates))

    def get_template_variables(self, template_name: str) -> List[str]:
        """
        Extract variable names from template.

        Args:
            template_name: Template identifier

        Returns:
            List of variable names found in template
        """
        # Get template content
        if template_name in self._templates:
            content = self._templates[template_name]
        else:
            content = self.load_template(template_name)

        # Find all {{ variable }} patterns
        variables = re.findall(r'\{\{\s*(\w+(?:\.\w+)*)\s*\}\}', content)

        # Find variables in for loops: {% for item in items %}
        for_vars = re.findall(r'\{%\s*for\s+\w+\s+in\s+(\w+)\s*%\}', content)
        variables.extend(for_vars)

        # Find variables in if conditions: {% if condition %}
        if_vars = re.findall(r'\{%\s*if\s+(\w+)\s*%\}', content)
        variables.extend(if_vars)

        return sorted(set(variables))

    def _process_template(self, template: str, context: Dict[str, Any]) -> str:
        """
        Process template with context substitution.

        Args:
            template: Template content
            context: Substitution context

        Returns:
            Rendered content
        """
        result = template

        # Process for loops: {% for item in items %} ... {% endfor %}
        result = self._process_for_loops(result, context)

        # Process conditionals: {% if condition %} ... {% endif %}
        result = self._process_conditionals(result, context)

        # Process simple variable substitution: {{ variable }}
        result = self._process_variables(result, context)

        return result

    def _process_variables(self, template: str, context: Dict[str, Any]) -> str:
        """Process {{ variable }} substitutions."""
        def replace_var(match):
            var_name = match.group(1).strip()
            # Support nested access like {{ obj.property }}
            value = self._get_nested_value(context, var_name)
            return str(value) if value is not None else ""

        return re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_var, template)

    def _process_for_loops(self, template: str, context: Dict[str, Any]) -> str:
        """Process {% for item in items %} loops."""
        pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'

        def replace_loop(match):
            item_var = match.group(1)
            list_var = match.group(2)
            loop_body = match.group(3)

            items = context.get(list_var, [])
            if not isinstance(items, list):
                return ""

            results = []
            for item in items:
                # Create context with loop variable
                loop_context = context.copy()
                loop_context[item_var] = item
                # Recursively process the loop body
                processed = self._process_template(loop_body, loop_context)
                results.append(processed)

            return "\n".join(results)

        return re.sub(pattern, replace_loop, template, flags=re.DOTALL)

    def _process_conditionals(self, template: str, context: Dict[str, Any]) -> str:
        """Process {% if condition %} conditionals."""
        pattern = r'\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}'

        def replace_condition(match):
            condition_var = match.group(1)
            content = match.group(2)

            # Evaluate condition (truthy check)
            condition_value = context.get(condition_var, False)
            if self._is_truthy(condition_value):
                return self._process_template(content, context)
            return ""

        return re.sub(pattern, replace_condition, template, flags=re.DOTALL)

    def _get_nested_value(self, context: Dict[str, Any], key: str) -> Any:
        """
        Get nested value from context using dot notation.

        Example: "project.name" -> context["project"]["name"]
        """
        parts = key.split('.')
        value = context

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                return None

            if value is None:
                return None

        return value

    def _is_truthy(self, value: Any) -> bool:
        """Check if value is truthy."""
        if value is None or value is False:
            return False
        if isinstance(value, (list, dict, str)):
            return len(value) > 0
        return bool(value)

    def _register_builtin_templates(self) -> None:
        """Register built-in templates."""
        self.register_template("protocol", PROTOCOL_TEMPLATE)
        self.register_template("search_strategy", SEARCH_STRATEGY_TEMPLATE)
        self.register_template("inclusion_criteria", INCLUSION_CRITERIA_TEMPLATE)
        self.register_template("prisma_stage", PRISMA_STAGE_TEMPLATE)


# Built-in template constants

PROTOCOL_TEMPLATE = """# Research Protocol: {{ project_name }}

## Research Question
{{ research_question }}

## Paradigm
{{ paradigm }}

## Current Stage
{{ current_stage }}

## Objectives
{% for objective in objectives %}
- {{ objective }}
{% endfor %}

## Methodology
{{ methodology }}

{% if inclusion_criteria %}
## Inclusion Criteria
{% for criterion in inclusion_criteria %}
- {{ criterion }}
{% endfor %}
{% endif %}

{% if exclusion_criteria %}
## Exclusion Criteria
{% for criterion in exclusion_criteria %}
- {{ criterion }}
{% endfor %}
{% endif %}

## Timeline
Created: {{ created_at }}
Last Updated: {{ updated_at }}
"""

SEARCH_STRATEGY_TEMPLATE = """# Literature Search Strategy

## Research Question
{{ research_question }}

## Databases
{% for database in databases %}
- {{ database }}
{% endfor %}

## Search Terms
### Primary Concepts
{% for term in primary_terms %}
- {{ term }}
{% endfor %}

### Boolean Query
```
{{ boolean_query }}
```

## Date Range
From: {{ date_from }}
To: {{ date_to }}

## Language
{{ language }}

## Expected Results
Estimated papers: {{ estimated_count }}

## Notes
{{ notes }}
"""

INCLUSION_CRITERIA_TEMPLATE = """# Inclusion/Exclusion Criteria

## Research Question
{{ research_question }}

## Inclusion Criteria
{% for criterion in inclusion_criteria %}
### {{ criterion.category }}
- **Description**: {{ criterion.description }}
- **Rationale**: {{ criterion.rationale }}
{% endfor %}

## Exclusion Criteria
{% for criterion in exclusion_criteria %}
### {{ criterion.category }}
- **Description**: {{ criterion.description }}
- **Rationale**: {{ criterion.rationale }}
{% endfor %}

## Decision Rules
{% for rule in decision_rules %}
- {{ rule }}
{% endfor %}

## Inter-Rater Reliability
Target Cohen's Kappa: {{ target_kappa }}
"""

PRISMA_STAGE_TEMPLATE = """# PRISMA Stage Report: {{ stage_name }}

## Stage Overview
**Stage**: {{ stage_name }}
**Date**: {{ date }}

## Input
Papers entering this stage: {{ input_count }}

## Process
{{ process_description }}

## Results
Papers passing criteria: {{ output_count }}
Papers excluded: {{ excluded_count }}

## Exclusion Reasons
{% for reason in exclusion_reasons %}
- **{{ reason.category }}**: {{ reason.count }} papers
  - Details: {{ reason.details }}
{% endfor %}

## Quality Checks
{% for check in quality_checks %}
- {{ check.name }}: {{ check.result }}
{% endfor %}

## Next Stage
{{ next_stage }}

## Notes
{{ notes }}
"""
