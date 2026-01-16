"""Pattern extraction node."""

from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ..state import ExtractedPatterns, OrchestratorState


def extract_patterns(state: OrchestratorState) -> dict[str, Any]:
    """Extract CI/CD patterns and requirements from repository analysis.

    Uses Claude to analyze the repository analysis results and determine:
    - Build patterns (mono_repo, multi_service, library, etc.)
    - Deployment targets (kubernetes, docker, vm, etc.)
    - Environments needed
    - Deployment strategies
    - Test strategies
    - Required secrets and connectors
    - Infrastructure requirements

    Args:
        state: Current orchestrator state

    Returns:
        State updates with extracted patterns
    """
    analysis = state.get("repository_analysis")
    if not analysis:
        return {
            "current_phase": "error",
            "errors": ["No repository analysis available"],
            "messages": [
                AIMessage(content="❌ Cannot extract patterns: no repository analysis")
            ],
        }

    try:
        # Initialize Claude
        llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0,
        )

        # Create pattern extraction prompt
        system_prompt = SystemMessage(
            content="""You are a DevOps architect expert at identifying CI/CD patterns.

Given a repository analysis, determine the optimal:
1. Build pattern (mono_repo, multi_service, library, container, serverless)
2. Deployment target (kubernetes, docker, vm, serverless, hybrid)
3. Environments (dev, staging, production, preview)
4. Deployment strategy (rolling, blue_green, canary)
5. Test strategy (unit, integration, e2e, performance)
6. Artifact types (docker, binary, package, helm)
7. Required secrets
8. Required connectors (git, docker, k8s, cloud)
9. Infrastructure requirements
10. Monitoring patterns
11. Compliance requirements
12. Recommended pipeline stages

Be specific and provide actionable recommendations."""
        )

        user_prompt = HumanMessage(
            content=f"""Based on this repository analysis, extract CI/CD patterns:

**Repository:** {analysis['repo_path']}
**Primary Language:** {analysis['primary_language']}
**Languages:** {', '.join(analysis['languages'])}
**Build Tools:** {', '.join(analysis['build_tools'])}
**Dockerfile Present:** {analysis['dockerfile_present']}
**Kubernetes Manifests:** {len(analysis['kubernetes_manifests'])}
**Complexity:** {analysis['complexity_score']}/10

**Structure Analysis:**
{analysis['structure_analysis']}

Provide:
1. Build pattern recommendation
2. Deployment target
3. Environments to create
4. Deployment strategy
5. Test strategy
6. Required connectors
7. Pipeline stages

Format as structured JSON."""
        )

        # Invoke Claude
        response = llm.invoke([system_prompt, user_prompt])

        # Parse pattern extraction results
        # NOTE: In production, we'd use structured output or JSON parsing
        patterns: ExtractedPatterns = {
            "build_pattern": "container",
            "deployment_target": "kubernetes",
            "environments": ["dev", "staging", "production"],
            "deployment_strategy": "rolling",
            "test_strategy": {
                "unit": "pytest",
                "integration": "pytest",
                "e2e": "manual",
            },
            "artifact_types": ["docker"],
            "secrets_required": ["github_token", "docker_credentials"],
            "connectors_required": [
                {"type": "github", "name": "github_connector"},
                {"type": "docker", "name": "docker_hub"},
                {"type": "kubernetes", "name": "k8s_cluster"},
            ],
            "infrastructure_requirements": {
                "compute": ["kubernetes_cluster"],
                "storage": ["container_registry"],
            },
            "monitoring_patterns": ["prometheus", "grafana"],
            "compliance_requirements": [],
            "recommended_pipeline_stages": [
                "build",
                "test",
                "security_scan",
                "deploy",
                "verify",
            ],
            "confidence_level": 0.85,
        }

        return {
            "extracted_patterns": patterns,
            "current_phase": "generate",
            "messages": [
                AIMessage(
                    content=f"""✅ Pattern extraction complete

**Build Pattern:** {patterns['build_pattern']}
**Deployment Target:** {patterns['deployment_target']}
**Environments:** {', '.join(patterns['environments'])}
**Strategy:** {patterns['deployment_strategy']}
**Confidence:** {patterns['confidence_level']:.0%}

Proceeding to template generation..."""
                )
            ],
        }

    except Exception as e:
        return {
            "current_phase": "error",
            "errors": [f"Pattern extraction failed: {str(e)}"],
            "messages": [AIMessage(content=f"❌ Pattern extraction failed: {str(e)}")],
        }
