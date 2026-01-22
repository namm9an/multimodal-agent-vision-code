"""LLM adapter classes for E2E Networks endpoints.

This module provides async clients for interacting with the E2E Networks
inference endpoints using the OpenAI-compatible API format.
"""

import base64
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import httpx
import structlog

from app.config import get_settings

logger = structlog.get_logger()


class LLMAdapterError(Exception):
    """Base exception for LLM adapter errors."""


class LLMConnectionError(LLMAdapterError):
    """Raised when connection to LLM endpoint fails."""


class LLMResponseError(LLMAdapterError):
    """Raised when LLM returns an error response."""


class BaseLLMAdapter(ABC):
    """Abstract base class for LLM adapters.

    All LLM adapters must implement the generate method.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        api_token: str,
        timeout: float = 120.0,
    ) -> None:
        """Initialize the LLM adapter.

        Args:
            base_url: The base URL for the LLM endpoint.
            model: The model identifier to use.
            api_token: Bearer token for authentication.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_token = api_token
        self.timeout = timeout

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            The generated text response.
        """
        pass

    async def health_check(self) -> bool:
        """Check if the LLM endpoint is healthy.

        Returns:
            True if healthy, False otherwise.
        """
        try:
            response = await self.generate(
                prompt="Say 'OK' if you are working.",
                max_tokens=10,
            )
            return len(response) > 0
        except (LLMAdapterError, httpx.HTTPError) as e:
            logger.warning("Health check failed", model=self.model, error=str(e))
            return False


class TextLLMAdapter(BaseLLMAdapter):
    """Adapter for text-only LLM endpoints (Mistral, DeepSeek)."""

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a text response from the LLM.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            The generated text response.

        Raises:
            LLMConnectionError: If connection fails.
            LLMResponseError: If LLM returns an error.
        """
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                )

                if response.status_code != 200:
                    logger.error(
                        "LLM request failed",
                        model=self.model,
                        status_code=response.status_code,
                        response=response.text,
                    )
                    raise LLMResponseError(
                        f"LLM returned status {response.status_code}: {response.text}"
                    )

                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.ConnectError as e:
            logger.error("Connection to LLM failed", model=self.model, error=str(e))
            raise LLMConnectionError(f"Failed to connect to {self.model}: {e}")
        except httpx.TimeoutException as e:
            logger.error("LLM request timed out", model=self.model, error=str(e))
            raise LLMConnectionError(f"Request to {self.model} timed out: {e}")
        except KeyError as e:
            logger.error("Unexpected LLM response format", model=self.model, error=str(e))
            raise LLMResponseError(f"Unexpected response format from {self.model}: {e}")


class VisionLLMAdapter(BaseLLMAdapter):
    """Adapter for vision LLM endpoints (Qwen2.5-VL)."""

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a text response from the vision LLM (text-only mode).

        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            The generated text response.
        """
        # For text-only calls, use the same logic as TextLLMAdapter
        messages: list[dict[str, Any]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                )

                if response.status_code != 200:
                    raise LLMResponseError(
                        f"LLM returned status {response.status_code}: {response.text}"
                    )

                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.ConnectError as e:
            raise LLMConnectionError(f"Failed to connect to {self.model}: {e}")
        except httpx.TimeoutException as e:
            raise LLMConnectionError(f"Request to {self.model} timed out: {e}")

    async def generate_with_image(
        self,
        prompt: str,
        image_data: bytes,
        image_mime_type: str = "image/png",
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a response based on an image and prompt.

        Args:
            prompt: The user prompt describing what to analyze.
            image_data: Raw image bytes.
            image_mime_type: MIME type of the image.
            system_prompt: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            The generated text analysis.

        Raises:
            LLMConnectionError: If connection fails.
            LLMResponseError: If LLM returns an error.
        """
        # Encode image to base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        image_url = f"data:{image_mime_type};base64,{image_base64}"

        messages: list[dict[str, Any]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Multimodal message format for vision models
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                )

                if response.status_code != 200:
                    logger.error(
                        "Vision LLM request failed",
                        model=self.model,
                        status_code=response.status_code,
                        response=response.text,
                    )
                    raise LLMResponseError(
                        f"LLM returned status {response.status_code}: {response.text}"
                    )

                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.ConnectError as e:
            logger.error("Connection to vision LLM failed", model=self.model, error=str(e))
            raise LLMConnectionError(f"Failed to connect to {self.model}: {e}")
        except httpx.TimeoutException as e:
            logger.error("Vision LLM request timed out", model=self.model, error=str(e))
            raise LLMConnectionError(f"Request to {self.model} timed out: {e}")

    async def generate_with_image_path(
        self,
        prompt: str,
        image_path: str | Path,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a response based on an image file path.

        Args:
            prompt: The user prompt describing what to analyze.
            image_path: Path to the image file.
            system_prompt: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            The generated text analysis.
        """
        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")

        # Determine MIME type from extension
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        mime_type = mime_types.get(path.suffix.lower(), "image/png")

        with open(path, "rb") as f:
            image_data = f.read()

        return await self.generate_with_image(
            prompt=prompt,
            image_data=image_data,
            image_mime_type=mime_type,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )


# Factory functions to create adapters from settings


def get_qwen_adapter() -> VisionLLMAdapter:
    """Get the Qwen vision model adapter."""
    settings = get_settings()
    return VisionLLMAdapter(
        base_url=settings.qwen_base_url,
        model=settings.qwen_model,
        api_token=settings.e2e_api_token,
    )


def get_llama_adapter() -> TextLLMAdapter:
    """Get the Llama 3.1 reasoning model adapter."""
    settings = get_settings()
    return TextLLMAdapter(
        base_url=settings.llama_base_url,
        model=settings.llama_model,
        api_token=settings.e2e_api_token,
    )


def get_deepseek_adapter() -> TextLLMAdapter:
    """Get the DeepSeek code generation model adapter."""
    settings = get_settings()
    return TextLLMAdapter(
        base_url=settings.deepseek_base_url,
        model=settings.deepseek_model,
        api_token=settings.e2e_api_token,
    )
