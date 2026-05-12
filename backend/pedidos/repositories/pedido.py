from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.base_repository import BaseRepository
from backend.pedidos.models.pedido import Pedido


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Pedido)

    async def list_by_user(
        self, usuario_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Pedido]:
        stmt = (
            select(Pedido)
            .where(Pedido.usuario_id == usuario_id)
            .order_by(Pedido.creado_en.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def list_all_with_filters(
        self,
        skip: int = 0,
        limit: int = 100,
        estado_id: Optional[int] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
        usuario_id: Optional[int] = None,
    ) -> Sequence[Pedido]:
        stmt = select(Pedido)

        if estado_id is not None:
            stmt = stmt.where(Pedido.estado_id == estado_id)
        if fecha_desde is not None:
            stmt = stmt.where(Pedido.creado_en >= fecha_desde)
        if fecha_hasta is not None:
            stmt = stmt.where(Pedido.creado_en <= fecha_hasta)
        if usuario_id is not None:
            stmt = stmt.where(Pedido.usuario_id == usuario_id)

        stmt = stmt.order_by(Pedido.creado_en.desc()).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def count_by_status(self) -> dict[int, int]:
        stmt = (
            select(Pedido.estado_id, func.count(Pedido.id))
            .group_by(Pedido.estado_id)
        )
        result = await self._session.execute(stmt)
        counts: dict[int, int] = {}
        for estado_id, count in result:
            counts[estado_id] = count
        return counts

    async def get_with_details(self, pedido_id: int) -> Optional[Pedido]:
        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .options(
                selectinload(Pedido.detalles),
                selectinload(Pedido.historial_estados),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
