"""Redis-based API rate limiting.

Implements sliding window rate limiting using Redis sorted sets.
Integrates with existing cache_manager from Phase 4.

Following Google Python Style Guide.
"""

import time
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.core.cache import cache_manager
from app.core.logging import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Sliding window rate limiter using Redis sorted sets.

    Uses Redis ZSET to track request timestamps within a sliding window.
    This approach provides accurate rate limiting without race conditions.

    Attributes:
        requests_limit: Maximum requests allowed per window.
        window_seconds: Size of the sliding window in seconds.
    """

    def __init__(
        self,
        requests_limit: int | None = None,
        window_seconds: int | None = None,
    ) -> None:
        """Initialize rate limiter with configurable limits.

        Args:
            requests_limit: Max requests per window. Defaults to config value.
            window_seconds: Window size in seconds. Defaults to config value.
        """
        settings = get_settings()
        self.requests_limit = requests_limit or settings.rate_limit_requests
        self.window_seconds = window_seconds or settings.rate_limit_window

    async def is_allowed(self, identifier: str) -> tuple[bool, int]:
        """Check if request is allowed under rate limit.

        Args:
            identifier: Unique identifier for rate limiting (e.g., user_id, IP).

        Returns:
            Tuple of (is_allowed, remaining_requests).
        """
        if not cache_manager.redis:
            # If Redis unavailable, allow request (fail open)
            logger.warning("Redis unavailable, rate limiting disabled")
            return True, self.requests_limit

        key = f"rate_limit:{identifier}"
        now = time.time()
        window_start = now - self.window_seconds

        try:
            # Remove old entries outside the window
            await cache_manager.redis.zremrangebyscore(key, 0, window_start)

            # Count current requests in window
            current_count = await cache_manager.redis.zcard(key)

            if current_count >= self.requests_limit:
                logger.warning(
                    "Rate limit exceeded",
                    identifier=identifier,
                    limit=self.requests_limit,
                    window=self.window_seconds,
                )
                return False, 0

            # Add current request
            await cache_manager.redis.zadd(key, {str(now): now})
            await cache_manager.redis.expire(key, self.window_seconds)

            remaining = self.requests_limit - current_count - 1
            return True, remaining

        except Exception as e:
            logger.error("Rate limit check failed", error=str(e))
            # Fail open on errors
            return True, self.requests_limit


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(
    request: Request,
    call_next: Callable,
) -> Response:
    """FastAPI middleware for rate limiting.

    Applies rate limiting based on user ID (if authenticated) or IP address.
    Adds rate limit headers to response.

    Args:
        request: FastAPI request object.
        call_next: Next middleware/handler in chain.

    Returns:
        Response with rate limit headers, or 429 if limit exceeded.
    """
    settings = get_settings()

    # Skip rate limiting in development (optional)
    if settings.is_development and settings.debug:
        return await call_next(request)

    # Get identifier: prefer user_id, fallback to IP
    user_id = getattr(request.state, "user_id", None)
    identifier = user_id or request.client.host if request.client else "unknown"

    # Check rate limit
    is_allowed, remaining = await rate_limiter.is_allowed(identifier)

    if not is_allowed:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "success": False,
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": f"Rate limit exceeded. Try again in {settings.rate_limit_window} seconds.",
                },
            },
            headers={
                "X-RateLimit-Limit": str(settings.rate_limit_requests),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(time.time()) + settings.rate_limit_window),
                "Retry-After": str(settings.rate_limit_window),
            },
        )

    # Proceed with request
    response = await call_next(request)

    # Add rate limit headers to successful responses
    response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
    response.headers["X-RateLimit-Remaining"] = str(remaining)

    return response
