"""Health check endpoints."""

from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter()
logger = structlog.get_logger()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: str
    version: str = "0.1.0"


class ReadinessResponse(BaseModel):
    """Readiness check response model."""

    status: str
    database: str
    timestamp: str


@router.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Simple health check endpoint to verify the API is running.",
)
async def health_check() -> HealthResponse:
    """Check if the API is healthy.

    Returns:
        HealthResponse: Health status of the API.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get(
    "/readyz",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness check",
    description="Check if the API is ready to serve requests (database connected).",
)
async def readiness_check(
    db: AsyncSession = Depends(get_db),
) -> ReadinessResponse:
    """Check if the API is ready to serve requests.

    This includes checking database connectivity.

    Args:
        db: Database session dependency.

    Returns:
        ReadinessResponse: Readiness status including database status.
    """
    db_status = "connected"

    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error("Database connection failed", error=str(e))
        db_status = "disconnected"

    return ReadinessResponse(
        status="ready" if db_status == "connected" else "not_ready",
        database=db_status,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
