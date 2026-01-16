"""Tests for state definitions."""

from orchestrator.state import (
    OrchestratorState,
    RepositoryAnalysis,
    ExtractedPatterns,
)


def test_orchestrator_state_creation():
    """Test creating an OrchestratorState."""
    state: OrchestratorState = {
        "messages": [],
        "current_phase": "init",
        "target_repo_path": "/test/repo",
        "target_repo_url": "https://github.com/test/repo",
        "harness_org_id": "test-org",
        "harness_project_id": "test-project",
        "repository_analysis": None,
        "extracted_patterns": None,
        "generated_templates": None,
        "harness_setup": None,
        "deployment_verification": None,
        "hitl_required": True,
        "hitl_approved": False,
        "hitl_feedback": None,
        "errors": [],
        "warnings": [],
        "workflow_id": "test-workflow-123",
        "started_at": "2024-01-01T00:00:00Z",
        "completed_at": None,
        "total_duration_seconds": None,
    }

    assert state["current_phase"] == "init"
    assert state["target_repo_path"] == "/test/repo"
    assert state["hitl_required"] is True


def test_repository_analysis_creation():
    """Test creating a RepositoryAnalysis."""
    analysis: RepositoryAnalysis = {
        "repo_path": "/test/repo",
        "repo_url": "https://github.com/test/repo",
        "primary_language": "python",
        "languages": ["python", "yaml"],
        "frameworks": ["django"],
        "build_tools": ["pip"],
        "package_managers": ["pip"],
        "dependencies": {"python": ["django", "pytest"]},
        "entry_points": ["manage.py"],
        "test_frameworks": ["pytest"],
        "dockerfile_present": True,
        "docker_compose_present": False,
        "kubernetes_manifests": [],
        "ci_files_present": [],
        "deployment_patterns": ["container"],
        "infrastructure_as_code": [],
        "structure_analysis": "Test analysis",
        "complexity_score": 5,
        "confidence_level": 0.9,
    }

    assert analysis["primary_language"] == "python"
    assert analysis["complexity_score"] == 5
    assert analysis["confidence_level"] == 0.9


def test_extracted_patterns_creation():
    """Test creating ExtractedPatterns."""
    patterns: ExtractedPatterns = {
        "build_pattern": "container",
        "deployment_target": "kubernetes",
        "environments": ["dev", "prod"],
        "deployment_strategy": "rolling",
        "test_strategy": {"unit": "pytest"},
        "artifact_types": ["docker"],
        "secrets_required": ["api_key"],
        "connectors_required": [{"type": "github", "name": "gh_conn"}],
        "infrastructure_requirements": {"compute": ["k8s"]},
        "monitoring_patterns": ["prometheus"],
        "compliance_requirements": [],
        "recommended_pipeline_stages": ["build", "test", "deploy"],
        "confidence_level": 0.85,
    }

    assert patterns["build_pattern"] == "container"
    assert patterns["deployment_target"] == "kubernetes"
    assert len(patterns["environments"]) == 2
