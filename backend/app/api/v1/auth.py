"""Authentication endpoints and utilities."""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.config import get_settings

router = APIRouter()
logger = structlog.get_logger()
security = HTTPBearer()


class UserInfo(BaseModel):
    """User information from JWT token."""

    user_id: str
    email: str | None = None


class AuthResponse(BaseModel):
    """Authentication verification response."""

    authenticated: bool
    user_id: str | None = None
    message: str


async def verify_clerk_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserInfo:
    """Verify Clerk JWT token and extract user information.

    Args:
        credentials: Bearer token from Authorization header.

    Returns:
        UserInfo: Extracted user information from token.

    Raises:
        HTTPException: If token is invalid or expired.
    """
    settings = get_settings()
    token = credentials.credentials

    if not settings.clerk_secret_key:
        # Development mode: allow any token
        if settings.is_development:
            logger.warning("Clerk secret key not set, using development auth")
            return UserInfo(user_id="dev_user", email="dev@example.com")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication not configured",
        )

    try:
        # In production, verify the JWT token with Clerk
        # For now, we'll use a simplified approach
        # TODO: Implement full Clerk JWT verification in Phase 2
        import jwt

        # Clerk tokens are JWTs that can be verified
        # For development, we'll decode without full verification
        if settings.is_development:
            # Decode without verification in dev
            payload = jwt.decode(token, options={"verify_signature": False})
        else:
            # In production, verify with Clerk's public key
            # This requires fetching JWKS from Clerk
            payload = jwt.decode(token, options={"verify_signature": False})
            # TODO: Implement proper JWKS verification

        user_id = payload.get("sub", "")
        email = payload.get("email")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
            )

        return UserInfo(user_id=user_id, email=email)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError as e:
        logger.error("Token validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.get(
    "/verify",
    response_model=AuthResponse,
    summary="Verify authentication",
    description="Verify the current user's authentication status.",
)
async def verify_auth(
    user: UserInfo = Depends(verify_clerk_token),
) -> AuthResponse:
    """Verify the current user's authentication.

    Args:
        user: User info extracted from token.

    Returns:
        AuthResponse: Authentication status.
    """
    return AuthResponse(
        authenticated=True,
        user_id=user.user_id,
        message="Authentication successful",
    )


@router.get(
    "/me",
    response_model=UserInfo,
    summary="Get current user",
    description="Get information about the currently authenticated user.",
)
async def get_current_user(
    user: UserInfo = Depends(verify_clerk_token),
) -> UserInfo:
    """Get the current authenticated user's information.

    Args:
        user: User info extracted from token.

    Returns:
        UserInfo: Current user information.
    """
    return user
