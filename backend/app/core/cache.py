"""Redis caching layer for improved performance.

This module provides a Redis-based caching layer with:
- Job result caching to avoid reprocessing
- LLM response caching for identical prompts
- Rate limiting support
- Automatic cache invalidation with TTL

Following Google Python Style Guide.
"""

import hashlib
import json
from typing import Any

import redis.asyncio as redis
from redis.asyncio import Redis

from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CacheManager:
    """Manages Redis caching operations.

    Provides async methods for caching job results, LLM responses,
    and rate limiting data.

    Attributes:
        redis: Async Redis client instance.
        default_ttl: Default time-to-live for cache entries in seconds.
    """

    def __init__(self) -> None:
        """Initialize CacheManager with Redis connection."""
        self.redis: Redis | None = None
        self.default_ttl = 3600  # 1 hour default

    async def connect(self) -> None:
        """Establish connection to Redis server."""
        try:
            self.redis = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
            await self.redis.ping()
            logger.info("Redis cache connected successfully")
        except Exception as e:
            logger.error("Failed to connect to Redis cache", error=str(e))
            self.redis = None

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
            logger.info("Redis cache disconnected")

    async def get(self, key: str) -> Any | None:
        """Retrieve value from cache.

        Args:
            key: Cache key to retrieve.

        Returns:
            Cached value if found, None otherwise.
        """
        if not self.redis:
            return None

        try:
            value = await self.redis.get(key)
            if value:
                logger.debug("Cache hit", key=key)
                return json.loads(value)
            logger.debug("Cache miss", key=key)
            return None
        except Exception as e:
            logger.warning("Cache get failed", key=key, error=str(e))
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:
        """Store value in cache.

        Args:
            key: Cache key.
            value: Value to cache (must be JSON serializable).
            ttl: Time-to-live in seconds. Uses default if not specified.

        Returns:
            True if successful, False otherwise.
        """
        if not self.redis:
            return False

        try:
            serialized = json.dumps(value)
            await self.redis.setex(
                key,
                ttl or self.default_ttl,
                serialized,
            )
            logger.debug("Cache set", key=key, ttl=ttl or self.default_ttl)
            return True
        except Exception as e:
            logger.warning("Cache set failed", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache.

        Args:
            key: Cache key to delete.

        Returns:
            True if key was deleted, False otherwise.
        """
        if not self.redis:
            return False

        try:
            result = await self.redis.delete(key)
            logger.debug("Cache delete", key=key, deleted=bool(result))
            return bool(result)
        except Exception as e:
            logger.warning("Cache delete failed", key=key, error=str(e))
            return False

    @staticmethod
    def generate_key(prefix: str, *args: str) -> str:
        """Generate a cache key from prefix and arguments.

        Args:
            prefix: Key prefix (e.g., 'job', 'llm').
            *args: Additional key components.

        Returns:
            Formatted cache key string.
        """
        components = [prefix] + list(args)
        return ":".join(components)

    @staticmethod
    def hash_prompt(prompt: str, model: str) -> str:
        """Generate hash for LLM prompt caching.

        Args:
            prompt: The prompt text.
            model: Model identifier.

        Returns:
            SHA256 hash of the prompt+model combination.
        """
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# Global cache manager instance
cache_manager = CacheManager()


async def get_cached_job_result(job_id: str) -> dict[str, Any] | None:
    """Get cached job result.

    Args:
        job_id: The job ID to look up.

    Returns:
        Cached job result dict or None.
    """
    key = CacheManager.generate_key("job", job_id, "result")
    return await cache_manager.get(key)


async def cache_job_result(
    job_id: str,
    result: dict[str, Any],
    ttl: int = 86400,  # 24 hours
) -> bool:
    """Cache a job result.

    Args:
        job_id: The job ID.
        result: Result data to cache.
        ttl: Cache TTL in seconds.

    Returns:
        True if cached successfully.
    """
    key = CacheManager.generate_key("job", job_id, "result")
    return await cache_manager.set(key, result, ttl)


async def get_cached_llm_response(
    prompt: str,
    model: str,
) -> str | None:
    """Get cached LLM response for identical prompts.

    Args:
        prompt: The prompt text.
        model: Model identifier.

    Returns:
        Cached response string or None.
    """
    prompt_hash = CacheManager.hash_prompt(prompt, model)
    key = CacheManager.generate_key("llm", model, prompt_hash)
    result = await cache_manager.get(key)
    return result.get("response") if result else None


async def cache_llm_response(
    prompt: str,
    model: str,
    response: str,
    ttl: int = 3600,  # 1 hour
) -> bool:
    """Cache an LLM response.

    Args:
        prompt: The prompt text.
        model: Model identifier.
        response: The LLM response to cache.
        ttl: Cache TTL in seconds.

    Returns:
        True if cached successfully.
    """
    prompt_hash = CacheManager.hash_prompt(prompt, model)
    key = CacheManager.generate_key("llm", model, prompt_hash)
    return await cache_manager.set(key, {"response": response}, ttl)
