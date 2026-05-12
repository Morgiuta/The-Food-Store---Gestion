from fastapi import APIRouter, Depends

from backend.core.dependencies import DatabaseSession, get_current_user
from backend.pedidos.schemas.checkout import (
    ValidarStockRequest,
    ValidarStockResponse,
    CalcularTotalRequest,
    CalcularTotalResponse,
)
from backend.pedidos.services.checkout_service import CheckoutService

router = APIRouter(prefix="/pedidos", tags=["Checkout"])
service = CheckoutService()


@router.post("/validar", response_model=ValidarStockResponse)
async def validar_stock(
    body: ValidarStockRequest,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Valida que haya stock disponible para los items del carrito."""
    items_data = [item.model_dump() for item in body.items]
    return await service.validar_stock(session, items_data)


@router.post("/calcular-total", response_model=CalcularTotalResponse)
async def calcular_total(
    body: CalcularTotalRequest,
    current_user: dict = Depends(get_current_user),
):
    """Calcula el subtotal, costo de envío y total del pedido."""
    items_data = [item.model_dump() for item in body.items]
    # Para el cálculo no necesitamos backend, podemos hacerlo en frontend
    # pero mantenemos el endpoint por si necesitamos validaciones futuras
    return await service.calcular_total(items_data, body.direccion_id)