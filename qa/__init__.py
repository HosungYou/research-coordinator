"""
Diverga QA Framework
====================

Comprehensive testing framework for Diverga plugin's agentic AI research assistant.

Modules:
- protocol: Test scenario definitions, metrics, and grading rubrics
- runners: Execution engines for simulation and validation

Features:
- Checkpoint compliance testing (REQUIRED/RECOMMENDED/OPTIONAL)
- Agent invocation accuracy tracking
- VS Methodology quality evaluation
- Context persistence verification
"""

__version__ = "1.0.0"
__author__ = "Diverga Research Team"

from pathlib import Path

# Package paths
PACKAGE_DIR = Path(__file__).parent
PROTOCOL_DIR = PACKAGE_DIR / "protocol"
RUNNERS_DIR = PACKAGE_DIR / "runners"
REPORTS_DIR = PACKAGE_DIR / "reports"

# Ensure reports directory exists
REPORTS_DIR.mkdir(exist_ok=True)
