"""Code generation tool using DeepSeek.

This tool generates Python code based on the image analysis and planning results.
"""

import re

import structlog

from app.adapters.llm_adapter import get_deepseek_adapter
from app.agents.prompts.templates import CODEGEN_SYSTEM_PROMPT, CODEGEN_USER_PROMPT
from app.agents.state import AgentState

logger = structlog.get_logger()


def extract_python_code(text: str) -> str:
    """Extract Python code from markdown code blocks.

    Args:
        text: Text containing Python code blocks.

    Returns:
        Extracted Python code, or the original text if no blocks found.
    """
    # Try to find code blocks
    pattern = r"```python\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        # Return the first Python code block
        return matches[0].strip()

    # Try generic code blocks
    pattern = r"```\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        return matches[0].strip()

    # Return original text if no code blocks found
    return text.strip()


def validate_code_syntax(code: str) -> tuple[bool, str | None]:
    """Validate Python code syntax.

    Args:
        code: Python code to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        compile(code, "<string>", "exec")
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"


async def generate_code(state: AgentState) -> dict:
    """Generate Python code using DeepSeek.

    This function takes the image analysis and reasoning to generate
    executable Python code.

    Args:
        state: Current agent state with image_analysis and reasoning.

    Returns:
        Dict with updated state values (generated_code, current_step, error).
    """
    logger.info(
        "Starting code generation",
        job_id=state.get("job_id"),
        has_analysis=state.get("image_analysis") is not None,
        has_reasoning=state.get("reasoning") is not None,
    )

    try:
        image_analysis = state.get("image_analysis")
        reasoning = state.get("reasoning")

        if not image_analysis:
            return {
                "error": "No image analysis available for code generation",
                "current_step": "error",
            }

        if not reasoning:
            # Use a default reasoning if not available
            reasoning = "Generate Python code to process and analyze the described data."

        # Get user prompt from messages if available
        user_prompt = ""
        messages = state.get("messages", [])
        if messages:
            for msg in reversed(messages):
                if hasattr(msg, "content"):
                    user_prompt = msg.content
                    break

        # Format the prompt
        formatted_prompt = CODEGEN_USER_PROMPT.format(
            image_analysis=image_analysis,
            reasoning=reasoning,
            user_prompt=user_prompt or "Generate useful Python code.",
        )

        # Call code generation model
        adapter = get_deepseek_adapter()
        response = await adapter.generate(
            prompt=formatted_prompt,
            system_prompt=CODEGEN_SYSTEM_PROMPT,
            temperature=0.2,  # Lower temperature for code generation
            max_tokens=4096,
        )

        # Extract code from response
        code = extract_python_code(response)

        # Validate syntax
        is_valid, error_msg = validate_code_syntax(code)
        if not is_valid:
            logger.warning(
                "Generated code has syntax errors",
                job_id=state.get("job_id"),
                error=error_msg,
            )
            # Still return the code, but include the error
            return {
                "generated_code": code,
                "current_step": "codegen_complete_with_errors",
                "error": f"Code has syntax errors: {error_msg}",
            }

        logger.info(
            "Code generation complete",
            job_id=state.get("job_id"),
            code_length=len(code),
        )

        return {
            "generated_code": code,
            "current_step": "codegen_complete",
            "error": None,
        }

    except Exception as e:
        logger.error(
            "Code generation failed",
            job_id=state.get("job_id"),
            error=str(e),
        )
        return {
            "error": f"Code generation failed: {str(e)}",
            "current_step": "error",
        }
