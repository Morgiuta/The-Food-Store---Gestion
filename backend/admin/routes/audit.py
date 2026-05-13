from datetime import datetime
from fastapi import APIRouter, Depends, Query
from backend.admin.schemas.audit import AuditEntryRead, PaginatedAuditLogs
from backend.admin.services.audit_service import AuditService
from backend.core.dependencies import DatabaseSession, RoleRequired
from backend.core.uow import UnitOfWork

router = APIRouter(prefix="/admin/audit", tags=["Admin Audit"])
service = AuditService()


@router.get("", response_model=PaginatedAuditLogs)
async def listar_audit(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    tabla: str | None = Query(None),
    accion: str | None = Query(None),
    usuario_id: int | None = Query(None),
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
):
    skip = (page - 1) * size
    async with UnitOfWork(session) as uow:
        items, total = await service.listar(
            uow, skip, size, tabla, accion, usuario_id, fecha_desde, fecha_hasta
        )
    
    pages = max(1, (total + size - 1) // size)
    return {
        "items": [
            AuditEntryRead(
                id=e.id, usuario_id=e.usuario_id, accion=e.accion, tabla=e.tabla,
                registro_id=e.registro_id, valor_anterior=e.valor_anterior,
                valor_nuevo=e.valor_nuevo, ip_address=e.ip_address, created_at=e.created_at,
            ) for e in items
        ],
        "total": total, "page": page, "size": size, "pages": pages,
    }
