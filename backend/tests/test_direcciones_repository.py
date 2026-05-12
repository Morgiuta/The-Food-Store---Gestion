import pytest
import pytest_asyncio
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def disable_rate_limiting():
    from backend.auth.routes.auth import limiter as auth_limiter
    auth_limiter.enabled = False
    yield
    auth_limiter.enabled = True


async def create_test_user(session: AsyncSession, email: str = "test@test.com"):
    from backend.auth.models.usuario import Usuario
    from backend.core.security import get_password_hash

    user = Usuario(
        nombre="Test User",
        email=email,
        password_hash=get_password_hash("password123"),
        telefono="1234567890",
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def create_test_direccion(session: AsyncSession, usuario_id: int, es_predeterminada: bool = False):
    from backend.auth.models.direccion import DireccionEntrega

    direccion = DireccionEntrega(
        usuario_id=usuario_id,
        calle="Calle Test",
        numero="123",
        ciudad="Ciudad Test",
        codigo_postal="1234",
        es_predeterminada=es_predeterminada,
    )
    session.add(direccion)
    await session.flush()
    await session.refresh(direccion)
    return direccion


class TestDireccionRepository:
    """Tests para DireccionRepository"""

    async def test_get_by_user_returns_only_user_direcciones(self, session: AsyncSession):
        """Verificar que get_by_user retorna solo direcciones del usuario"""
        from backend.direcciones.repositories.direccion_repository import DireccionRepository

        # Crear dos usuarios con direcciones
        user1 = await create_test_user(session, "user1@test.com")
        user2 = await create_test_user(session, "user2@test.com")

        await create_test_direccion(session, user1.id)
        await create_test_direccion(session, user2.id)

        repo = DireccionRepository(session)
        direcciones_user1 = await repo.get_by_user(user1.id)

        assert len(direcciones_user1) == 1
        assert direcciones_user1[0].usuario_id == user1.id

    async def test_get_by_user_excludes_soft_deleted(self, session: AsyncSession):
        """Verificar que get_by_user excluye direcciones eliminadas"""
        from backend.auth.models.direccion import DireccionEntrega
        from backend.direcciones.repositories.direccion_repository import DireccionRepository

        user = await create_test_user(session)
        direccion = await create_test_direccion(session, user.id)

        # Soft delete
        direccion.eliminado_en = datetime.now(timezone.utc)
        await session.flush()

        repo = DireccionRepository(session)
        direcciones = await repo.get_by_user(user.id)

        assert len(direcciones) == 0

    async def test_get_predeterminada_returns_default_address(self, session: AsyncSession):
        """Verificar que get_predeterminada retorna la dirección predeterminada"""
        from backend.direcciones.repositories.direccion_repository import DireccionRepository

        user = await create_test_user(session)
        await create_test_direccion(session, user.id, es_predeterminada=True)
        await create_test_direccion(session, user.id, es_predeterminada=False)

        repo = DireccionRepository(session)
        predeterminada = await repo.get_predeterminada(user.id)

        assert predeterminada is not None
        assert predeterminada.es_predeterminada is True

    async def test_set_predeterminada_clears_others(self, session: AsyncSession):
        """Verificar que set_predeterminada quita el flag de las demás"""
        from backend.direcciones.repositories.direccion_repository import DireccionRepository

        user = await create_test_user(session)
        dir1 = await create_test_direccion(session, user.id, es_predeterminada=True)
        dir2 = await create_test_direccion(session, user.id, es_predeterminada=False)

        repo = DireccionRepository(session)
        await repo.set_predeterminada(dir2.id, user.id)

        # Verificar que dir1 ya no es predeterminada
        await session.refresh(dir1)
        assert dir1.es_predeterminada is False

        # Verificar que dir2 ahora es predeterminada
        await session.refresh(dir2)
        assert dir2.es_predeterminada is True

    async def test_soft_delete_sets_eliminado_en(self, session: AsyncSession):
        """Verificar que soft_delete establece eliminado_en"""
        from backend.direcciones.repositories.direccion_repository import DireccionRepository

        user = await create_test_user(session)
        direccion = await create_test_direccion(session, user.id)

        repo = DireccionRepository(session)
        await repo.soft_delete(direccion.id)
        await session.refresh(direccion)

        assert direccion.eliminado_en is not None