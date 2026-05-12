from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.auth.models.usuario import Usuario
from backend.auth.models.usuario_rol import UsuarioRol
from backend.core.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Usuario)

    async def get_by_email(self, email: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_with_roles(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[Usuario]:
        stmt = (
            select(Usuario)
            .options(
                selectinload(Usuario.roles).selectinload(UsuarioRol.rol)
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_with_roles(self, user_id: int) -> Optional[Usuario]:
        stmt = (
            select(Usuario)
            .where(Usuario.id == user_id)
            .options(
                selectinload(Usuario.roles).selectinload(UsuarioRol.rol)
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
