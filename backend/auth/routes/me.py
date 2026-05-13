"""
Router for authenticated user profile retrieval.
"""
from fastapi import APIRouter, Depends
from backend.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
):
    """Get the current authenticated user's profile info."""
    from backend.auth.services.auth_service import AuthService
    # Return user data from token + session
    return {
        "id": current_user["user_id"],
        "email": current_user["email"],
        "roles": current_user.get("roles", []),
    }
