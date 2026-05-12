import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import create_access_token

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


def make_admin_token(user_id: int = 1, email: str = "admin@test.com") -> str:
    return create_access_token({
        "sub": str(user_id),
        "email": email,
        "roles": ["ADMIN", "CLIENT"],
    })


def make_client_token(user_id: int = 2, email: str = "client@test.com") -> str:
    return create_access_token({
        "sub": str(user_id),
        "email": email,
        "roles": ["CLIENT"],
    })


class TestListUsuarios:
    async def test_list_usuarios_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        await create_user(session, "user1@test.com", roles=["CLIENT"])
        await create_user(session, "user2@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id, email="admin@test.com")
        response = await client.get(
            "/api/v1/admin/usuarios",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 3
        assert len(data["items"]) == 3

    async def test_list_usuarios_unauthorized(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "client@test.com", roles=["CLIENT"])

        token = make_client_token(user_id=user.id)
        response = await client.get(
            "/api/v1/admin/usuarios",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    async def test_list_usuarios_without_auth(self, client: AsyncClient, session: AsyncSession):
        response = await client.get("/api/v1/admin/usuarios")
        assert response.status_code == 401

    async def test_list_usuarios_search(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        await create_user(session, "john@test.com", roles=["CLIENT"])
        await create_user(session, "jane@test.com", roles=["CLIENT"])
        await create_user(session, "other@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.get(
            "/api/v1/admin/usuarios?search=john",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["email"] == "john@test.com"

    async def test_list_usuarios_rol_filter(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        await create_user(session, "stock1@test.com", roles=["STOCK", "CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.get(
            "/api/v1/admin/usuarios?rol=STOCK",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["email"] == "stock1@test.com"

    async def test_list_usuarios_pagination(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        for i in range(5):
            await create_user(session, f"user{i}@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.get(
            "/api/v1/admin/usuarios?skip=0&limit=2",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 6
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["limit"] == 2


class TestGetUsuario:
    async def test_get_usuario_detail(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.get(
            f"/api/v1/admin/usuarios/{target.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "target@test.com"
        assert data["nombre"] == "Test User"
        assert data["telefono"] == "1234567890"
        assert "CLIENT" in data["roles"]
        assert "id" in data
        assert "creado_en" in data
        assert "actualizado_en" in data

    async def test_get_usuario_not_found(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.get(
            "/api/v1/admin/usuarios/9999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "no encontrado" in data["detail"].lower()

    async def test_get_usuario_unauthorized(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "client@test.com", roles=["CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_client_token(user_id=user.id)
        response = await client.get(
            f"/api/v1/admin/usuarios/{target.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403


class TestUpdateUsuario:
    async def test_update_usuario(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.put(
            f"/api/v1/admin/usuarios/{target.id}",
            json={"nombre": "Updated Name", "telefono": "9999999999"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Updated Name"
        assert data["telefono"] == "9999999999"
        assert data["email"] == "target@test.com"

    async def test_update_usuario_not_found(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.put(
            "/api/v1/admin/usuarios/9999",
            json={"nombre": "Nobody"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    async def test_update_usuario_roles(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.put(
            f"/api/v1/admin/usuarios/{target.id}",
            json={"roles": ["CLIENT", "STOCK"]},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        stmt = select(UsuarioRol).where(UsuarioRol.usuario_id == target.id)
        result = await session.execute(stmt)
        assigned = result.scalars().all()
        assigned_names = []
        for ur in assigned:
            rol_stmt = select(Rol).where(Rol.id == ur.rol_id)
            rol_result = await session.execute(rol_stmt)
            assigned_names.append(rol_result.scalar_one().nombre)
        assert "STOCK" in assigned_names
        assert "CLIENT" in assigned_names

    async def test_update_usuario_remove_last_admin(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.put(
            f"/api/v1/admin/usuarios/{admin.id}",
            json={"roles": ["CLIENT"]},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 409
        data = response.json()
        assert "último administrador" in data["detail"].lower()


class TestToggleEstado:
    async def test_toggle_estado_desactivar(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.patch(
            f"/api/v1/admin/usuarios/{target.id}/estado",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["eliminado_en"] is not None

    async def test_toggle_estado_activar(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_admin_token(user_id=admin.id)

        resp1 = await client.patch(
            f"/api/v1/admin/usuarios/{target.id}/estado",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp1.status_code == 200
        assert resp1.json()["eliminado_en"] is not None

        resp2 = await client.patch(
            f"/api/v1/admin/usuarios/{target.id}/estado",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp2.status_code == 200
        assert resp2.json()["eliminado_en"] is None

    async def test_toggle_estado_self(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.patch(
            f"/api/v1/admin/usuarios/{admin.id}/estado",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        data = response.json()
        assert "tu propia cuenta" in data["detail"].lower()

    async def test_toggle_estado_last_admin(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "lonely@admin.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token(user_id=admin.id, email="lonely@admin.com")
        response = await client.patch(
            f"/api/v1/admin/usuarios/{admin.id}/estado",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    async def test_toggle_estado_not_found(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token(user_id=admin.id)
        response = await client.patch(
            "/api/v1/admin/usuarios/9999/estado",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    async def test_toggle_estado_unauthorized(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        user = await create_user(session, "client@test.com", roles=["CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_client_token(user_id=user.id)
        response = await client.patch(
            f"/api/v1/admin/usuarios/{target.id}/estado",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    async def test_login_desactivated_user(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin = await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        admin_token = make_admin_token(user_id=admin.id)
        await client.patch(
            f"/api/v1/admin/usuarios/{target.id}/estado",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "target@test.com",
            "password": "password123",
        })
        assert login_resp.status_code == 403
        data = login_resp.json()
        assert "desactivada" in data["detail"].lower()
