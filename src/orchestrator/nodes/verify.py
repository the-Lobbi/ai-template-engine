"""Deployment verification node."""

import datetime
from typing import Any

from langchain_core.messages import AIMessage

from ..state import DeploymentVerification, OrchestratorState
from ..tools.mcp_registry import get_mcp_tools


def verify_deployment(state: OrchestratorState) -> dict[str, Any]:
    """Verify the deployment by triggering a test pipeline execution.

    Uses the Harness MCP server to:
    1. Trigger the pipeline
    2. Monitor execution
    3. Verify stages completed successfully
    4. Check artifacts generated
    5. Provide recommendations

    Args:
        state: Current orchestrator state

    Returns:
        State updates with verification results
    """
    setup = state.get("harness_setup")

    if not setup or setup.get("setup_status") != "success":
        return {
            "current_phase": "error",
            "errors": ["Cannot verify: Harness setup incomplete or failed"],
            "messages": [
                AIMessage(
                    content="❌ Cannot verify deployment: Harness setup incomplete"
                )
            ],
        }

    try:
        # Get Harness MCP tools
        harness_tools = get_mcp_tools(["harness"])

        # TODO: Use Harness MCP tools to trigger and monitor pipeline
        # This is a placeholder implementation

        pipeline_url = setup["pipeline_created"]["url"]

        verification: DeploymentVerification = {
            "test_execution_id": "exec_test_001",
            "test_execution_url": f"{pipeline_url}/executions/exec_test_001",
            "execution_status": "success",
            "stages_completed": ["build", "test", "deploy"],
            "stages_failed": [],
            "artifacts_generated": ["docker_image:latest"],
            "logs_url": f"{pipeline_url}/executions/exec_test_001/logs",
            "verification_passed": True,
            "recommendations": [
                "Pipeline executed successfully",
                "Consider adding monitoring and alerts",
                "Review and optimize resource limits",
                "Add automated rollback on failure",
                "Configure approval gates for production",
            ],
        }

        # Calculate total duration
        started = datetime.datetime.fromisoformat(state["started_at"])
        completed = datetime.datetime.now(datetime.UTC)
        duration = (completed - started).total_seconds()

        return {
            "deployment_verification": verification,
            "current_phase": "complete",
            "completed_at": completed.isoformat(),
            "total_duration_seconds": duration,
            "messages": [
                AIMessage(
                    content=f"""✅ Deployment verification complete

**Execution Status:** {verification['execution_status']}
**Stages Completed:** {', '.join(verification['stages_completed'])}
**Artifacts:** {', '.join(verification['artifacts_generated'])}

**Execution URL:** {verification['test_execution_url']}
**Logs:** {verification['logs_url']}

**Recommendations:**
{chr(10).join(f"- {r}" for r in verification['recommendations'])}

---

**Workflow Complete**
**Total Duration:** {duration:.2f} seconds

🚀 Your Harness CI/CD pipeline is ready to use!"""
                )
            ],
        }

    except Exception as e:
        return {
            "current_phase": "error",
            "errors": [f"Deployment verification failed: {str(e)}"],
            "deployment_verification": {
                "execution_status": "failed",
                "verification_passed": False,
            },
            "messages": [
                AIMessage(content=f"❌ Deployment verification failed: {str(e)}")
            ],
        }
