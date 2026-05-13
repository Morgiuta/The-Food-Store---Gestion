from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.base_repository import BaseRepository
from backend.pagos.models.forma_pago import FormaPago


class FormaPagoRepository(BaseRepository[FormaPago]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, FormaPago)

    async def list_activas(self) -> Sequence[FormaPago]:
        stmt = select(FormaPago).where(FormaPago.activo == True).order_by(FormaPago.nombre)  # noqa: E712
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def toggle_activo(self, id: int, activo: bool) -> Optional[FormaPago]:
        return await self.update(id, {"activo": activo})
