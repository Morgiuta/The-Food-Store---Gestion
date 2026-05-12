import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def disable_rate_limiting():
    from backend.auth.routes.auth import limiter as auth_limiter
    auth_limiter.enabled = False
    yield
    auth_limiter.enabled = True


async def get_auth_token(client: AsyncClient, email: str = "test@test.com", password: str = "password123") -> str:
    """Helper para obtener token de autenticación"""
    from backend.auth.models.usuario import Usuario
    from backend.auth.models.rol import Rol
    from backend.auth.models.usuario_rol import UsuarioRol
    from backend.core.security import get_password_hash, create_access_token

    # Crear usuario en la DB si no existe
    from sqlalchemy import select
    from backend.core.database import async_session_factory

    async with async_session_factory() as session:
        result = await session.execute(select(Usuario).where(Usuario.email == email))
        user = result.scalar_oneOrNone()

        if not user:
            user = Usuario(
                nombre="Test User",
                email=email,
                password_hash=get_password_hash(password),
                telefono="1234567890",
            )
            session.add(user)
            await session.flush()

            # Asignar rol CLIENT
            result = await session.execute(select(Rol).where(Rol.nombre == "CLIENT"))
            rol = result.scalar_one()
            session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))
            await session.commit()

    token = create_access_token({"sub": email, "id": user.id})
    return token


class TestDireccionesAPI:
    """Tests de integración para endpoints de direcciones"""

    async def test_create_direccion_returns_201(self, client: AsyncClient, session: AsyncSession):
        """Verificar que crear dirección retorna 201"""
        from backend.auth.models.usuario import Usuario
        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        from backend.core.security import get_password_hash
        from backend.core.security import create_access_token

        # Crear usuario
        user = Usuario(
            nombre="Test",
            email="apitest@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user)
        await session.flush()

        result = await session.execute(select(Rol).where(Rol.nombre == "CLIENT"))
        rol = result.scalar_one()
        session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))
        await session.commit()

        token = create_access_token({"sub": user.email, "id": user.id})

        response = await client.post(
            "/api/v1/direcciones",
            json={
                "calle": "Calle Test",
                "numero": "123",
                "ciudad": "Ciudad Test",
                "codigo_postal": "1234",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["calle"] == "Calle Test"
        assert data["es_predeterminada"] is True

    async def test_list_direcciones_requires_auth(self, client: AsyncClient):
        """Verificar que listar direcciones requiere autenticación"""
        response = await client.get("/api/v1/direcciones")
        assert response.status_code == 401

    async def test_list_direcciones_returns_user_addresses(self, client: AsyncClient, session: AsyncSession):
        """Verificar que listar direcciones retorna solo las del usuario"""
        from backend.auth.models.usuario import Usuario
        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        from backend.auth.models.direccion import DireccionEntrega
        from backend.core.security import get_password_hash, create_access_token

        # Crear usuario
        user = Usuario(
            nombre="Test",
            email="listtest@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user)
        await session.flush()

        result = await session.execute(select(Rol).where(Rol.nombre == "CLIENT"))
        rol = result.scalar_one()
        session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))

        # Crear dirección
        direccion = DireccionEntrega(
            usuario_id=user.id,
            calle="Calle Test",
            numero="123",
            ciudad="Ciudad Test",
            codigo_postal="1234",
        )
        session.add(direccion)
        await session.commit()

        token = create_access_token({"sub": user.email, "id": user.id})

        response = await client.get(
            "/api/v1/direcciones",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["calle"] == "Calle Test"

    async def test_update_direccion_ownership_check(self, client: AsyncClient, session: AsyncSession):
        """Verificar que no se puede editar dirección de otro usuario"""
        from backend.auth.models.usuario import Usuario
        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        from backend.auth.models.direccion import DireccionEntrega
        from backend.core.security import get_password_hash, create_access_token

        # Crear dos usuarios
        user1 = Usuario(
            nombre="User1",
            email="user1@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user1)
        await session.flush()

        user2 = Usuario(
            nombre="User2",
            email="user2@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user2)
        await session.flush()

        result = await session.execute(select(Rol).where(Rol.nombre == "CLIENT"))
        rol = result.scalar_one()
        session.add(UsuarioRol(usuario_id=user1.id, rol_id=rol.id))
        session.add(UsuarioRol(usuario_id=user2.id, rol_id=rol.id))

        # Crear dirección para user1
        direccion = DireccionEntrega(
            usuario_id=user1.id,
            calle="Calle User1",
            numero="123",
            ciudad="Ciudad",
            codigo_postal="1234",
        )
        session.add(direccion)
        await session.commit()

        # Intentar editar como user2
        token2 = create_access_token({"sub": user2.email, "id": user2.id})

        response = await client.put(
            f"/api/v1/direcciones/{direccion.id}",
            json={"calle": "Calle Modificada"},
            headers={"Authorization": f"Bearer {token2}"},
        )

        assert response.status_code == 404

    async def test_set_predeterminada(self, client: AsyncClient, session: AsyncSession):
        """Verificar que se puede marcar dirección como predeterminada"""
        from backend.auth.models.usuario import Usuario
        from backend.auth.models.rol import Rol
        from backend.auth.models.usuario_rol import UsuarioRol
        from backend.auth.models.direccion import DireccionEntrega
        from backend.core.security import get_password_hash, create_access_token

        user = Usuario(
            nombre="Test",
            email="predtest@test.com",
            password_hash=get_password_hash("password123"),
            telefono="1234567890",
        )
        session.add(user)
        await session.flush()

        result = await session.execute(select(Rol).where(Rol.nombre == "CLIENT"))
        rol = result.scalar_one()
        session.add(UsuarioRol(usuario_id=user.id, rol_id=rol.id))

        dir1 = DireccionEntrega(
            usuario_id=user.id,
            calle="Calle 1",
            numero="1",
            ciudad="Ciudad",
            codigo_postal="1234",
            es_predeterminada=True,
        )
        dir2 = DireccionEntrega(
            usuario_id=user.id,
            calle="Calle 2",
            numero="2",
            ciudad="Ciudad",
            codigo_postal="1234",
            es_predeterminada=False,
        )
        session.add(dir1)
        session.add(dir2)
        await session.commit()

        token = create_access_token({"sub": user.email, "id": user.id})

        response = await client.post(
            f"/api/v1/direcciones/{dir2.id}/predeterminada",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["es_predeterminada"] is True