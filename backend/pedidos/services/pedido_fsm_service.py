"""
FSM Service for order state transitions and cancellation.
Implements the Finite State Machine with valid transition map,
stock management, and append-only audit trail.
"""
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from backend.core.exceptions import NotFoundException, ValidationException, ForbiddenException
from backend.core.uow import UnitOfWork
from backend.pedidos.models.pedido import Pedido
from backend.pedidos.models.detalle_pedido import DetallePedido
from backend.pedidos.models.historial_estado import HistorialEstadoPedido
from backend.productos.models.producto import Producto

ID_PENDIENTE = 1
ID_CONFIRMADO = 2
ID_EN_PREPARACION = 3
ID_EN_CAMINO = 4
ID_ENTREGADO = 5
ID_CANCELADO = 6

TRANSICIONES_VALIDAS: dict[str, list[str]] = {
    "PENDIENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["EN_PREPARACION", "CANCELADO"],
    "EN_PREPARACION": ["EN_CAMINO", "CANCELADO"],
    "EN_CAMINO": ["ENTREGADO"],
    "ENTREGADO": [],
    "CANCELADO": [],
}

TRANSICIONES_CON_STOCK = {
    "PENDIENTE-CONFIRMADO": "DECREMENTAR",
    "CONFIRMADO-CANCELADO": "RESTAURAR",
}


