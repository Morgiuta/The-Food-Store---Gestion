from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.models.direccion import DireccionEntrega
from backend.core.base_repository import BaseRepository


class DireccionRepository(BaseRepository[DireccionEntrega]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DireccionEntrega)

    async def get_by_user(
        self, usuario_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[DireccionEntrega]:
        stmt = (
            select(DireccionEntrega)
            .where(
                DireccionEntrega.usuario_id == usuario_id,
                DireccionEntrega.eliminado_en.is_(None),
            )
            .order_by(DireccionEntrega.es_predeterminada.desc(), DireccionEntrega.creado_en.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_user_count(self, usuario_id: int) -> int:
        from sqlalchemy import func

        stmt = (
            select(func.count(DireccionEntrega.id))
            .where(
                DireccionEntrega.usuario_id == usuario_id,
                DireccionEntrega.eliminado_en.is_(None),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar() or 0

    async def get_by_id_and_user(
        self, direccion_id: int, usuario_id: int
    ) -> DireccionEntrega | None:
        stmt = select(DireccionEntrega).where(
            DireccionEntrega.id == direccion_id,
            DireccionEntrega.usuario_id == usuario_id,
            DireccionEntrega.eliminado_en.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_predeterminada(self, usuario_id: int) -> DireccionEntrega | None:
        stmt = select(DireccionEntrega).where(
            DireccionEntrega.usuario_id == usuario_id,
            DireccionEntrega.es_predeterminada == True,
            DireccionEntrega.eliminado_en.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def clear_predeterminada_for_user(self, usuario_id: int) -> None:
        stmt = (
            update(DireccionEntrega)
            .where(
                DireccionEntrega.usuario_id == usuario_id,
                DireccionEntrega.es_predeterminada == True,
            )
            .values(es_predeterminada=False)
        )
        await self._session.execute(stmt)

    async def set_predeterminada(self, direccion_id: int, usuario_id: int) -> DireccionEntrega | None:
        # Clear all predeterminada for this user
        await self.clear_predeterminada_for_user(usuario_id)
        # Set this one as predeterminada
        stmt = (
            update(DireccionEntrega)
            .where(
                DireccionEntrega.id == direccion_id,
                DireccionEntrega.usuario_id == usuario_id,
            )
            .values(es_predeterminada=True)
        )
        await self._session.execute(stmt)
        await self._session.flush()
        return await self.get_by_id(direccion_id)