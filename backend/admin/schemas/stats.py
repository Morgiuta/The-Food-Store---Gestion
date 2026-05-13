from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class ProductoStockBajo(BaseModel):
    id: int
    nombre: str
    stock_cantidad: int
    disponible: bool


class ProductoMasVendido(BaseModel):
    id: int
    nombre: str
    total_vendido: int


class AdminStatsResponse(BaseModel):
    total_ventas: Decimal
    pedidos_hoy: int
    usuarios_activos: int
    stock_bajo: int


class RevenueEntry(BaseModel):
    fecha: str
    ingresos: Decimal


class OrderStatusCount(BaseModel):
    estado: str
    cantidad: int


class ProductsStatsResponse(BaseModel):
    stock_bajo: list[ProductoStockBajo]
    mas_vendidos: list[ProductoMasVendido]
