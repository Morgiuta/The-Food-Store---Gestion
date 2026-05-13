"""
Service for creating and managing orders with atomic transactions.
"""
import json
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from backend.auth.models.direccion import DireccionEntrega
from backend.core.exceptions import ForbiddenException, ValidationException
from backend.core.uow import UnitOfWork
from backend.pedidos.models.detalle_pedido import DetallePedido
from backend.pedidos.models.historial_estado import HistorialEstadoPedido
from backend.pedidos.models.pedido import Pedido
from backend.productos.models.producto import Producto

COSTO_ENVIO = Decimal("500.00")
ID_ESTADO_PENDIENTE = 1  # Seed ID for PENDIENTE


class PedidoService:
    """Service for order operations."""

    async def crear(
        self,
        uow: UnitOfWork,
        items: list[dict],
        direccion_id: int | None,
        forma_pago_id: int | None,
        usuario_id: int,
    ) -> Pedido:
        """
        Create a new order atomically using Unit of Work.

        Steps:
        1. Validate each product (exists, available, stock sufficient) with SELECT FOR UPDATE
        2. Validate address ownership (if provided)
        3. Calculate totals
        4. Create Pedido, DetallePedido records, and initial HistorialEstadoPedido
        """
        detalles_data = []
        total = Decimal("0")

        for item in items:
            producto_id = item["producto_id"]
            cantidad = item["cantidad"]
            personalizacion = item.get("personalizacion")

            stmt = select(Producto).where(Producto.id == producto_id).with_for_update()
            result = await uow._session.execute(stmt)
            producto = result.scalar_one_or_none()

            if not producto:
                raise ValidationException(f"Producto ID {producto_id} no encontrado")
            if producto.eliminado_en:
                raise ValidationException(f"Producto '{producto.nombre}' no está disponible")
            if not producto.disponible:
                raise ValidationException(f"Producto '{producto.nombre}' no está disponible")
            if producto.stock_cantidad < cantidad:
                raise ValidationException(
                    f"Stock insuficiente para '{producto.nombre}': "
                    f"disponible {producto.stock_cantidad}, solicitado {cantidad}"
                )

            precio_snapshot = producto.precio
            subtotal = precio_snapshot * cantidad
            total += subtotal

            detalles_data.append({
                "producto_id": producto_id,
                "producto_nombre": producto.nombre,
                "cantidad": cantidad,
                "precio_snapshot": precio_snapshot,
                "subtotal": subtotal,
                "personalizacion": personalizacion,
            })

        # Validate address if provided and create snapshot
        direccion_snapshot = None
        if direccion_id:
            result = await uow._session.execute(
                select(DireccionEntrega).where(DireccionEntrega.id == direccion_id)
            )
            direccion = result.scalar_one_or_none()
            if not direccion:
                raise ValidationException("Dirección no encontrada")
            if direccion.usuario_id != usuario_id:
                raise ValidationException("La dirección no pertenece al usuario")

            direccion_snapshot = json.dumps({
                "calle": direccion.calle,
                "numero": direccion.numero,
                "piso": direccion.piso,
                "departamento": direccion.departamento,
                "ciudad": direccion.ciudad,
                "codigo_postal": direccion.codigo_postal,
                "referencia": direccion.referencia,
            })

        total_con_envio = total + COSTO_ENVIO

        # Create Pedido
        pedido = Pedido(
            usuario_id=usuario_id,
            estado_id=ID_ESTADO_PENDIENTE,
            direccion_id=direccion_id,
            forma_pago_id=forma_pago_id,
            total=total_con_envio,
            costo_envio=COSTO_ENVIO,
            direccion_snapshot=direccion_snapshot,
        )
        pedido = await uow.pedidos.create(pedido)

        # Create DetallePedido for each item
        for det in detalles_data:
            detalle = DetallePedido(
                pedido_id=pedido.id,
                producto_id=det["producto_id"],
                cantidad=det["cantidad"],
                precio_snapshot=det["precio_snapshot"],
                subtotal=det["subtotal"],
                personalizacion=det["personalizacion"],
            )
            await uow.detalles_pedido.create(detalle)

        # Create initial HistorialEstadoPedido (estado_anterior = NULL)
        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_anterior_id=None,
            estado_nuevo_id=ID_ESTADO_PENDIENTE,
            usuario_id=usuario_id,
            observacion="Pedido creado",
        )
        await uow.historial_estados.create(historial)

        # Refresh with relationships
        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido.id)
            .options(
                selectinload(Pedido.detalles),
                selectinload(Pedido.historial_estados).selectinload(HistorialEstadoPedido.estado_nuevo),
                selectinload(Pedido.estado),
            )
        )
        result = await uow._session.execute(stmt)
        return result.scalar_one_or_none()

    async def listar_mis_pedidos(
        self,
        uow: UnitOfWork,
        usuario_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Pedido], int]:
        """List orders for the authenticated user with pagination."""
        count_stmt = (
            select(func.count())
            .select_from(Pedido)
            .where(Pedido.usuario_id == usuario_id, Pedido.eliminado_en.is_(None))
        )
        result = await uow._session.execute(count_stmt)
        total = result.scalar_one()

        stmt = (
            select(Pedido)
            .where(Pedido.usuario_id == usuario_id, Pedido.eliminado_en.is_(None))
            .options(selectinload(Pedido.estado))
            .order_by(Pedido.creado_en.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await uow._session.execute(stmt)
        pedidos = list(result.scalars().all())

        return pedidos, total

    async def obtener_detalle(
        self,
        uow: UnitOfWork,
        pedido_id: int,
        usuario_id: int,
        roles: list[str],
    ) -> Pedido | None:
        """Get full order detail. Only owner or ADMIN/PEDIDOS can view."""
        stmt = (
            select(Pedido)
            .where(Pedido.id == pedido_id, Pedido.eliminado_en.is_(None))
            .options(
                selectinload(Pedido.detalles),
                selectinload(Pedido.historial_estados).selectinload(HistorialEstadoPedido.estado_nuevo),
                selectinload(Pedido.historial_estados).selectinload(HistorialEstadoPedido.estado_anterior),
                selectinload(Pedido.estado),
            )
        )
        result = await uow._session.execute(stmt)
        pedido = result.scalar_one_or_none()

        if not pedido:
            return None

        is_admin = any(r in roles for r in ["ADMIN", "PEDIDOS"])
        if pedido.usuario_id != usuario_id and not is_admin:
            raise ForbiddenException("No tienes permiso para ver este pedido")

        return pedido

    async def listar_admin(
        self,
        uow: UnitOfWork,
        skip: int = 0,
        limit: int = 20,
        estado_id: int | None = None,
    ) -> tuple[list[Pedido], int]:
        """List all orders for admin/pedidos with optional filters."""
        base_query = select(Pedido).where(Pedido.eliminado_en.is_(None))
        count_query = select(func.count()).select_from(Pedido).where(Pedido.eliminado_en.is_(None))

        if estado_id is not None:
            base_query = base_query.where(Pedido.estado_id == estado_id)
            count_query = count_query.where(Pedido.estado_id == estado_id)

        result = await uow._session.execute(count_query)
        total = result.scalar_one()

        stmt = (
            base_query
            .options(selectinload(Pedido.estado), selectinload(Pedido.usuario))
            .order_by(Pedido.creado_en.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await uow._session.execute(stmt)
        pedidos = list(result.scalars().all())

        return pedidos, total
