from fastapi import APIRouter, Depends, Request

from backend.auth.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from backend.auth.services.auth_service import AuthService
from backend.core.dependencies import DatabaseSession, get_current_user
from backend.core.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/register", response_model=TokenResponse, status_code=201)
@limiter.limit("3/hour")
async def register(
    request: Request, body: RegisterRequest, session: DatabaseSession
):
    """Register a new client user."""
    return await auth_service.register(
        session, body.nombre, body.email, body.password, body.telefono
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/15minutes")
async def login(
    request: Request, body: LoginRequest, session: DatabaseSession
):
    """Authenticate user and return tokens."""
    return await auth_service.login(session, body.email, body.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, session: DatabaseSession):
    """Rotate refresh token."""
    return await auth_service.refresh_token(session, body.refresh_token)


@router.post("/logout", status_code=204)
async def logout(
    body: RefreshRequest,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Invalidate refresh token."""
    await auth_service.logout(session, body.refresh_token)
