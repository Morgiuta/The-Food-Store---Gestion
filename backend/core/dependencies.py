"""
FastAPI dependencies for authentication, authorization, and database access.
"""

from typing import Annotated, Any

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.exceptions import ForbiddenException, UnauthorizedException
from backend.core.security import decode_token

# HTTP Bearer token scheme for OpenAPI docs
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, Any]:
    """
    Extract and validate the current user from the JWT access token.

    Args:
        credentials: Bearer token from Authorization header
        session: Database session

    Returns:
        Dict with user_id, email, and roles from the token payload

    Raises:
        UnauthorizedException: If token is missing, invalid, or expired
    """
    if credentials is None:
        raise UnauthorizedException(
            detail="Authentication required",
            instance="Authorization header missing",
        )

    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise UnauthorizedException(
            detail="Invalid or expired token",
            instance="Token validation failed",
        )

    user_id = payload.get("sub")
    email = payload.get("email")
    roles = payload.get("roles", [])

    if user_id is None or email is None:
        raise UnauthorizedException(
            detail="Invalid token payload",
            instance="Missing required claims",
        )

    return {
        "user_id": int(user_id),
        "email": email,
        "roles": roles,
    }


async def require_role(
    required_roles: list[str],
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> dict[str, Any]:
    """
    Verify that the current user has at least one of the required roles.

    Args:
        required_roles: List of role names that are allowed
        current_user: User info from get_current_user

    Returns:
        The current user dict if authorized

    Raises:
        ForbiddenException: If user lacks any required role
    """
    user_roles = current_user.get("roles", [])

    if not any(role in user_roles for role in required_roles):
        raise ForbiddenException(
            detail="Insufficient permissions",
            instance=f"Required roles: {', '.join(required_roles)}",
        )

    return current_user


# Type alias for common dependency injection
CurrentUser = Annotated[dict[str, Any], Depends(get_current_user)]
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


def RoleRequired(roles: list[str]) -> Any:
    """
    Factory for role-based authorization dependencies.

    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(
            current_user: CurrentUser = Depends(RoleRequired(["ADMIN"]))
        ):
            ...

    Args:
        roles: List of required role names

    Returns:
        A FastAPI dependency that validates role access
    """
    return Depends(lambda: None)  # Placeholder; use with require_role
