"""Initialize workflow node."""

import datetime
import uuid
from typing import Any

from langchain_core.messages import AIMessage

from ..state import OrchestratorState


def initialize_workflow(state: OrchestratorState) -> dict[str, Any]:
    """Initialize the orchestration workflow.

    Sets up workflow metadata and validates input parameters.

    Args:
        state: Current orchestrator state

    Returns:
        State updates
    """
    workflow_id = str(uuid.uuid4())
    started_at = datetime.datetime.now(datetime.UTC).isoformat()

    # Validate required inputs
    errors = []
    if not state.get("target_repo_path"):
        errors.append("target_repo_path is required")
    if not state.get("harness_org_id"):
        errors.append("harness_org_id is required")
    if not state.get("harness_project_id"):
        errors.append("harness_project_id is required")

    if errors:
        return {
            "current_phase": "error",
            "errors": errors,
            "messages": [
                AIMessage(
                    content=f"❌ Workflow initialization failed: {', '.join(errors)}"
                )
            ],
        }

    return {
        "workflow_id": workflow_id,
        "started_at": started_at,
        "current_phase": "analyze",
        "errors": [],
        "warnings": [],
        "hitl_required": False,
        "hitl_approved": False,
        "messages": [
            AIMessage(
                content=f"""✅ Workflow initialized successfully

**Workflow ID:** `{workflow_id}`
**Repository:** `{state['target_repo_path']}`
**Harness Org:** `{state['harness_org_id']}`
**Harness Project:** `{state['harness_project_id']}`

Starting repository analysis..."""
            )
        ],
    }
