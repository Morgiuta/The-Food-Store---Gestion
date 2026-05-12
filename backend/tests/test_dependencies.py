import pytest
from fastapi.security import HTTPAuthorizationCredentials

from backend.core.dependencies import get_current_user, require_role
from backend.core.exceptions import ForbiddenException, UnauthorizedException
from backend.core.security import create_access_token


class TestGetCurrentUser:
    async def test_with_valid_token_returns_user_dict(self, session):
        token = create_access_token({
            "sub": "1",
            "email": "test@test.com",
            "roles": ["ADMIN"],
        })
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        result = await get_current_user(creds, session)
        assert result == {
            "user_id": 1,
            "email": "test@test.com",
            "roles": ["ADMIN"],
        }

    async def test_with_valid_token_and_multiple_roles(self, session):
        token = create_access_token({
            "sub": "2",
            "email": "multi@test.com",
            "roles": ["STOCK", "PEDIDOS"],
        })
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        result = await get_current_user(creds, session)
        assert result["user_id"] == 2
        assert result["roles"] == ["STOCK", "PEDIDOS"]

    async def test_with_missing_token_raises_unauthorized(self, session):
        with pytest.raises(UnauthorizedException) as exc_info:
            await get_current_user(None, session)
        assert "Authentication required" in str(exc_info.value.detail)

    async def test_with_invalid_token_raises_unauthorized(self, session):
        creds = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid.token.here",
        )
        with pytest.raises(UnauthorizedException) as exc_info:
            await get_current_user(creds, session)
        assert "Invalid or expired token" in str(exc_info.value.detail)

    async def test_with_token_missing_sub_raises_unauthorized(self, session):
        token = create_access_token({"email": "test@test.com"})
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        with pytest.raises(UnauthorizedException) as exc_info:
            await get_current_user(creds, session)
        assert "Invalid token payload" in str(exc_info.value.detail)


class TestRequireRole:
    async def test_with_sufficient_roles_passes(self):
        user = {
            "user_id": 1,
            "email": "admin@test.com",
            "roles": ["ADMIN", "STOCK"],
        }
        result = await require_role(["ADMIN"], user)
        assert result == user

    async def test_with_any_one_of_required_roles_passes(self):
        user = {
            "user_id": 1,
            "email": "stock@test.com",
            "roles": ["STOCK"],
        }
        result = await require_role(["ADMIN", "STOCK"], user)
        assert result == user

    async def test_with_insufficient_roles_raises_forbidden(self):
        user = {
            "user_id": 1,
            "email": "client@test.com",
            "roles": ["CLIENT"],
        }
        with pytest.raises(ForbiddenException) as exc_info:
            await require_role(["ADMIN"], user)
        assert "Insufficient permissions" in str(exc_info.value.detail)

    async def test_with_empty_roles_raises_forbidden(self):
        user = {
            "user_id": 1,
            "email": "noroles@test.com",
            "roles": [],
        }
        with pytest.raises(ForbiddenException) as exc_info:
            await require_role(["ADMIN"], user)
        assert "Insufficient permissions" in str(exc_info.value.detail)
