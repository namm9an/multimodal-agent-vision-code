"""Tests for cache manager."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestCacheManager:
    """Test cases for CacheManager class."""

    @pytest.mark.asyncio
    async def test_generate_key(self):
        """Test cache key generation."""
        from app.core.cache import CacheManager
        
        key = CacheManager.generate_key("job", "123", "result")
        assert key == "job:123:result"

    @pytest.mark.asyncio
    async def test_generate_key_single_component(self):
        """Test cache key with single component."""
        from app.core.cache import CacheManager
        
        key = CacheManager.generate_key("prefix")
        assert key == "prefix"

    @pytest.mark.asyncio
    async def test_hash_prompt(self):
        """Test prompt hashing for LLM caching."""
        from app.core.cache import CacheManager
        
        hash1 = CacheManager.hash_prompt("test prompt", "qwen")
        hash2 = CacheManager.hash_prompt("test prompt", "qwen")
        hash3 = CacheManager.hash_prompt("different prompt", "qwen")
        
        assert hash1 == hash2  # Same input = same hash
        assert hash1 != hash3  # Different input = different hash
        assert len(hash1) == 16  # Truncated hash

    @pytest.mark.asyncio
    async def test_get_returns_none_when_redis_unavailable(self):
        """Test cache get fails gracefully without Redis."""
        from app.core.cache import CacheManager
        
        manager = CacheManager()
        manager.redis = None
        
        result = await manager.get("test_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_returns_false_when_redis_unavailable(self):
        """Test cache set fails gracefully without Redis."""
        from app.core.cache import CacheManager
        
        manager = CacheManager()
        manager.redis = None
        
        result = await manager.set("test_key", {"data": "value"})
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_redis_unavailable(self):
        """Test cache delete fails gracefully without Redis."""
        from app.core.cache import CacheManager
        
        manager = CacheManager()
        manager.redis = None
        
        result = await manager.delete("test_key")
        assert result is False
