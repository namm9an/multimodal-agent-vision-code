"""FastAPI application entry point.

Phase 4 Integration:
- Redis cache manager lifecycle
- Global error handlers
- Sentry integration (optional)
- Request ID middleware
"""

import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, files, health, jobs, models
from app.config import get_settings
from app.core.cache import cache_manager
from app.core.database import init_db
from app.core.errors import setup_error_handlers
from app.core.logging import setup_logging
from app.core.rate_limiter import rate_limit_middleware

# Initialize structured logging
setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    settings = get_settings()

    # Startup
    logger.info(
        "Starting application",
        environment=settings.environment,
        debug=settings.debug,
    )

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Initialize Redis cache (Phase 4)
    await cache_manager.connect()

    # Initialize Sentry if DSN provided (Phase 4)
    sentry_dsn = getattr(settings, "sentry_dsn", None)
    if sentry_dsn:
        try:
            import sentry_sdk
            sentry_sdk.init(
                dsn=sentry_dsn,
                environment=settings.environment,
                traces_sample_rate=0.1,
            )
            logger.info("Sentry initialized")
        except ImportError:
            logger.warning("sentry-sdk not installed, skipping Sentry init")

    yield

    # Shutdown
    await cache_manager.disconnect()
    logger.info("Shutting down application")


async def request_id_middleware(request: Request, call_next):
    """Add unique request ID to each request for tracing."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Add to structlog context
    structlog.contextvars.bind_contextvars(request_id=request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title="Multimodal AI Agent API",
        description="API for processing images and generating Python code",
        version="0.1.0",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add request ID middleware (Phase 4)
    app.middleware("http")(request_id_middleware)

    # Add rate limiting middleware (Phase 6)
    app.middleware("http")(rate_limit_middleware)

    # Register global error handlers (Phase 4)
    setup_error_handlers(app)

    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(files.router, prefix="/api/v1/files", tags=["Files"])
    app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
    app.include_router(models.router, prefix="/api/v1/models", tags=["Models"])

    return app


# Create the application instance
app = create_app()

