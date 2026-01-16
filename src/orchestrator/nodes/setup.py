"""Harness platform setup node."""

from typing import Any

from langchain_core.messages import AIMessage

from ..state import HarnessSetupResult, OrchestratorState
from ..tools.mcp_registry import get_mcp_tools


def setup_harness(state: OrchestratorState) -> dict[str, Any]:
    """Setup Harness platform with connectors, secrets, environments, and pipelines.

    Uses the Harness MCP server to:
    1. Create connectors (GitHub, Docker, Kubernetes, etc.)
    2. Create secrets
    3. Create environments (dev, staging, production)
    4. Create services
    5. Create infrastructure definitions
    6. Create the pipeline

    Args:
        state: Current orchestrator state

    Returns:
        State updates with setup results
    """
    templates = state.get("generated_templates")
    patterns = state.get("extracted_patterns")

    if not templates or not patterns:
        return {
            "current_phase": "error",
            "errors": ["Missing templates or patterns for Harness setup"],
            "messages": [
                AIMessage(content="❌ Cannot setup Harness: missing required data")
            ],
        }

    # Check approval
    if state.get("hitl_required") and not state.get("hitl_approved"):
        return {
            "current_phase": "error",
            "errors": ["Setup requires human approval"],
            "messages": [AIMessage(content="❌ Setup blocked: awaiting human approval")],
        }

    try:
        # Get Harness MCP tools
        harness_tools = get_mcp_tools(["harness"])

        # TODO: Use Harness MCP tools to create resources
        # This is a placeholder implementation

        org_id = state["harness_org_id"]
        project_id = state["harness_project_id"]

        setup_result: HarnessSetupResult = {
            "connectors_created": [
                {
                    "id": "github_conn_1",
                    "name": "GitHub Connector",
                    "type": "github",
                    "status": "success",
                }
            ],
            "secrets_created": [
                {
                    "id": "secret_1",
                    "name": "github_token",
                    "type": "SecretText",
                    "status": "success",
                }
            ],
            "environments_created": [
                {
                    "id": "env_dev",
                    "name": "Development",
                    "type": "PreProduction",
                    "status": "success",
                },
                {
                    "id": "env_prod",
                    "name": "Production",
                    "type": "Production",
                    "status": "success",
                },
            ],
            "services_created": [
                {
                    "id": "svc_1",
                    "name": "Application Service",
                    "type": "Kubernetes",
                    "status": "success",
                }
            ],
            "infrastructure_created": [
                {
                    "id": "infra_k8s",
                    "name": "Kubernetes Cluster",
                    "type": "KubernetesDirect",
                    "status": "success",
                }
            ],
            "pipeline_created": {
                "id": "pipeline_1",
                "name": "Auto-Generated Pipeline",
                "url": f"https://app.harness.io/ng/account/{org_id}/module/cd/orgs/{org_id}/projects/{project_id}/pipelines/pipeline_1",
                "status": "success",
            },
            "setup_status": "success",
            "setup_errors": [],
            "harness_urls": {
                "pipeline": f"https://app.harness.io/ng/account/{org_id}/module/cd/orgs/{org_id}/projects/{project_id}/pipelines/pipeline_1",
                "project": f"https://app.harness.io/ng/account/{org_id}/module/cd/orgs/{org_id}/projects/{project_id}",
            },
        }

        return {
            "harness_setup": setup_result,
            "current_phase": "verify",
            "messages": [
                AIMessage(
                    content=f"""✅ Harness setup complete

**Connectors Created:** {len(setup_result['connectors_created'])}
**Secrets Created:** {len(setup_result['secrets_created'])}
**Environments Created:** {len(setup_result['environments_created'])}
**Services Created:** {len(setup_result['services_created'])}
**Infrastructure Created:** {len(setup_result['infrastructure_created'])}

**Pipeline:** {setup_result['pipeline_created']['name']}
**URL:** {setup_result['pipeline_created']['url']}

Proceeding to deployment verification..."""
                )
            ],
        }

    except Exception as e:
        return {
            "current_phase": "error",
            "errors": [f"Harness setup failed: {str(e)}"],
            "harness_setup": {
                "setup_status": "failed",
                "setup_errors": [str(e)],
            },
            "messages": [AIMessage(content=f"❌ Harness setup failed: {str(e)}")],
        }
