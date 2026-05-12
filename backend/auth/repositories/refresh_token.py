from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.models.refresh_token import RefreshToken
from backend.core.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RefreshToken)

    async def get_valid_token(self, token: str) -> Optional[RefreshToken]:
        now = datetime.now(timezone.utc)
        stmt = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.revocado_en.is_(None),
            RefreshToken.expires_at > now,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def invalidate_token(self, token: str) -> bool:
        now = datetime.now(timezone.utc)
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.token == token)
            .values(revocado_en=now)
        )
        result = await self._session.execute(stmt)
        await self._session.flush()
        return result.rowcount > 0

    async def invalidate_all_for_user(self, usuario_id: int) -> None:
        now = datetime.now(timezone.utc)
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.usuario_id == usuario_id,
                RefreshToken.revocado_en.is_(None),
            )
            .values(revocado_en=now)
        )
        await self._session.execute(stmt)
        await self._session.flush()
