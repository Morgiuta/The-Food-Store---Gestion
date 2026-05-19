from backend.auth.models.direccion import DireccionEntrega
from backend.core.exceptions import NotFoundException
from backend.direcciones.repositories.direccion_repository import DireccionRepository


class DireccionService:

    async def list_by_user(
        self, session, usuario_id: int, skip: int = 0, limit: int = 100
    ) -> list[DireccionEntrega]:
        repo = DireccionRepository(session)
        return await repo.get_by_user(usuario_id, skip=skip, limit=limit)

    async def count_by_user(self, session, usuario_id: int) -> int:
        repo = DireccionRepository(session)
        return await repo.get_by_user_count(usuario_id)

    async def get_by_id(self, session, direccion_id: int, usuario_id: int) -> DireccionEntrega:
        repo = DireccionRepository(session)
        direccion = await repo.get_by_id_and_user(direccion_id, usuario_id)
        if not direccion:
            raise NotFoundException("Dirección no encontrada")
        return direccion

    async def create(self, session, usuario_id: int, data: dict) -> DireccionEntrega:
        repo = DireccionRepository(session)
        # Check if this is the first address for this user
        count = await repo.get_by_user_count(usuario_id)
        data["usuario_id"] = usuario_id
        data["es_predeterminada"] = count == 0  # First address is default
        direccion = DireccionEntrega(**data)
        created = await repo.create(direccion)
        await session.commit()
        return created

    async def update(
        self, session, direccion_id: int, usuario_id: int, data: dict
    ) -> DireccionEntrega:
        repo = DireccionRepository(session)
        existing = await repo.get_by_id_and_user(direccion_id, usuario_id)
        if not existing:
            raise NotFoundException("Dirección no encontrada")
        updated = await repo.update(direccion_id, data)
        await session.commit()
        return updated

    async def delete(self, session, direccion_id: int, usuario_id: int) -> None:
        repo = DireccionRepository(session)
        existing = await repo.get_by_id_and_user(direccion_id, usuario_id)
        if not existing:
            raise NotFoundException("Dirección no encontrada")
        await repo.soft_delete(direccion_id)
        await session.commit()

    async def set_predeterminada(
        self, session, direccion_id: int, usuario_id: int
    ) -> DireccionEntrega:
        repo = DireccionRepository(session)
        existing = await repo.get_by_id_and_user(direccion_id, usuario_id)
        if not existing:
            raise NotFoundException("Dirección no encontrada")
        updated = await repo.set_predeterminada(direccion_id, usuario_id)
        await session.commit()
        return updated
