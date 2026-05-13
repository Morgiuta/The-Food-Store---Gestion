"""
Admin routes for payment management.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from backend.admin.services.admin_pago_service import AdminPagoService
from backend.core.dependencies import DatabaseSession, RoleRequired
from backend.core.uow import UnitOfWork
from backend.pagos.schemas.pago import (
    PagoDetail,
    PagoRead,
    PaginatedPagos,
    ReembolsarPagoRequest,
)

router = APIRouter(prefix="/admin/pagos", tags=["Admin Pagos"])
service = AdminPagoService()


@router.get("", response_model=PaginatedPagos)
async def listar_pagos(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    mp_status: str | None = Query(None),
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
):
    """List all payments with filters (ADMIN only)."""
    skip = (page - 1) * size
    async with UnitOfWork(session) as uow:
        pagos, total = await service.listar_pagos(
            uow, skip, size, mp_status, fecha_desde, fecha_hasta
        )

    items = [
        PagoRead(
            id=p.id,
            pedido_id=p.pedido_id,
            monto=p.monto,
            mp_status=p.mp_status,
            external_reference=p.external_reference,
            creado_en=p.creado_en,
        )
        for p in pagos
    ]
    pages = max(1, (total + size - 1) // size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


@router.get("/{pago_id}", response_model=PagoDetail)
async def obtener_pago(
    pago_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Get payment detail (ADMIN only)."""
    async with UnitOfWork(session) as uow:
        pago = await service.obtener_detalle(uow, pago_id)

    return PagoDetail(
        id=pago.id,
        pedido_id=pago.pedido_id,
        monto=pago.monto,
        mp_payment_id=pago.mp_payment_id,
        mp_status=pago.mp_status,
        external_reference=pago.external_reference,
        idempotency_key=pago.idempotency_key,
        creado_en=pago.creado_en,
        actualizado_en=pago.actualizado_en,
    )


@router.post("/{pago_id}/reembolsar", response_model=PagoRead)
async def reembolsar_pago(
    pago_id: int,
    body: ReembolsarPagoRequest,
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN"])),
):
    """Refund an approved payment (ADMIN only)."""
    async with UnitOfWork(session) as uow:
        pago = await service.reembolsar(uow, pago_id, body.motivo)

    return PagoRead(
        id=pago.id,
        pedido_id=pago.pedido_id,
        monto=pago.monto,
        mp_status=pago.mp_status,
        external_reference=pago.external_reference,
        creado_en=pago.creado_en,
    )
