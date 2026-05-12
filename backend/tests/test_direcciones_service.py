import pytest
import pytest_asyncio
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


class TestDireccionService:
    """Tests para DireccionService"""

    async def test_create_first_address_is_default(self, session: AsyncSession):
        """Verificar que la primera dirección se marca como predeterminada"""
        from backend.direcciones.services.direccion_service import DireccionService

        user = await create_test_user(session)
        service = DireccionService()

        data = {
            "calle": "Calle Nueva",
            "numero": "123",
            "ciudad": "Ciudad",
            "codigo_postal": "1234",
        }

        direccion = await service.create(session, user.id, data)

        assert direccion.es_predeterminada is True

    async def test_create_subsequent_address_not_default(self, session: AsyncSession):
        """Verificar que las direcciones siguientes no son predeterminadas"""
        from backend.direcciones.services.direccion_service import DireccionService

        user = await create_test_user(session)
        service = DireccionService()

        # Primera dirección
        await service.create(session, user.id, {
            "calle": "Calle 1",
            "numero": "1",
            "ciudad": "Ciudad",
            "codigo_postal": "1234",
        })

        # Segunda dirección
        segunda = await service.create(session, user.id, {
            "calle": "Calle 2",
            "numero": "2",
            "ciudad": "Ciudad",
            "codigo_postal": "1234",
        })

        assert segunda.es_predeterminada is False

    async def test_get_by_id_validates_ownership(self, session: AsyncSession):
        """Verificar que get_by_id valida ownership"""
        from backend.direcciones.services.direccion_service import DireccionService
        from backend.core.exceptions import NotFoundException

        user1 = await create_test_user(session, "user1@test.com")
        user2 = await create_test_user(session, "user2@test.com")
        service = DireccionService()

        # Crear dirección para user1
        direccion = await service.create(session, user1.id, {
            "calle": "Calle Test",
            "numero": "123",
            "ciudad": "Ciudad",
            "codigo_postal": "1234",
        })

        # Intentar acceder como user2
        with pytest.raises(NotFoundException):
            await service.get_by_id(session, direccion.id, user2.id)

    async def test_delete_removes_address(self, session: AsyncSession):
        """Verificar que delete hace soft delete"""
        from backend.direcciones.services.direccion_service import DireccionService

        user = await create_test_user(session)
        service = DireccionService()

        direccion = await service.create(session, user.id, {
            "calle": "Calle Test",
            "numero": "123",
            "ciudad": "Ciudad",
            "codigo_postal": "1234",
        })

        await service.delete(session, direccion.id, user.id)

        # Verificar que ya no se puede acceder
        from backend.core.exceptions import NotFoundException
        with pytest.raises(NotFoundException):
            await service.get_by_id(session, direccion.id, user.id)

    async def test_set_predeterminada_changes_default(self, session: AsyncSession):
        """Verificar que set_predeterminada cambia la dirección predeterminada"""
        from backend.direcciones.services.direccion_service import DireccionService

        user = await create_test_user(session)
        service = DireccionService()

        dir1 = await service.create(session, user.id, {
            "calle": "Calle 1",
            "numero": "1",
            "ciudad": "Ciudad",
            "codigo_postal": "1234",
        })

        dir2 = await service.create(session, user.id, {
            "calle": "Calle 2",
            "numero": "2",
            "ciudad": "Ciudad",
            "codigo_postal": "1234",
        })

        await service.set_predeterminada(session, dir2.id, user.id)

        # Verificar cambios
        from backend.direcciones.repositories.direccion_repository import DireccionRepository
        repo = DireccionRepository(session)

        predeterminada = await repo.get_predeterminada(user.id)
        assert predeterminada.id == dir2.id