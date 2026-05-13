"""
Router for order CRUD operations (client and admin).
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import DatabaseSession, RoleRequired, get_current_user
from backend.core.exceptions import NotFoundException
from backend.core.uow import UnitOfWork
from backend.pedidos.schemas.pedido import (
    AvanzarEstadoRequest,
    CancelarPedidoRequest,
    CrearPedidoRequest,
    HistorialEstadoRead,
    PaginatedPedidos,
    PedidoDetail,
)
from backend.pedidos.services.pedido_fsm_service import PedidoFsmService
from backend.pedidos.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
service = PedidoService()
fsm_service = PedidoFsmService()


def _build_pedido_detail(pedido) -> dict:
    """Build PedidoDetail response dict from ORM model."""
    estado_nombre = pedido.estado.nombre if pedido.estado else "DESCONOCIDO"
    detalles_read = []
    for det in pedido.detalles or []:
        detalles_read.append({
            "id": det.id,
            "producto_id": det.producto_id,
            "producto_nombre": getattr(det, "producto_nombre", None),
            "cantidad": det.cantidad,
            "precio_unitario": det.precio_snapshot,
            "subtotal": det.subtotal,
            "personalizacion": det.personalizacion or [],
        })
    historial_read = []
    for hist in pedido.historial_estados or []:
        historial_read.append({
            "id": hist.id,
            "estado_anterior": hist.estado_anterior.nombre if hist.estado_anterior else None,
            "estado_nuevo": hist.estado_nuevo.nombre if hist.estado_nuevo else "DESCONOCIDO",
            "usuario_id": hist.usuario_id,
            "observacion": hist.observacion,
            "timestamp": hist.timestamp,
        })
    return {
        "id": pedido.id,
        "usuario_id": pedido.usuario_id,
        "estado": estado_nombre,
        "total": pedido.total,
        "costo_envio": pedido.costo_envio,
        "creado_en": pedido.creado_en,
        "detalles": detalles_read,
        "historial": historial_read,
    }


def pedido_to_read(pedido) -> dict:
    """Convert Pedido ORM to dict for schema."""
    estado_nombre = pedido.estado.nombre if pedido.estado else "DESCONOCIDO"
    return {
        "id": pedido.id,
        "usuario_id": pedido.usuario_id,
        "estado": estado_nombre,
        "total": pedido.total,
        "costo_envio": pedido.costo_envio,
        "creado_en": pedido.creado_en,
    }


@router.post("", response_model=PedidoDetail, status_code=201)
async def crear_pedido(
    body: CrearPedidoRequest,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Create a new order atomically."""
    items_data = [item.model_dump() for item in body.items]

    async with UnitOfWork(session) as uow:
        pedido = await service.crear(
            uow,
            items_data,
            body.direccion_id,
            body.forma_pago_id,
            current_user["user_id"],
        )

    return _build_pedido_detail(pedido)


@router.get("", response_model=PaginatedPedidos)
async def listar_mis_pedidos(
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """List orders for the authenticated user."""
    skip = (page - 1) * size
    async with UnitOfWork(session) as uow:
        pedidos, total = await service.listar_mis_pedidos(
            uow, current_user["user_id"], skip, size
        )

    items = [pedido_to_read(p) for p in pedidos]
    pages = max(1, (total + size - 1) // size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


@router.get("/{pedido_id}", response_model=PedidoDetail)
async def obtener_pedido(
    pedido_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Get full order detail with items and history."""
    async with UnitOfWork(session) as uow:
        pedido = await service.obtener_detalle(
            uow,
            pedido_id,
            current_user["user_id"],
            current_user["roles"],
        )

    if not pedido:
        raise NotFoundException("Pedido no encontrado")

    return _build_pedido_detail(pedido)


@router.patch("/{pedido_id}/estado", response_model=PedidoDetail)
async def avanzar_estado_pedido(
    pedido_id: int,
    body: AvanzarEstadoRequest,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Advance order state (ADMIN/PEDIDOS only)."""
    async with UnitOfWork(session) as uow:
        pedido = await fsm_service.avanzar_estado(
            uow, pedido_id, body.nuevo_estado, body.motivo,
            current_user["user_id"], current_user["roles"],
        )
    return _build_pedido_detail(pedido)


@router.patch("/{pedido_id}/cancelar", response_model=PedidoDetail)
async def cancelar_pedido(
    pedido_id: int,
    body: CancelarPedidoRequest,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Cancel an order (permissions depend on current state)."""
    async with UnitOfWork(session) as uow:
        pedido = await fsm_service.cancelar(
            uow, pedido_id, body.motivo,
            current_user["user_id"], current_user["roles"],
        )
    return _build_pedido_detail(pedido)


@router.get("/{pedido_id}/historial", response_model=list[HistorialEstadoRead])
async def obtener_historial_pedido(
    pedido_id: int,
    session: DatabaseSession,
    current_user: dict = Depends(get_current_user),
):
    """Get order state history (append-only audit trail)."""
    async with UnitOfWork(session) as uow:
        historial = await fsm_service.obtener_historial(
            uow, pedido_id,
            current_user["user_id"], current_user["roles"],
        )
    return [
        {
            "id": h.id,
            "estado_anterior": h.estado_anterior.nombre if h.estado_anterior else None,
            "estado_nuevo": h.estado_nuevo.nombre if h.estado_nuevo else "DESCONOCIDO",
            "usuario_id": h.usuario_id,
            "observacion": h.observacion,
            "timestamp": h.timestamp,
        }
        for h in historial
    ]


@router.get("/admin/all", response_model=PaginatedPedidos)
async def listar_pedidos_admin(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN", "PEDIDOS"])),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    estado_id: int | None = Query(None),
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
    search: str | None = Query(None),
):
    """List all orders (ADMIN/PEDIDOS only) with optional filters."""
    skip = (page - 1) * size
    async with UnitOfWork(session) as uow:
        pedidos, total = await service.listar_admin(
            uow, skip, size, estado_id, fecha_desde, fecha_hasta, search
        )

    items = [pedido_to_read(p) for p in pedidos]
    pages = max(1, (total + size - 1) // size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }
