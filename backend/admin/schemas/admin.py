from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class StatsResponse(BaseModel):
    total_ventas: int
    pedidos_hoy: int
    usuarios_activos: int
    stock_bajo: int


class RevenueResponse(BaseModel):
    periodo: str
    monto: Decimal


class ConfigRead(BaseModel):
    id: int
    clave: str
    valor: str
    actualizado_en: datetime | None = None

    model_config = {"from_attributes": True}


class ConfigUpdate(BaseModel):
    valor: str = Field(..., min_length=1)
