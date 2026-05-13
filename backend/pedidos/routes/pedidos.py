"""
Router for order CRUD operations (client and admin).
"""
from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import DatabaseSession, RoleRequired, get_current_user
from backend.core.exceptions import NotFoundException
from backend.core.uow import UnitOfWork
from backend.pedidos.schemas.pedido import (
    CrearPedidoRequest,
    PaginatedPedidos,
    PedidoDetail,
)
from backend.pedidos.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
service = PedidoService()


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
        hist_estado_anterior = hist.estado_anterior.nombre if hist.estado_anterior else None
        hist_estado_nuevo = hist.estado_nuevo.nombre if hist.estado_nuevo else "DESCONOCIDO"
        historial_read.append({
            "id": hist.id,
            "estado_anterior": hist_estado_anterior,
            "estado_nuevo": hist_estado_nuevo,
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
        hist_estado_anterior = hist.estado_anterior.nombre if hist.estado_anterior else None
        hist_estado_nuevo = hist.estado_nuevo.nombre if hist.estado_nuevo else "DESCONOCIDO"
        historial_read.append({
            "id": hist.id,
            "estado_anterior": hist_estado_anterior,
            "estado_nuevo": hist_estado_nuevo,
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


@router.get("/admin/all", response_model=PaginatedPedidos)
async def listar_pedidos_admin(
    session: DatabaseSession,
    current_user: dict = Depends(RoleRequired(["ADMIN", "PEDIDOS"])),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    estado_id: int | None = Query(None),
):
    """List all orders (ADMIN/PEDIDOS only) with optional filters."""
    skip = (page - 1) * size
    async with UnitOfWork(session) as uow:
        pedidos, total = await service.listar_admin(
            uow, skip, size, estado_id
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