class PedidoFsmService:
    """Service for FSM operations on orders."""

    def validar_transicion(self, estado_actual: str, nuevo_estado: str) -> None:
        """Validate that a transition is allowed by the FSM map."""
        if estado_actual not in TRANSICIONES_VALIDAS:
            raise ValidationException(f"Estado '{estado_actual}' no reconocido")

        transiciones = TRANSICIONES_VALIDAS[estado_actual]
        if nuevo_estado not in transiciones:
            raise ValidationException(
                f"Transición '{estado_actual} \u2192 {nuevo_estado}' no permitida. "
                f"Transiciones válidas: {', '.join(transiciones) if transiciones else 'ninguna (estado terminal)'}"
            )

    def _get_estado_ids(self) -> dict[str, int]:
        """Map estado codigo to ID."""
        return {
            "PENDIENTE": ID_PENDIENTE,
            "CONFIRMADO": ID_CONFIRMADO,
            "EN_PREPARACION": ID_EN_PREPARACION,
            "EN_CAMINO": ID_EN_CAMINO,
            "ENTREGADO": ID_ENTREGADO,
            "CANCELADO": ID_CANCELADO,
        }

    async def avanzar_estado(
        self,
        uow: UnitOfWork,
        pedido_id: int,
        nuevo_estado_codigo: str,
        observacion: str | None,
        usuario_id: int,
        roles: list[str],
        system_action: bool = False,
    ) -> Pedido:
        """Advance an order to the next state."""
        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .options(
                selectinload(Pedido.estado),
                selectinload(Pedido.detalles).selectinload(DetallePedido.producto),
            )
        )
        result = await uow._session.execute(stmt)
        pedido = result.scalar_one_or_none()

        if not pedido:
            raise NotFoundException("Pedido no encontrado")

        estado_actual_codigo = pedido.estado.nombre if pedido.estado else "DESCONOCIDO"

        self.validar_transicion(estado_actual_codigo, nuevo_estado_codigo)

        if not any(r in roles for r in ["ADMIN", "PEDIDOS"]) and not system_action:
            raise ForbiddenException("No tienes permisos para avanzar estados de pedido")

        if estado_actual_codigo == "PENDIENTE" and nuevo_estado_codigo == "CONFIRMADO":
            if not system_action:
                raise ValidationException("La transición PENDIENTE\u2192CONFIRMADO solo puede ocurrir por pago aprobado")

        estado_ids = self._get_estado_ids()
        nuevo_estado_id = estado_ids[nuevo_estado_codigo]

        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_anterior_id=pedido.estado_id,
            estado_nuevo_id=nuevo_estado_id,
            usuario_id=usuario_id,
            observacion=observacion,
        )
        await uow.historial_estados.create(historial)

        pedido.estado_id = nuevo_estado_id
        uow._session.add(pedido)
        await uow._session.flush()
        await uow._session.refresh(pedido)

        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido.id)
            .options(
                selectinload(Pedido.estado),
                selectinload(Pedido.detalles),
                selectinload(Pedido.historial_estados)
                .selectinload(HistorialEstadoPedido.estado_nuevo),
                selectinload(Pedido.historial_estados)
                .selectinload(HistorialEstadoPedido.estado_anterior),
            )
        )
        result = await uow._session.execute(stmt)
        return result.scalar_one()

    async def cancelar(
        self,
        uow: UnitOfWork,
        pedido_id: int,
        motivo: str,
        usuario_id: int,
        roles: list[str],
    ) -> Pedido:
        """Cancel an order with stock restoration if needed."""
        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido_id)
            .options(
                selectinload(Pedido.estado),
                selectinload(Pedido.detalles),
            )
        )
        result = await uow._session.execute(stmt)
        pedido = result.scalar_one_or_none()

        if not pedido:
            raise NotFoundException("Pedido no encontrado")

        estado_actual_codigo = pedido.estado.nombre if pedido.estado else "DESCONOCIDO"

        self.validar_transicion(estado_actual_codigo, "CANCELADO")

        if estado_actual_codigo == "PENDIENTE":
            is_owner = pedido.usuario_id == usuario_id
            has_admin_role = any(r in roles for r in ["ADMIN", "PEDIDOS"])
            if not is_owner and not has_admin_role:
                raise ForbiddenException("No tienes permiso para cancelar este pedido")
        elif estado_actual_codigo == "CONFIRMADO":
            if not any(r in roles for r in ["ADMIN", "PEDIDOS"]):
                raise ForbiddenException("Solo ADMIN o Gestor de Pedidos pueden cancelar pedidos confirmados")
        elif estado_actual_codigo == "EN_PREPARACION":
            if "ADMIN" not in roles:
                raise ForbiddenException("Solo ADMIN puede cancelar pedidos en preparación")
        else:
            raise ValidationException(f"No se puede cancelar un pedido en estado '{estado_actual_codigo}'")

        if estado_actual_codigo == "CONFIRMADO":
            for detalle in pedido.detalles:
                producto_id = detalle.producto_id
                cantidad = detalle.cantidad
                if producto_id:
                    stmt = (
                        update(Producto)
                        .where(Producto.id == producto_id)
                        .values(stock_cantidad=Producto.stock_cantidad + cantidad)
                    )
                    await uow._session.execute(stmt)

        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_anterior_id=pedido.estado_id,
            estado_nuevo_id=ID_CANCELADO,
            usuario_id=usuario_id,
            observacion=motivo,
        )
        await uow.historial_estados.create(historial)

        pedido.estado_id = ID_CANCELADO
        uow._session.add(pedido)
        await uow._session.flush()

        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido.id)
            .options(
                selectinload(Pedido.estado),
                selectinload(Pedido.detalles),
                selectinload(Pedido.historial_estados)
                .selectinload(HistorialEstadoPedido.estado_nuevo),
                selectinload(Pedido.historial_estados)
                .selectinload(HistorialEstadoPedido.estado_anterior),
            )
        )
        result = await uow._session.execute(stmt)
        return result.scalar_one()

    async def obtener_historial(
        self,
        uow: UnitOfWork,
        pedido_id: int,
        usuario_id: int,
        roles: list[str],
    ) -> list[HistorialEstadoPedido]:
        """Get the full state history for an order (append-only audit trail)."""
        stmt = select(Pedido).where(Pedido.id == pedido_id)
        result = await uow._session.execute(stmt)
        pedido = result.scalar_one_or_none()

        if not pedido:
            raise NotFoundException("Pedido no encontrado")

        is_admin = any(r in roles for r in ["ADMIN", "PEDIDOS"])
        if pedido.usuario_id != usuario_id and not is_admin:
            raise ForbiddenException("No tienes permiso para ver este historial")

        stmt = (
            select(HistorialEstadoPedido)
            .where(HistorialEstadoPedido.pedido_id == pedido_id)
            .options(
                selectinload(HistorialEstadoPedido.estado_nuevo),
                selectinload(HistorialEstadoPedido.estado_anterior),
            )
            .order_by(HistorialEstadoPedido.timestamp)
        )
        result = await uow._session.execute(stmt)
        return list(result.scalars().all())
