from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.base_repository import BaseRepository
from backend.ingredientes.models.ingrediente import Ingrediente


class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Ingrediente)

    async def list_by_allergen(
        self, es_alergeno: bool
    ) -> Sequence[Ingrediente]:
        stmt = (
            select(Ingrediente)
            .where(Ingrediente.es_alergeno == es_alergeno)
            .order_by(Ingrediente.nombre)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def count_by_allergen(self) -> dict:
        stmt = (
            select(
                Ingrediente.es_alergeno,
                func.count(Ingrediente.id),
            )
            .group_by(Ingrediente.es_alergeno)
        )
        result = await self._session.execute(stmt)
        counts: dict = {}
        for es_alergeno, count in result:
            counts[bool(es_alergeno)] = count
        return counts
