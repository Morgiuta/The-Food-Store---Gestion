"""
Admin service for payment management: listing, filtering, refunds.
"""
import logging
from datetime import datetime
from typing import Any

from backend.core.exceptions import NotFoundException, ValidationException
from backend.core.uow import UnitOfWork
from backend.pagos.models.pago import Pago

logger = logging.getLogger(__name__)


class AdminPagoService:
    """Admin service for payment operations."""

    async def listar_pagos(
        self,
        uow: UnitOfWork,
        skip: int = 0,
        limit: int = 20,
        mp_status: str | None = None,
        fecha_desde: datetime | None = None,
        fecha_hasta: datetime | None = None,
    ) -> tuple[list[Pago], int]:
        """List payments with filters for admin."""
        pagos = await uow.pagos.list_by_date_range(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            mp_status=mp_status,
            skip=skip,
            limit=limit,
        )
        total = await uow.pagos.count_by_status(mp_status)
        return list(pagos), total

    async def obtener_detalle(
        self,
        uow: UnitOfWork,
        pago_id: int,
    ) -> Pago | None:
        """Get payment detail by ID."""
        pago = await uow.pagos.get_by_id(pago_id)
        if not pago:
            raise NotFoundException("Pago no encontrado")
        return pago

    async def reembolsar(
        self,
        uow: UnitOfWork,
        pago_id: int,
        motivo: str,
    ) -> Pago:
        """
        Refund a payment via MercadoPago API.

        1. Validate payment exists and is in 'approved' status
        2. Call MercadoPago API to process refund
        3. Update payment status to 'refunded'
        4. Return updated payment
        """
        pago = await uow.pagos.get_by_id(pago_id)
        if not pago:
            raise NotFoundException("Pago no encontrado")

        if pago.mp_status != "approved":
            raise ValidationException(
                f"No se puede reembolsar un pago en estado '{pago.mp_status}'. "
                "Solo pagos 'approved' pueden reembolsarse."
            )

        if not pago.mp_payment_id:
            raise ValidationException("El pago no tiene un ID de MercadoPago asociado")

        # Call MercadoPago API to process refund
        try:
            import mercadopago
            from backend.core.config import get_settings
            settings = get_settings()
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

            mp_response = sdk.payment().refund(int(pago.mp_payment_id))

            if mp_response.get("status") not in (200, 201):
                logger.error(
                    "MercadoPago refund error for payment %s: %s",
                    pago.mp_payment_id,
                    mp_response.get("response", mp_response),
                )
                raise ValidationException("Error al procesar el reembolso en MercadoPago")

            logger.info(
                "Refund processed for payment %s (MP ID: %s)",
                pago_id,
                pago.mp_payment_id,
            )
        except Exception as e:
            logger.exception("Error calling MercadoPago refund API")
            if isinstance(e, ValidationException):
                raise
            raise ValidationException(f"Error de comunicación con MercadoPago: {str(e)}")

        # Update payment status
        pago.mp_status = "refunded"
        uow._session.add(pago)
        await uow._session.flush()
        await uow._session.refresh(pago)

        return pago
