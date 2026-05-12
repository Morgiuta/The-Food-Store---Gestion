import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import create_access_token

pytestmark = pytest.mark.asyncio


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


def make_admin_token() -> str:
    return create_access_token({
        "sub": "1",
        "email": "admin@test.com",
        "roles": ["ADMIN", "CLIENT"],
    })


def make_client_token(user_id: int = 2, email: str = "client@test.com") -> str:
    return create_access_token({
        "sub": str(user_id),
        "email": email,
        "roles": ["CLIENT"],
    })


class TestAssignRole:
    async def test_assign_role_admin_only(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "client@test.com", roles=["CLIENT"])
        user = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = make_client_token(user_id=2, email="client@test.com")
        response = await client.post(
            f"/api/v1/admin/usuarios/{user.id}/roles",
            json={"rol_nombre": "STOCK"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    async def test_assign_role_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        target = await create_user(session, "target@test.com", roles=["CLIENT"])

        token = create_access_token({
            "sub": str(target.id),
            "email": "admin@test.com",
            "roles": ["ADMIN", "CLIENT"],
        })
        response = await client.post(
            f"/api/v1/admin/usuarios/{target.id}/roles",
            json={"rol_nombre": "STOCK"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "target@test.com"

        from backend.auth.models.usuario_rol import UsuarioRol
        from sqlalchemy.orm import selectinload
        stmt = (
            select(UsuarioRol)
            .where(UsuarioRol.usuario_id == target.id)
            .options(selectinload(UsuarioRol.rol))
        )
        result = await session.execute(stmt)
        assigned = result.scalars().all()
        assigned_names = [ur.rol.nombre for ur in assigned]
        assert "STOCK" in assigned_names
        assert "CLIENT" in assigned_names

    async def test_assign_role_already_assigned(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        user = await create_user(session, "target2@test.com", roles=["CLIENT", "STOCK"])

        token = make_admin_token()
        response = await client.post(
            f"/api/v1/admin/usuarios/{user.id}/roles",
            json={"rol_nombre": "STOCK"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 409
        data = response.json()
        assert "ya tiene el rol" in data["detail"].lower()

    async def test_assign_role_invalid_rol(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        user = await create_user(session, "target3@test.com", roles=["CLIENT"])

        token = make_admin_token()
        response = await client.post(
            f"/api/v1/admin/usuarios/{user.id}/roles",
            json={"rol_nombre": "SUPER_ADMIN"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "no encontrado" in data["detail"].lower()

    async def test_assign_role_user_not_found(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token()
        response = await client.post(
            "/api/v1/admin/usuarios/9999/roles",
            json={"rol_nombre": "STOCK"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "no encontrado" in data["detail"].lower()

    async def test_assign_role_without_auth(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "target4@test.com", roles=["CLIENT"])

        response = await client.post(
            "/api/v1/admin/usuarios/1/roles",
            json={"rol_nombre": "STOCK"},
        )
        assert response.status_code == 401


class TestRevokeRole:
    async def test_revoke_role_success(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        user = await create_user(session, "revoke@test.com", roles=["CLIENT", "STOCK"])

        token = make_admin_token()
        response = await client.request(
            "DELETE",
            f"/api/v1/admin/usuarios/{user.id}/roles/STOCK",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "revoke@test.com"
        assert "STOCK" not in data["roles"]
        assert "CLIENT" in data["roles"]

    async def test_revoke_last_admin(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        admin_user = await create_user(session, "lonely@admin.com", roles=["ADMIN", "CLIENT"])

        token = make_admin_token()
        response = await client.request(
            "DELETE",
            f"/api/v1/admin/usuarios/{admin_user.id}/roles/ADMIN",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 409
        data = response.json()
        assert "último administrador" in data["detail"].lower()

    async def test_revoke_role_not_assigned(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        user = await create_user(session, "noperms@test.com", roles=["CLIENT"])

        token = make_admin_token()
        response = await client.request(
            "DELETE",
            f"/api/v1/admin/usuarios/{user.id}/roles/STOCK",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        data = response.json()
        assert "no tiene el rol" in data["detail"].lower()

    async def test_revoke_invalid_role_name(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "admin@test.com", roles=["ADMIN", "CLIENT"])
        user = await create_user(session, "badrole@test.com", roles=["CLIENT"])

        token = make_admin_token()
        response = await client.request(
            "DELETE",
            f"/api/v1/admin/usuarios/{user.id}/roles/FAKE_ROLE",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    async def test_revoke_role_without_admin(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        await create_user(session, "client@test.com", roles=["CLIENT"])
        user = await create_user(session, "target@test.com", roles=["CLIENT", "STOCK"])

        token = make_client_token(user_id=2, email="client@test.com")
        response = await client.request(
            "DELETE",
            f"/api/v1/admin/usuarios/{user.id}/roles/STOCK",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    async def test_revoke_role_without_auth(self, client: AsyncClient, session: AsyncSession):
        await seed_roles(session)
        response = await client.request(
            "DELETE",
            "/api/v1/admin/usuarios/1/roles/STOCK",
        )
        assert response.status_code == 401
