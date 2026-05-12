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
    from backend.auth.models.rol import Rol
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


async def login(client: AsyncClient, email: str, password: str = "password123") -> dict:
    resp = await client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password,
    })
    return resp.json()


class TestGetPerfil:
    async def test_get_perfil(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "user@test.com", roles=["CLIENT"])

        tokens = await login(client, "user@test.com")
        response = await client.get(
            "/api/v1/perfil",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "user@test.com"
        assert data["nombre"] == "Test User"
        assert data["telefono"] == "1234567890"
        assert "CLIENT" in data["roles"]
        assert "id" in data
        assert "creado_en" in data
        assert "actualizado_en" in data

    async def test_get_perfil_unauthorized(self, client: AsyncClient, session: AsyncSession):
        response = await client.get("/api/v1/perfil")
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    async def test_get_perfil_invalid_token(self, client: AsyncClient, session: AsyncSession):
        response = await client.get(
            "/api/v1/perfil",
            headers={"Authorization": "Bearer invalid-token-here"},
        )
        assert response.status_code == 401


class TestUpdatePerfil:
    async def test_update_perfil(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "user@test.com", roles=["CLIENT"])

        tokens = await login(client, "user@test.com")
        response = await client.put(
            "/api/v1/perfil",
            json={"nombre": "Updated Name"},
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Updated Name"
        assert data["email"] == "user@test.com"

    async def test_update_perfil_email(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "user@test.com", roles=["CLIENT"])

        tokens = await login(client, "user@test.com")
        response = await client.put(
            "/api/v1/perfil",
            json={"email": "newemail@test.com"},
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@test.com"

    async def test_update_perfil_unauthorized(self, client: AsyncClient, session: AsyncSession):
        response = await client.put(
            "/api/v1/perfil",
            json={"nombre": "Hacker"},
        )
        assert response.status_code == 401


class TestChangePassword:
    async def test_change_password_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "user@test.com", password="current1234", roles=["CLIENT"])

        tokens = await login(client, "user@test.com", password="current1234")
        response = await client.put(
            "/api/v1/perfil/password",
            json={"password_actual": "current1234", "password_nueva": "newpass1234"},
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert response.status_code == 204
        assert response.text == ""

    async def test_change_password_wrong_current(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "user@test.com", password="current1234", roles=["CLIENT"])

        tokens = await login(client, "user@test.com", password="current1234")
        response = await client.put(
            "/api/v1/perfil/password",
            json={"password_actual": "wrongpassword", "password_nueva": "newpass1234"},
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert response.status_code == 401
        data = response.json()
        assert "incorrecta" in data["detail"].lower()

    async def test_change_password_weak_new(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "user@test.com", password="current1234", roles=["CLIENT"])

        tokens = await login(client, "user@test.com", password="current1234")
        response = await client.put(
            "/api/v1/perfil/password",
            json={"password_actual": "current1234", "password_nueva": "short"},
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert response.status_code == 422

    async def test_change_password_unauthorized(self, client: AsyncClient, session: AsyncSession):
        response = await client.put(
            "/api/v1/perfil/password",
            json={"password_actual": "anything", "password_nueva": "newpass1234"},
        )
        assert response.status_code == 401

    async def test_change_password_invalidates_refresh(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "user@test.com", password="current1234", roles=["CLIENT"])

        tokens = await login(client, "user@test.com", password="current1234")

        await client.put(
            "/api/v1/perfil/password",
            json={"password_actual": "current1234", "password_nueva": "newpass1234"},
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )

        refresh_resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": tokens["refresh_token"],
        })
        assert refresh_resp.status_code == 401
        data = refresh_resp.json()
        assert "Token inválido" in data["detail"]
