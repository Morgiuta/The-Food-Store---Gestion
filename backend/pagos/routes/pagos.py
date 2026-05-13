
import logging

from fastapi import APIRouter, Depends, Request

from backend.core.dependencies import DatabaseSession, get_current_user
from backend.core.uow import UnitOfWork
from backend.pagos.schemas.pago import CrearPagoRequest, CrearPreferenciaResponse, PagoRead
from backend.pagos.services.pago_service import PagoService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pagos", tags=["Pagos"])
service = PagoService()


@router.post("/crear", response_model=CrearPreferenciaResponse, status_code=201)
async def crear_pago(
    body: CrearPagoRequest,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Create a MercadoPago payment preference for an order."""
    async with UnitOfWork(session) as uow:
        result = await service.crear_preferencia(
            uow,
            pedido_id=body.pedido_id,
            usuario_id=current_user["user_id"],
        )

    return CrearPreferenciaResponse(
        preference_id=result["preference_id"],
        init_point=result["init_point"],
    )


@router.post("/webhook")
async def webhook_mercadopago(request: Request):
    """Receive MercadoPago IPN webhook notifications."""
    try:
        data = await request.json()
    except Exception:
        data = dict(request.query_params)

    logger.info("MercadoPago webhook received: %s", data)
    result = await service.procesar_webhook(data)

    return {"status": result["status"]}


@router.get("/{pedido_id}", response_model=PagoRead | None)
async def consultar_pago(
    pedido_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Get payment status for an order."""
    async with UnitOfWork(session) as uow:
        pago = await service.consultar_estado(
            uow,
            pedido_id=pedido_id,
            usuario_id=current_user["user_id"],
            roles=current_user["roles"],
        )

    if not pago:
        return None

    return PagoRead(
        id=pago.id,
        pedido_id=pago.pedido_id,
        monto=pago.monto,
        mp_status=pago.mp_status,
        external_reference=pago.external_reference,
        creado_en=pago.creado_en,
    )
