"""Reasoning tool for planning code generation using Llama 3.1.

This tool takes the image analysis and creates a plan for what code to generate.
"""

import structlog

from app.adapters.llm_adapter import get_llama_adapter
from app.agents.prompts.templates import REASONING_SYSTEM_PROMPT, REASONING_USER_PROMPT
from app.agents.state import AgentState

logger = structlog.get_logger()


async def plan_approach(state: AgentState) -> dict:
    """Plan the code generation approach using Llama 3.1.

    This function takes the image analysis and creates a structured plan
    for what Python code should be generated.

    Args:
        state: Current agent state with image_analysis.

    Returns:
        Dict with updated state values (reasoning, current_step, error).
    """
    logger.info(
        "Starting reasoning/planning",
        job_id=state.get("job_id"),
        has_analysis=state.get("image_analysis") is not None,
    )

    try:
        image_analysis = state.get("image_analysis")
        if not image_analysis:
            return {
                "error": "No image analysis available for planning",
                "current_step": "error",
            }

        # Get user prompt from messages if available
        user_prompt = ""
        messages = state.get("messages", [])
        if messages:
            for msg in reversed(messages):
                if hasattr(msg, "content"):
                    user_prompt = msg.content
                    break

        # Format the prompt
        formatted_prompt = REASONING_USER_PROMPT.format(
            image_analysis=image_analysis,
            user_prompt=user_prompt or "Generate useful Python code based on the image.",
        )

        # Call reasoning model
        adapter = get_llama_adapter()
        reasoning = await adapter.generate(
            prompt=formatted_prompt,
            system_prompt=REASONING_SYSTEM_PROMPT,
            temperature=0.5,
            max_tokens=1024,
        )

        logger.info(
            "Planning complete",
            job_id=state.get("job_id"),
            reasoning_length=len(reasoning),
        )

        return {
            "reasoning": reasoning,
            "current_step": "planning_complete",
            "error": None,
        }

    except Exception as e:
        logger.error(
            "Planning failed",
            job_id=state.get("job_id"),
            error=str(e),
        )
        return {
            "error": f"Planning failed: {str(e)}",
            "current_step": "error",
        }
