"""LangGraph workflow definition for Harness orchestration.

This module defines the complete workflow graph that will be visualized
in LangGraph Studio. The graph coordinates all phases of the orchestration:
initialize → analyze → extract → generate → approve → setup → verify
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import OrchestratorState
from .nodes import (
    initialize_workflow,
    analyze_repository,
    extract_patterns,
    generate_templates,
    human_approval,
    setup_harness,
    verify_deployment,
)


def should_proceed_to_setup(state: OrchestratorState) -> str:
    """Conditional edge: check if we should proceed to setup.

    Returns 'setup' if approved, 'approval' if waiting for approval.
    """
    if state.get("hitl_required") and not state.get("hitl_approved"):
        return "approval"
    return "setup"


def should_continue_workflow(state: OrchestratorState) -> str:
    """Conditional edge: check if workflow should continue or end.

    Returns 'error' if there are errors, 'end' if complete, or next phase.
    """
    if state.get("errors"):
        return "error"

    phase = state.get("current_phase")

    if phase == "complete":
        return "end"
    elif phase == "error":
        return "error"

    # Continue to next phase
    return phase


# Create the workflow graph
workflow = StateGraph(OrchestratorState)

# Add nodes to the graph
workflow.add_node("init", initialize_workflow)
workflow.add_node("analyze", analyze_repository)
workflow.add_node("extract", extract_patterns)
workflow.add_node("generate", generate_templates)
workflow.add_node("approval", human_approval)
workflow.add_node("setup", setup_harness)
workflow.add_node("verify", verify_deployment)

# Define edges (workflow flow)
workflow.add_edge(START, "init")
workflow.add_edge("init", "analyze")
workflow.add_edge("analyze", "extract")
workflow.add_edge("extract", "generate")

# Conditional edge for human approval
workflow.add_conditional_edges(
    "generate",
    should_proceed_to_setup,
    {
        "approval": "approval",
        "setup": "setup",
    },
)

# Allow loop back from approval to setup after approval
workflow.add_conditional_edges(
    "approval",
    should_proceed_to_setup,
    {
        "approval": "approval",  # Stay in approval until approved
        "setup": "setup",
    },
)

workflow.add_edge("setup", "verify")

# Conditional edge for completion
workflow.add_conditional_edges(
    "verify",
    should_continue_workflow,
    {
        "end": END,
        "error": END,
        "complete": END,
    },
)

# Add error handling edge
workflow.add_edge("init", END)  # Allow early exit from init if errors

# Compile the graph with memory checkpointer for Studio
# This enables the graph to pause at interrupts (like human approval)
memory = MemorySaver()
graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["approval"],  # Pause before approval node
)

# Export for LangGraph Studio
# The langgraph.json file points to this variable
__all__ = ["graph"]
