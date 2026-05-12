from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.base_repository import BaseRepository
from backend.pedidos.models.historial_estado import HistorialEstadoPedido


class HistorialEstadoPedidoRepository(BaseRepository[HistorialEstadoPedido]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, HistorialEstadoPedido)

    async def list_by_pedido(
        self, pedido_id: int
    ) -> Sequence[HistorialEstadoPedido]:
        stmt = (
            select(HistorialEstadoPedido)
            .where(HistorialEstadoPedido.pedido_id == pedido_id)
            .order_by(HistorialEstadoPedido.timestamp)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
