from pydantic import BaseModel, Field


class CheckoutItemRequest(BaseModel):
    """Item del carrito para validar stock."""
    producto_id: int
    cantidad: int = Field(..., gt=0)


class ValidarStockRequest(BaseModel):
    """Request para validar stock de items."""
    items: list[CheckoutItemRequest]


class ValidarStockResponse(BaseModel):
    """Response de validación de stock."""
    valido: bool
    errores: list[str] = []
    items_validados: list[dict] = []


class CalcularTotalRequest(BaseModel):
    """Request para calcular total del checkout."""
    items: list[CheckoutItemRequest]
    direccion_id: int | None = None


class CalcularTotalResponse(BaseModel):
    """Response del cálculo de total."""
    subtotal: float
    costo_envio: float
    total: float
    direccion_id: int | None = None