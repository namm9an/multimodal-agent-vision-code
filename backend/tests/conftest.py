"""Pytest fixtures for backend tests.

Provides mock Redis, database, and authentication fixtures
for isolated unit testing.
"""

import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_redis():
    """Mock Redis client for cache tests."""
    redis_mock = AsyncMock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.setex.return_value = True
    redis_mock.delete.return_value = 1
    redis_mock.zremrangebyscore.return_value = 0
    redis_mock.zcard.return_value = 0
    redis_mock.zadd.return_value = 1
    redis_mock.expire.return_value = True
    redis_mock.ping.return_value = True
    return redis_mock


@pytest.fixture
def mock_cache_manager(mock_redis):
    """Mock cache manager with Redis client."""
    with patch("app.core.cache.cache_manager") as mock_cm:
        mock_cm.redis = mock_redis
        mock_cm.get = AsyncMock(return_value=None)
        mock_cm.set = AsyncMock(return_value=True)
        mock_cm.delete = AsyncMock(return_value=True)
        yield mock_cm


@pytest.fixture
def mock_settings():
    """Mock settings with test values."""
    settings = MagicMock()
    settings.environment = "test"
    settings.debug = True
    settings.is_development = True
    settings.is_production = False
    settings.is_staging = False
    settings.rate_limit_requests = 100
    settings.rate_limit_window = 60
    settings.cache_ttl_active_job = 10
    settings.cache_ttl_completed_job = 3600
    settings.log_level = "DEBUG"
    settings.cors_origins = ["http://localhost:3000"]
    settings.database_url = "sqlite+aiosqlite:///:memory:"
    settings.redis_url = "redis://localhost:6379/0"
    return settings


@pytest.fixture
def mock_user():
    """Mock authenticated user."""
    user = MagicMock()
    user.user_id = "test-user-123"
    user.email = "test@example.com"
    return user


@pytest.fixture
def client():
    """Create test client with mocked dependencies."""
    with patch("app.core.cache.cache_manager.connect", AsyncMock()):
        with patch("app.core.cache.cache_manager.disconnect", AsyncMock()):
            with patch("app.core.database.init_db", AsyncMock()):
                from app.main import app
                with TestClient(app) as test_client:
                    yield test_client
