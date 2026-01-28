"""Tests for rate limiter."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestRateLimiter:
    """Test cases for RateLimiter class."""

    @pytest.mark.asyncio
    async def test_is_allowed_when_redis_unavailable(self):
        """Test rate limiter allows requests when Redis is down (fail open)."""
        from app.core.rate_limiter import RateLimiter
        
        with patch("app.core.rate_limiter.cache_manager") as mock_cm:
            mock_cm.redis = None
            
            limiter = RateLimiter(requests_limit=10, window_seconds=60)
            is_allowed, remaining = await limiter.is_allowed("test-user")
            
            assert is_allowed is True
            assert remaining == 10

    @pytest.mark.asyncio
    async def test_is_allowed_under_limit(self, mock_redis):
        """Test rate limiter allows requests under limit."""
        from app.core.rate_limiter import RateLimiter
        
        with patch("app.core.rate_limiter.cache_manager") as mock_cm:
            mock_cm.redis = mock_redis
            mock_redis.zcard.return_value = 5  # 5 requests so far
            
            limiter = RateLimiter(requests_limit=10, window_seconds=60)
            is_allowed, remaining = await limiter.is_allowed("test-user")
            
            assert is_allowed is True
            assert remaining == 4  # 10 - 5 - 1 (current request)

    @pytest.mark.asyncio
    async def test_is_allowed_at_limit(self, mock_redis):
        """Test rate limiter blocks requests at limit."""
        from app.core.rate_limiter import RateLimiter
        
        with patch("app.core.rate_limiter.cache_manager") as mock_cm:
            mock_cm.redis = mock_redis
            mock_redis.zcard.return_value = 10  # At limit
            
            limiter = RateLimiter(requests_limit=10, window_seconds=60)
            is_allowed, remaining = await limiter.is_allowed("test-user")
            
            assert is_allowed is False
            assert remaining == 0

    @pytest.mark.asyncio
    async def test_different_users_have_separate_limits(self, mock_redis):
        """Test each user has independent rate limit."""
        from app.core.rate_limiter import RateLimiter
        
        with patch("app.core.rate_limiter.cache_manager") as mock_cm:
            mock_cm.redis = mock_redis
            mock_redis.zcard.return_value = 0
            
            limiter = RateLimiter(requests_limit=10, window_seconds=60)
            
            # Different users should both be allowed
            allowed1, _ = await limiter.is_allowed("user-1")
            allowed2, _ = await limiter.is_allowed("user-2")
            
            assert allowed1 is True
            assert allowed2 is True
