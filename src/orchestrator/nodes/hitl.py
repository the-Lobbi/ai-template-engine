"""Human-in-the-loop approval node."""

from typing import Any

from langchain_core.messages import AIMessage

from ..state import OrchestratorState


def human_approval(state: OrchestratorState) -> dict[str, Any]:
    """Request human approval before proceeding with Harness setup.

    This node pauses the workflow and waits for human approval.
    In LangGraph Studio, this will show up as an interrupt point
    where the user can review and approve/reject.

    Args:
        state: Current orchestrator state

    Returns:
        State updates based on approval decision
    """
    # Check if approval is required
    if not state.get("hitl_required", False):
        # No approval needed, proceed
        return {
            "hitl_approved": True,
            "messages": [AIMessage(content="✅ No approval required, proceeding...")],
        }

    # Check if already approved
    if state.get("hitl_approved", False):
        return {
            "current_phase": "setup",
            "messages": [
                AIMessage(content="✅ Approval granted, proceeding to Harness setup...")
            ],
        }

    # Request approval
    # In LangGraph Studio, this will create an interrupt
    # The user can then provide feedback or approval
    templates = state.get("generated_templates", {})
    patterns = state.get("extracted_patterns", {})

    approval_message = f"""🔍 **Human Approval Required**

Please review the following before proceeding:

**Generated Pipeline:**
- Stages: {len(templates.get('stages', []))}
- Variables: {len(templates.get('variables', {}))}
- Triggers: {len(templates.get('triggers', []))}

**Deployment Configuration:**
- Target: {patterns.get('deployment_target', 'N/A')}
- Strategy: {patterns.get('deployment_strategy', 'N/A')}
- Environments: {', '.join(patterns.get('environments', []))}

**Connectors to Create:**
{chr(10).join(f"- {c['name']} ({c['type']})" for c in patterns.get('connectors_required', []))}

**Secrets to Create:**
{chr(10).join(f"- {s}" for s in patterns.get('secrets_required', []))}

---

**Options:**
1. **Approve** - Proceed with Harness setup
2. **Reject** - Cancel workflow
3. **Modify** - Provide feedback for adjustments

To approve, update the state with: `{{"hitl_approved": true}}`
To reject, update the state with: `{{"current_phase": "error", "errors": ["User rejected"]}}`
"""

    return {
        "messages": [AIMessage(content=approval_message)],
        # This will cause the graph to pause at this node
        # The user must provide input to continue
    }
