"""AI Template Engine - LangGraph Orchestrator.

This package provides a LangGraph-based orchestration system for
automated repository analysis and Harness CI/CD setup.

The workflow can be visualized and debugged in LangGraph Studio.
"""

from .graph import graph
from .state import (
    OrchestratorState,
    RepositoryAnalysis,
    ExtractedPatterns,
    GeneratedTemplates,
    HarnessSetupResult,
    DeploymentVerification,
)

__version__ = "0.1.0"

__all__ = [
    "graph",
    "OrchestratorState",
    "RepositoryAnalysis",
    "ExtractedPatterns",
    "GeneratedTemplates",
    "HarnessSetupResult",
    "DeploymentVerification",
]
