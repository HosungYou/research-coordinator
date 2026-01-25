#!/usr/bin/env python3
"""
Tests for Agent Contract Validator
===================================

Tests the validation logic for SKILL.md files.

Usage:
    python3 tests/test_validate_agents.py
    # or with pytest if installed:
    pytest tests/test_validate_agents.py -v
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_agents import ContractValidator, ValidationResult


class TestValidationResult(unittest.TestCase):
    """Tests for ValidationResult dataclass."""

    def test_valid_result_str(self):
        """Valid result shows PASS with checkmark."""
        result = ValidationResult(agent_name="test-agent", is_valid=True)
        self.assertIn("PASS", str(result))
        self.assertIn("test-agent", str(result))

    def test_invalid_result_str(self):
        """Invalid result shows FAIL with X."""
        result = ValidationResult(agent_name="test-agent", is_valid=False)
        self.assertIn("FAIL", str(result))

    def test_result_with_errors(self):
        """Result can store errors."""
        result = ValidationResult(
            agent_name="test-agent",
            is_valid=False,
            errors=["Error 1", "Error 2"]
        )
        self.assertEqual(len(result.errors), 2)
        self.assertIn("Error 1", result.errors)


class TestYamlParser(unittest.TestCase):
    """Tests for the simple YAML parser."""

    def create_validator_with_content(self, content: str) -> ContractValidator:
        """Helper to create a validator with specific content."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.md', delete=False, encoding='utf-8'
        ) as f:
            f.write(content)
            temp_path = Path(f.name)

        validator = ContractValidator(temp_path)
        validator.content = content
        return validator

    def test_simple_key_value(self):
        """Parser handles simple key-value pairs."""
        content = """---
name: test-agent
version: "1.0.0"
description: A test agent
---
# Content
"""
        validator = self.create_validator_with_content(content)
        validator._parse_frontmatter()

        self.assertEqual(validator.frontmatter["name"], "test-agent")
        self.assertEqual(validator.frontmatter["version"], "1.0.0")
        self.assertEqual(validator.frontmatter["description"], "A test agent")

    def test_boolean_values(self):
        """Parser handles boolean values."""
        content = """---
name: test
enabled: true
disabled: false
---
"""
        validator = self.create_validator_with_content(content)
        validator._parse_frontmatter()

        self.assertTrue(validator.frontmatter["enabled"])
        self.assertFalse(validator.frontmatter["disabled"])

    def test_inline_list(self):
        """Parser handles inline lists."""
        content = """---
name: test
items: [one, two, three]
---
"""
        validator = self.create_validator_with_content(content)
        validator._parse_frontmatter()

        self.assertEqual(validator.frontmatter["items"], ["one", "two", "three"])

    def test_nested_object(self):
        """Parser handles nested objects."""
        content = """---
name: test
v3_integration:
  dynamic_t_score: true
  mode: enhanced
---
"""
        validator = self.create_validator_with_content(content)
        validator._parse_frontmatter()

        self.assertIn("v3_integration", validator.frontmatter)
        v3 = validator.frontmatter["v3_integration"]
        self.assertTrue(v3["dynamic_t_score"])
        self.assertEqual(v3["mode"], "enhanced")

    def test_nested_list(self):
        """Parser handles lists under nested keys."""
        content = """---
name: test
v3_integration:
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
---
"""
        validator = self.create_validator_with_content(content)
        validator._parse_frontmatter()

        v3 = validator.frontmatter["v3_integration"]
        self.assertIn("creativity_modules", v3)
        self.assertEqual(len(v3["creativity_modules"]), 3)
        self.assertIn("forced-analogy", v3["creativity_modules"])

    def test_multiline_string(self):
        """Parser handles multiline strings."""
        content = """---
name: test
description: |
  This is a multiline
  description string
---
"""
        validator = self.create_validator_with_content(content)
        validator._parse_frontmatter()

        self.assertIn("multiline", validator.frontmatter["description"])

    def test_no_frontmatter(self):
        """Parser handles missing frontmatter."""
        content = "# Just markdown content"
        validator = self.create_validator_with_content(content)
        validator._parse_frontmatter()

        self.assertGreater(len(validator.result.errors), 0)
        self.assertIn("frontmatter", validator.result.errors[0].lower())


