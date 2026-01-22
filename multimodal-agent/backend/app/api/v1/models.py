"""LLM health check and testing endpoints."""

import structlog
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.adapters.llm_adapter import (
    LLMAdapterError,
    get_deepseek_adapter,
    get_llama_adapter,
    get_qwen_adapter,
)

router = APIRouter()
logger = structlog.get_logger()


class ModelHealthResponse(BaseModel):
    """Response model for model health check."""

    qwen: str
    llama: str
    deepseek: str


class ModelTestRequest(BaseModel):
    """Request model for testing a specific LLM."""

    model: str  # "qwen", "llama", or "deepseek"
    prompt: str
    system_prompt: str | None = None


class ModelTestResponse(BaseModel):
    """Response model for LLM test."""

    model: str
    response: str
    success: bool
    error: str | None = None


@router.get(
    "/health",
    response_model=ModelHealthResponse,
    summary="Check LLM health",
    description="Check if all three LLM endpoints are accessible and responding.",
)
async def check_model_health() -> ModelHealthResponse:
    """Check health of all LLM endpoints.

    Returns:
        ModelHealthResponse: Health status for each model.
    """
    results = {
        "qwen": "unknown",
        "llama": "unknown",
        "deepseek": "unknown",
    }

    # Check Qwen (Vision)
    try:
        qwen = get_qwen_adapter()
        if await qwen.health_check():
            results["qwen"] = "healthy"
        else:
            results["qwen"] = "unhealthy"
    except Exception as e:
        logger.error("Qwen health check error", error=str(e))
        results["qwen"] = f"error: {str(e)[:50]}"

    # Check Llama (Reasoning)
    try:
        llama = get_llama_adapter()
        if await llama.health_check():
            results["llama"] = "healthy"
        else:
            results["llama"] = "unhealthy"
    except Exception as e:
        logger.error("Llama health check error", error=str(e))
        results["llama"] = f"error: {str(e)[:50]}"

    # Check DeepSeek (CodeGen)
    try:
        deepseek = get_deepseek_adapter()
        if await deepseek.health_check():
            results["deepseek"] = "healthy"
        else:
            results["deepseek"] = "unhealthy"
    except Exception as e:
        logger.error("DeepSeek health check error", error=str(e))
        results["deepseek"] = f"error: {str(e)[:50]}"

    return ModelHealthResponse(**results)


@router.post(
    "/test",
    response_model=ModelTestResponse,
    summary="Test a specific LLM",
    description="Send a test prompt to a specific LLM and get the response.",
)
async def test_model(request: ModelTestRequest) -> ModelTestResponse:
    """Test a specific LLM with a prompt.

    Args:
        request: The test request with model name and prompt.

    Returns:
        ModelTestResponse: The response from the LLM.
    """
    adapters = {
        "qwen": get_qwen_adapter,
        "llama": get_llama_adapter,
        "deepseek": get_deepseek_adapter,
    }

    if request.model not in adapters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown model: {request.model}. Use 'qwen', 'llama', or 'deepseek'.",
        )

    try:
        adapter = adapters[request.model]()
        response = await adapter.generate(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
        )

        logger.info(
            "LLM test successful",
            model=request.model,
            prompt_length=len(request.prompt),
            response_length=len(response),
        )

        return ModelTestResponse(
            model=request.model,
            response=response,
            success=True,
        )

    except LLMAdapterError as e:
        logger.error("LLM test failed", model=request.model, error=str(e))
        return ModelTestResponse(
            model=request.model,
            response="",
            success=False,
            error=str(e),
        )
