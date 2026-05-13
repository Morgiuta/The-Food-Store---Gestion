from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CrearPagoRequest(BaseModel):
    pedido_id: int = Field(..., gt=0)


class PagoCreate(BaseModel):
    pedido_id: int = Field(..., gt=0)
    monto: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)


class PagoRead(BaseModel):
    id: int
    pedido_id: int
    monto: Decimal
    mp_status: str | None
    external_reference: str | None
    creado_en: datetime

    model_config = {"from_attributes": True}


class CrearPreferenciaResponse(BaseModel):
    preference_id: str
    init_point: str
