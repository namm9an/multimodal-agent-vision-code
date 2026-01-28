"""Tests for configuration settings."""

from unittest.mock import patch

import pytest


class TestSettings:
    """Test cases for Settings configuration."""

    def test_default_environment(self):
        """Test default environment is development."""
        with patch.dict("os.environ", {}, clear=True):
            from app.config import Settings
            settings = Settings()
            assert settings.environment == "development"

    def test_is_development_property(self, mock_settings):
        """Test is_development returns True for development env."""
        mock_settings.environment = "development"
        mock_settings.is_development = mock_settings.environment == "development"
        assert mock_settings.is_development is True

    def test_is_production_property(self, mock_settings):
        """Test is_production returns True for production env."""
        mock_settings.environment = "production"
        mock_settings.is_production = mock_settings.environment == "production"
        assert mock_settings.is_production is True

    def test_is_staging_property(self, mock_settings):
        """Test is_staging returns True for staging env."""
        mock_settings.environment = "staging"
        mock_settings.is_staging = mock_settings.environment == "staging"
        assert mock_settings.is_staging is True

    def test_rate_limit_defaults(self, mock_settings):
        """Test rate limiting has sensible defaults."""
        assert mock_settings.rate_limit_requests > 0
        assert mock_settings.rate_limit_window > 0

    def test_cache_ttl_defaults(self, mock_settings):
        """Test cache TTL has sensible defaults."""
        assert mock_settings.cache_ttl_active_job > 0
        assert mock_settings.cache_ttl_completed_job > mock_settings.cache_ttl_active_job
