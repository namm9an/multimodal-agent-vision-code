"""Vision tool for image analysis using Qwen2.5-VL.

This tool handles downloading images from MinIO and calling the vision model
to analyze them.
"""

import structlog

from app.adapters.llm_adapter import get_qwen_adapter
from app.agents.prompts.templates import VISION_SYSTEM_PROMPT, VISION_USER_PROMPT
from app.agents.state import AgentState

logger = structlog.get_logger()


async def analyze_image(state: AgentState) -> dict:
    """Analyze an image using the Qwen vision model.

    This function takes the image data from state and calls the vision model
    to generate a detailed analysis.

    Args:
        state: Current agent state with image_data and image_mime_type.

    Returns:
        Dict with updated state values (image_analysis, current_step, error).
    """
    logger.info(
        "Starting image analysis",
        job_id=state.get("job_id"),
        has_image_data=state.get("image_data") is not None,
    )

    try:
        # Get image data from state
        image_data = state.get("image_data")
        if not image_data:
            return {
                "error": "No image data available for analysis",
                "current_step": "error",
            }

        image_mime_type = state.get("image_mime_type", "image/png")

        # Get user prompt from messages if available
        user_prompt = ""
        messages = state.get("messages", [])
        if messages:
            # Get the last human message
            for msg in reversed(messages):
                if hasattr(msg, "content"):
                    user_prompt = msg.content
                    break

        # Format the prompt
        formatted_prompt = VISION_USER_PROMPT.format(
            user_prompt=user_prompt or "Analyze this image and describe its contents."
        )

        # Call vision model
        adapter = get_qwen_adapter()
        analysis = await adapter.generate_with_image(
            prompt=formatted_prompt,
            image_data=image_data,
            image_mime_type=image_mime_type,
            system_prompt=VISION_SYSTEM_PROMPT,
            temperature=0.3,  # Lower temperature for more factual analysis
            max_tokens=2048,
        )

        logger.info(
            "Image analysis complete",
            job_id=state.get("job_id"),
            analysis_length=len(analysis),
        )

        return {
            "image_analysis": analysis,
            "current_step": "analyze_complete",
            "error": None,
        }

    except Exception as e:
        logger.error(
            "Image analysis failed",
            job_id=state.get("job_id"),
            error=str(e),
        )
        return {
            "error": f"Image analysis failed: {str(e)}",
            "current_step": "error",
        }