class TestContractValidation(unittest.TestCase):
    """Tests for contract validation rules."""

    def create_temp_skill_file(self, content: str) -> Path:
        """Create a temporary SKILL.md file."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.md', delete=False, encoding='utf-8'
        ) as f:
            f.write(content)
            return Path(f.name)

    def test_valid_enhanced_agent(self):
        """Valid ENHANCED agent passes validation."""
        content = """---
name: test-agent
version: "1.0.0"
description: A test agent
upgrade_level: ENHANCED
v3_integration:
  dynamic_t_score: false
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
  checkpoints:
    - CP-INIT-001
    - CP-VS-001
    - CP-VS-002
---
## Overview
This is a test agent.
"""
        path = self.create_temp_skill_file(content)
        validator = ContractValidator(path)
        result = validator.validate()

        self.assertTrue(result.is_valid, f"Errors: {result.errors}")

    def test_valid_full_agent(self):
        """Valid FULL agent passes validation."""
        content = """---
name: test-agent
version: "1.0.0"
description: A test agent
upgrade_level: FULL
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
    - temporal-reframing
    - community-simulation
  checkpoints:
    - CP-INIT-001
    - CP-VS-001
    - CP-VS-002
    - CP-VS-003
    - CP-VS-004
    - CP-EXEC-001
---
## Overview
This is a FULL VS agent.

## T-Score System
Details about T-Score here.
"""
        path = self.create_temp_skill_file(content)
        validator = ContractValidator(path)
        result = validator.validate()

        self.assertTrue(result.is_valid, f"Errors: {result.errors}")

    def test_missing_required_field(self):
        """Missing required field causes validation failure."""
        content = """---
name: test-agent
version: "1.0.0"
description: A test agent
---
# Content
"""
        path = self.create_temp_skill_file(content)
        validator = ContractValidator(path)
        result = validator.validate()

        self.assertFalse(result.is_valid)
        self.assertTrue(any("upgrade_level" in err for err in result.errors))

    def test_invalid_upgrade_level(self):
        """Invalid upgrade_level causes validation failure."""
        content = """---
name: test-agent
version: "1.0.0"
description: A test agent
upgrade_level: INVALID
v3_integration:
  dynamic_t_score: false
---
# Content
"""
        path = self.create_temp_skill_file(content)
        validator = ContractValidator(path)
        result = validator.validate()

        self.assertFalse(result.is_valid)
        self.assertTrue(any("INVALID" in err for err in result.errors))

    def test_full_without_dynamic_t_score(self):
        """FULL agent without dynamic_t_score causes error."""
        content = """---
name: test-agent
version: "1.0.0"
description: A test agent
upgrade_level: FULL
v3_integration:
  dynamic_t_score: false
---
# Content
"""
        path = self.create_temp_skill_file(content)
        validator = ContractValidator(path)
        result = validator.validate()

        self.assertFalse(result.is_valid)
        self.assertTrue(any("dynamic_t_score" in err for err in result.errors))

    def test_invalid_version_format(self):
        """Non-semver version causes warning."""
        content = """---
name: test-agent
version: "1.0"
description: A test agent
upgrade_level: LIGHT
v3_integration:
  dynamic_t_score: false
---
# Content
"""
        path = self.create_temp_skill_file(content)
        validator = ContractValidator(path)
        result = validator.validate()

        # Should pass but with warning
        self.assertTrue(result.is_valid)
        self.assertTrue(any("semantic versioning" in warn for warn in result.warnings))


class TestCheckpointPattern(unittest.TestCase):
    """Tests for checkpoint naming pattern."""

    def test_valid_checkpoint_patterns(self):
        """Valid checkpoint patterns are recognized."""
        validator = ContractValidator(Path("/fake/path"))

        valid_patterns = [
            "CP-INIT-001",
            "CP-VS-002",
            "CP_EXEC_003",
            "cp-test-100",
        ]

        for pattern in valid_patterns:
            self.assertIsNotNone(
                validator.CHECKPOINT_PATTERN.match(pattern),
                f"Should match: {pattern}"
            )

    def test_invalid_checkpoint_patterns(self):
        """Invalid checkpoint patterns are rejected."""
        validator = ContractValidator(Path("/fake/path"))

        invalid_patterns = [
            "CHECKPOINT-001",
            "CP001",
            "CP-INIT",
            "CP-INIT-1",  # Not 3 digits
        ]

        for pattern in invalid_patterns:
            self.assertIsNone(
                validator.CHECKPOINT_PATTERN.match(pattern),
                f"Should not match: {pattern}"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
