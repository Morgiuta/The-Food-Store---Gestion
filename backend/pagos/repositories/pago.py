from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.base_repository import BaseRepository
from backend.pagos.models.pago import Pago


class PagoRepository(BaseRepository[Pago]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Pago)

    async def get_by_pedido(self, pedido_id: int) -> Sequence[Pago]:
        stmt = (
            select(Pago)
            .where(Pago.pedido_id == pedido_id)
            .order_by(Pago.creado_en.desc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_preference(
        self, external_reference: str
    ) -> Optional[Pago]:
        stmt = select(Pago).where(
            Pago.external_reference == external_reference
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_idempotency_key(self, key: str) -> Optional[Pago]:
        stmt = select(Pago).where(Pago.idempotency_key == key)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_status(
        self, status: str, skip: int = 0, limit: int = 100
    ) -> Sequence[Pago]:
        stmt = (
            select(Pago)
            .where(Pago.mp_status == status)
            .offset(skip)
            .limit(limit)
            .order_by(Pago.creado_en.desc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
