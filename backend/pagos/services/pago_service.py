
import logging
from decimal import Decimal
from typing import Any

import mercadopago
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.core.config import get_settings
from backend.core.exceptions import NotFoundException, ValidationException, ForbiddenException
from backend.core.uow import UnitOfWork
from backend.pagos.models.pago import Pago
from backend.pedidos.models.pedido import Pedido
from backend.pedidos.services.pedido_fsm_service import PedidoFsmService

logger = logging.getLogger(__name__)
settings = get_settings()


class PagoService:
    """Service for MercadoPago payment operations."""

    def __init__(self):
        self._sdk = None

    def _get_sdk(self):
        """Get or initialize MercadoPago SDK."""
        if self._sdk is None:
            access_token = settings.MERCADOPAGO_ACCESS_TOKEN
            if not access_token:
                logger.warning("MERCADOPAGO_ACCESS_TOKEN not configured")
            self._sdk = mercadopago.SDK(access_token)
        return self._sdk

    async def crear_preferencia(
        self,
        uow: UnitOfWork,
        pedido_id: int,
        usuario_id: int,
    ) -> dict[str, Any]:
        """
        Create a MercadoPago payment preference for an order.
        """
        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .options(selectinload(Pedido.estado))
        )
        result = await uow._session.execute(stmt)
        pedido = result.scalar_one_or_none()

        if not pedido:
            raise NotFoundException("Pedido no encontrado")

        if pedido.usuario_id != usuario_id:
            raise ForbiddenException("El pedido no pertenece al usuario actual")

        if pedido.eliminado_en:
            raise ValidationException("El pedido ha sido eliminado")

        estado_codigo = pedido.estado.nombre if pedido.estado else ""
        if estado_codigo != "PENDIENTE":
            raise ValidationException(
                f"El pedido debe estar en PENDIENTE para pagar. Estado actual: {estado_codigo}"
            )

        import uuid
        idempotency_key = str(uuid.uuid4())

        monto = float(pedido.total)
        external_reference = str(pedido.id)

        preference_data = {
            "items": [
                {
                    "title": f"Pedido #{pedido.id}",
                    "quantity": 1,
                    "unit_price": monto,
                    "currency_id": "ARS",
                }
            ],
            "external_reference": external_reference,
            "purpose": "wallet_purchase",
            "back_urls": {
                "success": f"{settings.FRONTEND_URL}/pedidos/confirmacion/{pedido.id}",
                "failure": f"{settings.FRONTEND_URL}/checkout?status=rejected",
                "pending": f"{settings.FRONTEND_URL}/checkout?status=pending",
            },
            "auto_return": "approved",
            "notification_url": f"{settings.API_URL}/api/v1/pagos/webhook",
        }

        try:
            sdk = self._get_sdk()
            mp_response = sdk.preference().create(preference_data)

            if mp_response.get("status") not in (200, 201):
                logger.error(
                    "MercadoPago error creating preference: %s",
                    mp_response.get("response", mp_response),
                )
                raise ValidationException(
                    "Error al crear la preferencia de pago en MercadoPago"
                )

            mp_response_data = mp_response.get("response", {})
            preference_id = mp_response_data.get("id")
            init_point = mp_response_data.get("init_point") or mp_response_data.get("sandbox_init_point")

            if not preference_id:
                raise ValidationException("MercadoPago no devolvió un ID de preferencia")

        except ValidationException:
            raise
        except Exception as e:
            logger.exception("Error calling MercadoPago API")
            raise ValidationException(f"Error de comunicación con MercadoPago: {str(e)}")

        pago = Pago(
            pedido_id=pedido.id,
            monto=pedido.total,
            mp_status="pending",
            external_reference=external_reference,
            idempotency_key=idempotency_key,
        )
        pago = await uow.pagos.create(pago)

        return {
            "id": pago.id,
            "preference_id": preference_id,
            "init_point": init_point,
        }

    async def procesar_webhook(self, data: dict[str, Any]) -> dict[str, str]:
        """
        Process MercadoPago IPN webhook notification.
        """
        logger.info("Webhook received: %s", data)

        topic = data.get("topic") or data.get("type")
        payment_id = None

        if topic == "payment":
            payment_id = data.get("id") or data.get("data", {}).get("id")
        elif topic == "merchant_order":
            merchant_order_id = data.get("id") or data.get("data", {}).get("id")
            if merchant_order_id:
                try:
                    sdk = self._get_sdk()
                    mp_response = sdk.merchant_order().get(merchant_order_id)
                    if mp_response.get("status") == 200:
                        resp_data = mp_response.get("response", {})
                        payments = resp_data.get("payments", [])
                        if payments:
                            payment_id = payments[0].get("id")
                except Exception as e:
                    logger.exception("Error fetching merchant order")
                    return {"status": "error", "message": str(e)}

        if not payment_id:
            logger.warning("No payment_id found in webhook data")
            return {"status": "ignored", "message": "No payment_id"}

        try:
            sdk = self._get_sdk()
            mp_response = sdk.payment().get(int(payment_id))
            if mp_response.get("status") != 200:
                logger.error("Failed to query MP payment %s", payment_id)
                return {"status": "error", "message": "Failed to verify payment"}

            payment_data = mp_response.get("response", {})
            mp_status = payment_data.get("status")
            external_reference = payment_data.get("external_reference", "")
        except Exception as e:
            logger.exception("Error querying MP payment")
            return {"status": "error", "message": str(e)}

        if not external_reference:
            logger.warning("No external_reference in payment %s", payment_id)
            return {"status": "ignored", "message": "No external_reference"}

        from backend.core.database import async_session_factory

        try:
            async with async_session_factory() as session:
                async with UnitOfWork(session) as uow:
                    pago = await uow.pagos.get_by_preference(external_reference)
                    if not pago:
                        logger.warning("No pago found for external_reference %s", external_reference)
                        return {"status": "ignored", "message": "Pago not found"}

                    if pago.mp_payment_id == str(payment_id) and pago.mp_status == mp_status:
                        logger.info("Duplicate webhook, skipping (idempotency)")
                        return {"status": "duplicate", "message": "Already processed"}

                    pago.mp_payment_id = str(payment_id)
                    pago.mp_status = mp_status
                    uow._session.add(pago)

                    if mp_status == "approved":
                        fsm_service = PedidoFsmService()
                        try:
                            await fsm_service.avanzar_estado(
                                uow,
                                pedido_id=pago.pedido_id,
                                nuevo_estado_codigo="CONFIRMADO",
                                observacion=f"Pago aprobado (MP: {payment_id})",
                                usuario_id=0,
                                roles=["ADMIN"],
                                system_action=True,
                            )
                        except Exception as e:
                            logger.exception("Error transitioning order %s", pago.pedido_id)

                    await uow.commit()

            return {"status": "processed", "message": f"Payment {payment_id} status: {mp_status}"}

        except Exception as e:
            logger.exception("Error processing webhook")
            return {"status": "error", "message": str(e)}

    async def consultar_estado(
        self,
        uow: UnitOfWork,
        pedido_id: int,
        usuario_id: int,
        roles: list[str],
    ) -> Pago | None:
        """Get the latest payment for an order."""
        stmt = select(Pedido).where(Pedido.id == pedido_id)
        result = await uow._session.execute(stmt)
        pedido = result.scalar_one_or_none()

        if not pedido:
            raise NotFoundException("Pedido no encontrado")

        is_admin = any(r in roles for r in ["ADMIN", "PEDIDOS"])
        if pedido.usuario_id != usuario_id and not is_admin:
            raise ForbiddenException("No tienes permiso para ver este pago")

        pagos = await uow.pagos.get_by_pedido(pedido_id)
        if not pagos:
            return None

        return pagos[0]
