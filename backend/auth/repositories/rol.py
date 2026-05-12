from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.models.rol import Rol
from backend.core.base_repository import BaseRepository


class RolRepository(BaseRepository[Rol]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Rol)

    async def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        stmt = select(Rol).where(Rol.nombre == nombre)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_activos(self) -> Sequence[Rol]:
        stmt = select(Rol).order_by(Rol.nombre)
        result = await self._session.execute(stmt)
        return result.scalars().all()
