"""LangGraph workflow for the multimodal AI agent.

This module defines the graph-based workflow that orchestrates image analysis,
reasoning, and code generation using LangGraph.
"""

import structlog
from langgraph.graph import END, StateGraph

from app.agents.state import AgentState
from app.agents.tools.codegen_tool import generate_code
from app.agents.tools.reasoning_tool import plan_approach
from app.agents.tools.vision_tool import analyze_image

logger = structlog.get_logger()


def should_continue(state: AgentState) -> str:
    """Determine the next step based on current state.

    This is the routing function for conditional edges.

    Args:
        state: Current agent state.

    Returns:
        Name of the next node to execute, or END.
    """
    current_step = state.get("current_step", "")
    error = state.get("error")

    # If there's an error, end the workflow
    if error and current_step == "error":
        logger.warning("Workflow ending due to error", error=error)
        return END

    # Route based on current step
    if current_step == "analyze_complete":
        return "plan_approach"
    elif current_step == "planning_complete":
        return "generate_code"
    elif current_step in ("codegen_complete", "codegen_complete_with_errors"):
        return END

    # Default: continue to next step or end
    return END


def create_agent_graph() -> StateGraph:
    """Create the LangGraph workflow for the agent.

    The workflow follows this pattern:
    START -> analyze_image -> plan_approach -> generate_code -> END

    Returns:
        Compiled StateGraph ready for invocation.
    """
    # Create the graph with our state type
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("analyze_image", analyze_image)
    workflow.add_node("plan_approach", plan_approach)
    workflow.add_node("generate_code", generate_code)

    # Set entry point
    workflow.set_entry_point("analyze_image")

    # Add conditional edges
    workflow.add_conditional_edges(
        "analyze_image",
        should_continue,
        {
            "plan_approach": "plan_approach",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "plan_approach",
        should_continue,
        {
            "generate_code": "generate_code",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "generate_code",
        should_continue,
        {
            END: END,
        },
    )

    return workflow.compile()


# Create a singleton instance
_agent_graph = None


def get_agent_graph() -> StateGraph:
    """Get the agent graph singleton.

    Returns:
        The compiled agent graph.
    """
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = create_agent_graph()
    return _agent_graph


async def run_agent(
    job_id: str,
    user_id: str,
    image_path: str,
    image_data: bytes,
    image_mime_type: str = "image/png",
    user_prompt: str = "",
) -> AgentState:
    """Run the agent workflow for a job.

    Args:
        job_id: The ID of the processing job.
        user_id: The ID of the user who created the job.
        image_path: Path to the image in storage.
        image_data: Raw image bytes.
        image_mime_type: MIME type of the image.
        user_prompt: Optional user prompt for processing.

    Returns:
        Final agent state with results.
    """
    logger.info(
        "Running agent workflow",
        job_id=job_id,
        user_id=user_id,
        image_path=image_path,
        has_prompt=bool(user_prompt),
    )

    # Create initial state
    initial_state: AgentState = {
        "messages": [],
        "job_id": job_id,
        "user_id": user_id,
        "image_path": image_path,
        "image_data": image_data,
        "image_mime_type": image_mime_type,
        "image_analysis": None,
        "reasoning": None,
        "generated_code": None,
        "execution_result": None,
        "error": None,
        "current_step": "start",
    }

    # Add user prompt as a message if provided
    if user_prompt:
        from langchain_core.messages import HumanMessage

        initial_state["messages"] = [HumanMessage(content=user_prompt)]

    # Get and run the graph
    graph = get_agent_graph()
    final_state = await graph.ainvoke(initial_state)

    logger.info(
        "Agent workflow complete",
        job_id=job_id,
        final_step=final_state.get("current_step"),
        has_code=final_state.get("generated_code") is not None,
        has_error=final_state.get("error") is not None,
    )

    return final_state
