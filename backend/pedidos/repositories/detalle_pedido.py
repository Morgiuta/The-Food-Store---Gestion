from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.base_repository import BaseRepository
from backend.pedidos.models.detalle_pedido import DetallePedido


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DetallePedido)

    async def list_by_pedido(self, pedido_id: int) -> Sequence[DetallePedido]:
        stmt = (
            select(DetallePedido)
            .where(DetallePedido.pedido_id == pedido_id)
            .order_by(DetallePedido.id)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
