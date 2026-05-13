import json
from datetime import datetime
from typing import Any, Optional

from backend.core.uow import UnitOfWork
from backend.admin.models.audit_log import AuditLog


class AuditService:
    """Service for recording and querying audit logs."""

    async def registrar(
        self,
        uow: UnitOfWork,
        usuario_id: int | None,
        accion: str,
        tabla: str,
        registro_id: int | None = None,
        valor_anterior: dict[str, Any] | None = None,
        valor_nuevo: dict[str, Any] | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        audit = AuditLog(
            usuario_id=usuario_id,
            accion=accion,
            tabla=tabla,
            registro_id=registro_id,
            valor_anterior=json.dumps(valor_anterior) if valor_anterior else None,
            valor_nuevo=json.dumps(valor_nuevo) if valor_nuevo else None,
            ip_address=ip_address,
        )
        return await uow.audit_logs.create(audit)

    async def listar(
        self,
        uow: UnitOfWork,
        skip: int = 0,
        limit: int = 50,
        tabla: str | None = None,
        accion: str | None = None,
        usuario_id: int | None = None,
        fecha_desde: datetime | None = None,
        fecha_hasta: datetime | None = None,
    ) -> tuple[list[AuditLog], int]:
        items, total = await uow.audit_logs.list_with_filters(
            skip=skip, limit=limit, tabla=tabla, accion=accion,
            usuario_id=usuario_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
        )
        return list(items), total
