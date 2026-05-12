import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def disable_rate_limiting():
    from backend.auth.routes.auth import limiter as auth_limiter
    auth_limiter.enabled = False
    yield
    auth_limiter.enabled = True


async def seed_roles(session: AsyncSession):
    from backend.auth.models.rol import Rol
    roles = [
        Rol(nombre="ADMIN", descripcion="Acceso total al sistema"),
        Rol(nombre="STOCK", descripcion="Gestión de inventario y productos"),
        Rol(nombre="PEDIDOS", descripcion="Gestión de pedidos"),
        Rol(nombre="CLIENT", descripcion="Usuario cliente"),
    ]
    session.add_all(roles)
    await session.flush()


async def create_user(
    session: AsyncSession,
    email: str,
    password: str = "password123",
    roles: list[str] | None = None,
):
    from backend.auth.models.usuario import Usuario
    from backend.auth.models.usuario_rol import UsuarioRol
    from backend.core.security import get_password_hash

    user = Usuario(
        nombre="Test User",
        email=email,
        password_hash=get_password_hash(password),
        telefono="1234567890",
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)

    if roles:
        for rol_name in roles:
            stmt = select(Rol).where(Rol.nombre == rol_name)
            result = await session.execute(stmt)
            rol = result.scalar_one()
            ur = UsuarioRol(usuario_id=user.id, rol_id=rol.id)
            session.add(ur)
        await session.flush()

    return user


class TestRegister:
    async def test_register_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        response = await client.post("/api/v1/auth/register", json={
            "nombre": "New User",
            "email": "newuser@example.com",
            "password": "securepass123",
            "telefono": "0987654321",
        })
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["nombre"] == "New User"
        assert data["user"]["telefono"] == "0987654321"
        assert "CLIENT" in data["user"]["roles"]
        assert len(data["user"]["roles"]) == 1
        assert data["user"]["id"] is not None

    async def test_register_duplicate_email(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "dup@example.com")
        response = await client.post("/api/v1/auth/register", json={
            "nombre": "Dup User",
            "email": "dup@example.com",
            "password": "securepass123",
        })
        assert response.status_code == 409
        data = response.json()
        assert "registrado" in data["detail"].lower()

    async def test_register_weak_password(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        response = await client.post("/api/v1/auth/register", json={
            "nombre": "Weak",
            "email": "weak@example.com",
            "password": "short",
        })
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert len(data["detail"]) > 0

    async def test_register_missing_fields(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        response = await client.post("/api/v1/auth/register", json={
            "email": "missing@example.com",
        })
        assert response.status_code == 422

    async def test_register_invalid_email(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        response = await client.post("/api/v1/auth/register", json={
            "nombre": "Bad Email",
            "email": "not-an-email",
            "password": "securepass123",
        })
        assert response.status_code == 422


class TestLogin:
    async def test_login_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "logintest@example.com")
        response = await client.post("/api/v1/auth/login", json={
            "email": "logintest@example.com",
            "password": "password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "logintest@example.com"
        assert data["user"]["nombre"] == "Test User"

    async def test_login_invalid_email(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        response = await client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "password123",
        })
        assert response.status_code == 401
        data = response.json()
        assert "Email o contraseña incorrectos" in data["detail"]

    async def test_login_wrong_password(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "wrongpwd@example.com")
        response = await client.post("/api/v1/auth/login", json={
            "email": "wrongpwd@example.com",
            "password": "wrongpassword123",
        })
        assert response.status_code == 401
        data = response.json()
        assert "Email o contraseña incorrectos" in data["detail"]

    async def test_login_empty_password(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        response = await client.post("/api/v1/auth/login", json={
            "email": "any@example.com",
            "password": "",
        })
        assert response.status_code == 422


class TestRefresh:
    async def test_refresh_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "refresh@example.com")
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "refresh@example.com",
            "password": "password123",
        })
        assert login_resp.status_code == 200
        old_refresh = login_resp.json()["refresh_token"]

        refresh_resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": old_refresh,
        })
        assert refresh_resp.status_code == 200
        data = refresh_resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["refresh_token"] != old_refresh
        assert data["user"]["email"] == "refresh@example.com"

    async def test_refresh_invalid_token(self, client: AsyncClient, session: AsyncSession):
        response = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": "garbage-token-that-does-not-exist",
        })
        assert response.status_code == 401
        data = response.json()
        assert "Token inválido" in data["detail"]

    async def test_refresh_empty_token(self, client: AsyncClient, session: AsyncSession):
        response = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": "",
        })
        assert response.status_code == 401
        data = response.json()
        assert "Token inválido" in data["detail"]

    async def test_refresh_revoked_token(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "replay@example.com")
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "replay@example.com",
            "password": "password123",
        })
        assert login_resp.status_code == 200
        refresh_token = login_resp.json()["refresh_token"]

        resp1 = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token,
        })
        assert resp1.status_code == 200

        resp2 = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token,
        })
        assert resp2.status_code == 401
        data = resp2.json()
        assert "Token inválido" in data["detail"]


class TestLogout:
    async def test_logout_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "logout@example.com")
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "logout@example.com",
            "password": "password123",
        })
        assert login_resp.status_code == 200
        data = login_resp.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        logout_resp = await client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": refresh_token},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert logout_resp.status_code == 204

        refresh_resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token,
        })
        assert refresh_resp.status_code == 401

    async def test_logout_without_auth(self, client: AsyncClient, session: AsyncSession):
        response = await client.post("/api/v1/auth/logout", json={
            "refresh_token": "some-token",
        })
        assert response.status_code == 401

    async def test_logout_invalid_token(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "logout2@example.com")
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "logout2@example.com",
            "password": "password123",
        })
        access_token = login_resp.json()["access_token"]

        response = await client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": "nonexistent-token"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 204
        assert response.text == ""


class TestFullAuthFlow:
    async def test_full_auth_flow(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)

        reg_resp = await client.post("/api/v1/auth/register", json={
            "nombre": "Full Flow",
            "email": "fullflow@example.com",
            "password": "securepass123",
        })
        assert reg_resp.status_code == 201
        reg_data = reg_resp.json()
        assert "access_token" in reg_data

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "fullflow@example.com",
            "password": "securepass123",
        })
        assert login_resp.status_code == 200
        login_data = login_resp.json()
        access_token = login_data["access_token"]
        refresh_token = login_data["refresh_token"]

        refresh_resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token,
        })
        assert refresh_resp.status_code == 200
        refresh_data = refresh_resp.json()
        new_access = refresh_data["access_token"]
        new_refresh = refresh_data["refresh_token"]
        assert new_refresh != refresh_token

        logout_resp = await client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": new_refresh},
            headers={"Authorization": f"Bearer {new_access}"},
        )
        assert logout_resp.status_code == 204

        login2_resp = await client.post("/api/v1/auth/login", json={
            "email": "fullflow@example.com",
            "password": "securepass123",
        })
        assert login2_resp.status_code == 200

        login2_data = login2_resp.json()
        assert login2_data["user"]["email"] == "fullflow@example.com"
        assert "CLIENT" in login2_data["user"]["roles"]
