"""State definitions for the Harness orchestration workflow.

This module defines the state structure used by the LangGraph workflow
for orchestrating Harness CI/CD setup from repository analysis.
"""

from typing import Annotated, Literal, Optional, TypedDict

from langgraph.graph import add_messages


class RepositoryAnalysis(TypedDict, total=False):
    """Results from repository analysis phase."""

    repo_path: str
    repo_url: Optional[str]
    primary_language: str
    languages: list[str]
    frameworks: list[str]
    build_tools: list[str]
    package_managers: list[str]
    dependencies: dict[str, list[str]]
    entry_points: list[str]
    test_frameworks: list[str]
    dockerfile_present: bool
    docker_compose_present: bool
    kubernetes_manifests: list[str]
    ci_files_present: list[str]
    deployment_patterns: list[str]
    infrastructure_as_code: list[str]
    structure_analysis: str  # Detailed markdown analysis
    complexity_score: int  # 1-10
    confidence_level: float  # 0.0-1.0


class ExtractedPatterns(TypedDict, total=False):
    """Extracted CI/CD patterns and requirements."""

    build_pattern: str  # mono_repo, multi_service, library, container, serverless
    deployment_target: str  # kubernetes, docker, vm, serverless, hybrid
    environments: list[str]  # dev, staging, production, etc.
    deployment_strategy: str  # rolling, blue_green, canary
    test_strategy: dict[str, str]  # unit, integration, e2e
    artifact_types: list[str]  # docker, binary, package, etc.
    secrets_required: list[str]
    connectors_required: list[dict[str, str]]
    infrastructure_requirements: dict[str, list[str]]
    monitoring_patterns: list[str]
    compliance_requirements: list[str]
    recommended_pipeline_stages: list[str]
    confidence_level: float


class GeneratedTemplates(TypedDict, total=False):
    """Generated Harness templates."""

    pipeline_yaml: str
    stages: list[dict[str, str]]
    steps: dict[str, list[dict[str, str]]]
    variables: dict[str, str]
    triggers: list[dict[str, str]]
    input_sets: dict[str, dict[str, str]]
    templates_created: list[str]
    validation_results: dict[str, bool]


class HarnessSetupResult(TypedDict, total=False):
    """Results from Harness platform setup."""

    connectors_created: list[dict[str, str]]
    secrets_created: list[dict[str, str]]
    environments_created: list[dict[str, str]]
    services_created: list[dict[str, str]]
    infrastructure_created: list[dict[str, str]]
    pipeline_created: dict[str, str]
    setup_status: str  # success, partial, failed
    setup_errors: list[str]
    harness_urls: dict[str, str]


class DeploymentVerification(TypedDict, total=False):
    """Results from initial deployment verification."""

    test_execution_id: str
    test_execution_url: str
    execution_status: str  # success, failed, running, aborted
    stages_completed: list[str]
    stages_failed: list[str]
    artifacts_generated: list[str]
    logs_url: str
    verification_passed: bool
    recommendations: list[str]


class OrchestratorState(TypedDict):
    """Main state for the Harness orchestration workflow.

    This state is passed through the entire LangGraph workflow and
    can be visualized in LangGraph Studio.
    """

    # Conversation messages (for LangGraph Studio chat interface)
    messages: Annotated[list, add_messages]

    # Current workflow phase
    current_phase: Literal[
        "init", "analyze", "extract", "generate", "setup", "verify", "complete", "error"
    ]

    # Input configuration
    target_repo_path: str
    target_repo_url: Optional[str]
    harness_org_id: str
    harness_project_id: str

    # Phase results
    repository_analysis: Optional[RepositoryAnalysis]
    extracted_patterns: Optional[ExtractedPatterns]
    generated_templates: Optional[GeneratedTemplates]
    harness_setup: Optional[HarnessSetupResult]
    deployment_verification: Optional[DeploymentVerification]

    # Human-in-the-loop
    hitl_required: bool
    hitl_approved: bool
    hitl_feedback: Optional[str]

    # Error tracking
    errors: list[str]
    warnings: list[str]

    # Metadata
    workflow_id: str
    started_at: str
    completed_at: Optional[str]
    total_duration_seconds: Optional[float]
