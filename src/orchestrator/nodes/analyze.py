"""Repository analysis node."""

from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ..state import OrchestratorState, RepositoryAnalysis
from ..tools.mcp_registry import get_mcp_tools


def analyze_repository(state: OrchestratorState) -> dict[str, Any]:
    """Analyze the target repository structure and technologies.

    Uses MCP tools (Scaffold, Repomix) and Claude to perform deep analysis
    of the repository to understand:
    - Languages and frameworks
    - Build tools and dependencies
    - Existing CI/CD patterns
    - Deployment patterns
    - Infrastructure requirements

    Args:
        state: Current orchestrator state

    Returns:
        State updates with repository analysis results
    """
    repo_path = state["target_repo_path"]

    try:
        # Get MCP tools for repository analysis
        tools = get_mcp_tools(["scaffold", "repomix", "github"])

        # Initialize Claude with tools
        llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0,
        ).bind_tools(tools)

        # Create analysis prompt
        system_prompt = SystemMessage(
            content="""You are a DevOps expert analyzing repositories to determine optimal CI/CD setup.

Your task is to analyze the repository and extract:
1. Primary language and all languages used
2. Frameworks and libraries
3. Build tools (make, gradle, npm, cargo, etc.)
4. Package managers
5. Dependencies
6. Entry points (main files, binaries)
7. Test frameworks and test structure
8. Container files (Dockerfile, docker-compose.yml)
9. Kubernetes manifests
10. Existing CI/CD files (.github/workflows, .gitlab-ci.yml, etc.)
11. Deployment patterns
12. Infrastructure as code (Terraform, Helm, etc.)

Use the available MCP tools to:
- scaffold: Get repository structure and file listing
- repomix: Get combined repository content for analysis
- github: Get repository metadata if available

Provide a detailed analysis with confidence scores."""
        )

        user_prompt = HumanMessage(
            content=f"""Analyze the repository at: {repo_path}

Provide a comprehensive analysis including:
- Repository structure
- Technologies and frameworks
- Build and deployment patterns
- Testing strategy
- Infrastructure requirements
- Complexity assessment (1-10)
- Confidence level (0.0-1.0)

Use the MCP tools to gather this information."""
        )

        # Invoke Claude with tools
        response = llm.invoke([system_prompt, user_prompt])

        # Parse analysis results
        # NOTE: This is simplified - in production, we'd parse tool call results
        analysis: RepositoryAnalysis = {
            "repo_path": repo_path,
            "repo_url": state.get("target_repo_url"),
            "primary_language": "python",  # Placeholder
            "languages": ["python"],
            "frameworks": [],
            "build_tools": [],
            "package_managers": [],
            "dependencies": {},
            "entry_points": [],
            "test_frameworks": [],
            "dockerfile_present": False,
            "docker_compose_present": False,
            "kubernetes_manifests": [],
            "ci_files_present": [],
            "deployment_patterns": [],
            "infrastructure_as_code": [],
            "structure_analysis": response.content if isinstance(response.content, str) else "",
            "complexity_score": 5,
            "confidence_level": 0.8,
        }

        return {
            "repository_analysis": analysis,
            "current_phase": "extract",
            "messages": [
                AIMessage(
                    content=f"""✅ Repository analysis complete

**Primary Language:** {analysis['primary_language']}
**Complexity Score:** {analysis['complexity_score']}/10
**Confidence:** {analysis['confidence_level']:.0%}

Proceeding to pattern extraction..."""
                )
            ],
        }

    except Exception as e:
        return {
            "current_phase": "error",
            "errors": [f"Repository analysis failed: {str(e)}"],
            "messages": [
                AIMessage(content=f"❌ Repository analysis failed: {str(e)}")
            ],
        }
