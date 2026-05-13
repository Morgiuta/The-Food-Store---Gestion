from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.base_repository import BaseRepository
from backend.admin.models.configuracion import Configuracion


class ConfiguracionRepository(BaseRepository[Configuracion]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Configuracion)

    async def get_by_clave(self, clave: str) -> Optional[Configuracion]:
        stmt = select(Configuracion).where(Configuracion.clave == clave)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(self, clave: str, valor: str) -> Configuracion:
        existing = await self.get_by_clave(clave)
        if existing:
            existing.valor = valor
            self._session.add(existing)
            await self._session.flush()
            await self._session.refresh(existing)
            return existing
        else:
            conf = Configuracion(clave=clave, valor=valor)
            return await self.create(conf)
