from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ItemPedidoRequest(BaseModel):
    producto_id: int = Field(..., gt=0)
    cantidad: int = Field(..., ge=1)
    personalizacion: list[int] | None = None


class CrearPedidoRequest(BaseModel):
    items: list[ItemPedidoRequest] = Field(..., min_length=1)
    direccion_id: int | None = None
    forma_pago_id: int | None = None


class AvanzarEstadoRequest(BaseModel):
    nuevo_estado: str
    motivo: str | None = Field(None, max_length=500)


class CancelarPedidoRequest(BaseModel):
    motivo: str = Field(..., min_length=5, max_length=500)


class DetallePedidoRead(BaseModel):
    id: int
    producto_id: int | None
    producto_nombre: str | None = None
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    personalizacion: list[int] = []

    model_config = {"from_attributes": True}


class HistorialEstadoRead(BaseModel):
    id: int
    estado_anterior: str | None = None
    estado_nuevo: str
    usuario_id: int | None = None
    observacion: str | None = None
    timestamp: datetime

    model_config = {"from_attributes": True}


class PedidoRead(BaseModel):
    id: int
    usuario_id: int
    estado: str
    total: Decimal
    costo_envio: Decimal
    creado_en: datetime

    model_config = {"from_attributes": True}


class PedidoDetail(PedidoRead):
    detalles: list[DetallePedidoRead] = []
    historial: list[HistorialEstadoRead] = []


class PaginatedPedidos(BaseModel):
    items: list[PedidoRead]
    total: int
    page: int
    size: int
    pages: int
