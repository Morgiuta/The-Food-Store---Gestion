from datetime import datetime
from typing import Optional, Sequence
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.base_repository import BaseRepository
from backend.admin.models.audit_log import AuditLog


class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AuditLog)

    async def list_with_filters(
        self,
        skip: int = 0,
        limit: int = 50,
        tabla: Optional[str] = None,
        accion: Optional[str] = None,
        usuario_id: Optional[int] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
    ) -> tuple[Sequence[AuditLog], int]:
        stmt = select(AuditLog)
        count_stmt = select(func.count()).select_from(AuditLog)

        if tabla:
            stmt = stmt.where(AuditLog.tabla == tabla)
            count_stmt = count_stmt.where(AuditLog.tabla == tabla)
        if accion:
            stmt = stmt.where(AuditLog.accion == accion)
            count_stmt = count_stmt.where(AuditLog.accion == accion)
        if usuario_id is not None:
            stmt = stmt.where(AuditLog.usuario_id == usuario_id)
            count_stmt = count_stmt.where(AuditLog.usuario_id == usuario_id)
        if fecha_desde:
            stmt = stmt.where(AuditLog.created_at >= fecha_desde)
            count_stmt = count_stmt.where(AuditLog.created_at >= fecha_desde)
        if fecha_hasta:
            stmt = stmt.where(AuditLog.created_at <= fecha_hasta)
            count_stmt = count_stmt.where(AuditLog.created_at <= fecha_hasta)

        stmt = stmt.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
        
        result = await self._session.execute(stmt)
        items = result.scalars().all()
        
        result = await self._session.execute(count_stmt)
        total = result.scalar_one()
        
        return items, total
