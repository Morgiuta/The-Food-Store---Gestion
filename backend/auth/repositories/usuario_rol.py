from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.models.rol import Rol
from backend.auth.models.usuario_rol import UsuarioRol
from backend.core.base_repository import BaseRepository


class UsuarioRolRepository(BaseRepository[UsuarioRol]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UsuarioRol)

    async def get_user_roles(self, usuario_id: int) -> Sequence[UsuarioRol]:
        stmt = select(UsuarioRol).where(UsuarioRol.usuario_id == usuario_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def asignar_rol(self, usuario_id: int, rol_id: int) -> UsuarioRol:
        obj = UsuarioRol(usuario_id=usuario_id, rol_id=rol_id)
        return await self.create(obj)

    async def revocar_rol(self, usuario_id: int, rol_id: int) -> bool:
        stmt = select(UsuarioRol).where(
            UsuarioRol.usuario_id == usuario_id,
            UsuarioRol.rol_id == rol_id,
        )
        result = await self._session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self._session.delete(obj)
        await self._session.flush()
        return True

    async def count_admins(self) -> int:
        stmt = (
            select(func.count(func.distinct(UsuarioRol.usuario_id)))
            .select_from(UsuarioRol)
            .join(Rol, UsuarioRol.rol_id == Rol.id)
            .where(Rol.nombre == "ADMIN")
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()
