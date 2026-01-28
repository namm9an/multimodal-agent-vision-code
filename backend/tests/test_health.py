"""Tests for health endpoint."""

import pytest


class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    def test_health_check(self, client):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
