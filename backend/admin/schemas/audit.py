from datetime import datetime
from pydantic import BaseModel


class AuditEntryRead(BaseModel):
    id: int
    usuario_id: int | None
    accion: str
    tabla: str
    registro_id: int | None
    valor_anterior: str | None
    valor_nuevo: str | None
    ip_address: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedAuditLogs(BaseModel):
    items: list[AuditEntryRead]
    total: int
    page: int
    size: int
    pages: int
