"""Error handling middleware and exception classes.

This module provides:
- Custom exception classes for different error types
- Global exception handlers for FastAPI
- Structured error responses
- Request ID tracking for debugging

Following Google Python Style Guide.
"""

import traceback
import uuid
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base application error.

    Attributes:
        message: Human-readable error message.
        error_code: Machine-readable error code.
        status_code: HTTP status code.
        details: Additional error context.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize AppError.

        Args:
            message: Error message.
            error_code: Error code for client handling.
            status_code: HTTP status code.
            details: Additional context.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class ValidationError(AppError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class NotFoundError(AppError):
    """Raised when a resource is not found."""

    def __init__(
        self,
        resource: str,
        identifier: str,
    ) -> None:
        super().__init__(
            message=f"{resource} not found: {identifier}",
            error_code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "identifier": identifier},
        )


class AuthenticationError(AppError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication required",
    ) -> None:
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(AppError):
    """Raised when user lacks permission."""

    def __init__(
        self,
        message: str = "Permission denied",
    ) -> None:
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class RateLimitError(AppError):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        retry_after: int = 60,
    ) -> None:
        super().__init__(
            message="Rate limit exceeded. Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after_seconds": retry_after},
        )


class ExternalServiceError(AppError):
    """Raised when an external service fails."""

    def __init__(
        self,
        service: str,
        message: str,
    ) -> None:
        super().__init__(
            message=f"External service error ({service}): {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details={"service": service},
        )


def create_error_response(
    request_id: str,
    error_code: str,
    message: str,
    status_code: int,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    """Create a standardized error response.

    Args:
        request_id: Unique request identifier.
        error_code: Machine-readable error code.
        message: Human-readable message.
        status_code: HTTP status code.
        details: Additional context.

    Returns:
        JSONResponse with structured error body.
    """
    body = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "request_id": request_id,
        },
    }
    if details:
        body["error"]["details"] = details

    return JSONResponse(status_code=status_code, content=body)


async def app_error_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    """Handle AppError exceptions.

    Args:
        request: FastAPI request object.
        exc: The AppError exception.

    Returns:
        Structured error response.
    """
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    logger.warning(
        "Application error",
        request_id=request_id,
        error_code=exc.error_code,
        message=exc.message,
        path=str(request.url.path),
    )

    return create_error_response(
        request_id=request_id,
        error_code=exc.error_code,
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
    )


async def generic_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle uncaught exceptions.

    Args:
        request: FastAPI request object.
        exc: The uncaught exception.

    Returns:
        Generic 500 error response.
    """
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    # Log full traceback for debugging
    logger.error(
        "Unhandled exception",
        request_id=request_id,
        error_type=type(exc).__name__,
        error_message=str(exc),
        path=str(request.url.path),
        traceback=traceback.format_exc(),
    )

    return create_error_response(
        request_id=request_id,
        error_code="INTERNAL_ERROR",
        message="An unexpected error occurred. Please try again later.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def setup_error_handlers(app: FastAPI) -> None:
    """Register error handlers with FastAPI app.

    Args:
        app: FastAPI application instance.
    """
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)

    logger.info("Error handlers registered")
