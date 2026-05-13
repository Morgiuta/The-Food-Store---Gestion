"""
Admin service for dashboard statistics and metrics.
"""
from datetime import date, datetime, timezone, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import func, select, case

from backend.core.uow import UnitOfWork
from backend.pedidos.models.pedido import Pedido
from backend.pedidos.models.detalle_pedido import DetallePedido
from backend.pedidos.models.estado_pedido import EstadoPedido
from backend.productos.models.producto import Producto
from backend.auth.models.usuario import Usuario

ID_PENDIENTE = 1


class AdminStatsService:
    """Service for admin dashboard statistics."""

    async def get_stats(self, uow: UnitOfWork) -> dict[str, Any]:
        """Get main KPIs for the dashboard."""
        stmt_ventas = select(
            func.coalesce(func.sum(Pedido.total), 0)
        ).where(Pedido.estado_id > ID_PENDIENTE, Pedido.eliminado_en.is_(None))
        result = await uow._session.execute(stmt_ventas)
        total_ventas = result.scalar_one()

        hoy = date.today()
        stmt_pedidos_hoy = select(
            func.count(Pedido.id)
        ).where(
            func.date(Pedido.creado_en) == hoy,
            Pedido.eliminado_en.is_(None),
        )
        result = await uow._session.execute(stmt_pedidos_hoy)
        pedidos_hoy = result.scalar_one()

        stmt_usuarios = select(func.count(Usuario.id)).where(Usuario.eliminado_en.is_(None))
        result = await uow._session.execute(stmt_usuarios)
        usuarios_activos = result.scalar_one()

        stmt_stock_bajo = select(func.count(Producto.id)).where(
            Producto.stock_cantidad < 5,
            Producto.disponible == True,  # noqa: E712
            Producto.eliminado_en.is_(None),
        )
        result = await uow._session.execute(stmt_stock_bajo)
        stock_bajo = result.scalar_one()

        return {
            "total_ventas": total_ventas,
            "pedidos_hoy": pedidos_hoy,
            "usuarios_activos": usuarios_activos,
            "stock_bajo": stock_bajo,
        }

    async def get_revenue(self, uow: UnitOfWork, periodo: str = "day") -> list[dict[str, Any]]:
        """Get revenue aggregated by period (day, week, month)."""
        if periodo == "week":
            trunc = "week"
            days_back = 28
        elif periodo == "month":
            trunc = "month"
            days_back = 180
        else:
            trunc = "day"
            days_back = 7

        desde = datetime.now(timezone.utc) - timedelta(days=days_back)

        stmt = select(
            func.date_trunc(trunc, Pedido.creado_en).label("fecha"),
            func.sum(Pedido.total).label("ingresos"),
        ).where(
            Pedido.creado_en >= desde,
            Pedido.estado_id > ID_PENDIENTE,
            Pedido.eliminado_en.is_(None),
        ).group_by(
            func.date_trunc(trunc, Pedido.creado_en)
        ).order_by(
            func.date_trunc(trunc, Pedido.creado_en)
        )

        result = await uow._session.execute(stmt)
        rows = result.all()

        return [
            {
                "fecha": str(row.fecha) if hasattr(row, 'fecha') else str(row[0]),
                "ingresos": row.ingresos if hasattr(row, 'ingresos') else row[1],
            }
            for row in rows
        ]

    async def get_orders_by_status(self, uow: UnitOfWork) -> list[dict[str, Any]]:
        """Get order counts grouped by status."""
        stmt = select(
            EstadoPedido.nombre.label("estado"),
            func.count(Pedido.id).label("cantidad"),
        ).join(
            Pedido, Pedido.estado_id == EstadoPedido.id, isouter=True
        ).where(
            Pedido.eliminado_en.is_(None),
        ).group_by(
            EstadoPedido.id, EstadoPedido.nombre
        ).order_by(
            EstadoPedido.id
        )

        result = await uow._session.execute(stmt)
        rows = result.all()

        return [
            {"estado": row.estado, "cantidad": row.cantidad}
            for row in rows
        ]

    async def get_products_stats(self, uow: UnitOfWork) -> dict[str, Any]:
        """Get low stock products and best sellers."""
        stmt_bajo = select(Producto).where(
            Producto.stock_cantidad < 5,
            Producto.disponible == True,  # noqa: E712
            Producto.eliminado_en.is_(None),
        ).order_by(Producto.stock_cantidad).limit(10)
        result = await uow._session.execute(stmt_bajo)
        stock_bajo = result.scalars().all()

        stmt_vendidos = select(
            DetallePedido.producto_id,
            Producto.nombre,
            func.sum(DetallePedido.cantidad).label("total_vendido"),
        ).join(
            Producto, DetallePedido.producto_id == Producto.id
        ).join(
            Pedido, DetallePedido.pedido_id == Pedido.id
        ).where(
            Pedido.estado_id > ID_PENDIENTE,
            Pedido.eliminado_en.is_(None),
        ).group_by(
            DetallePedido.producto_id, Producto.nombre
        ).order_by(
            func.sum(DetallePedido.cantidad).desc()
        ).limit(10)

        result = await uow._session.execute(stmt_vendidos)
        mas_vendidos = result.all()

        return {
            "stock_bajo": [
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "stock_cantidad": p.stock_cantidad,
                    "disponible": p.disponible,
                }
                for p in stock_bajo
            ],
            "mas_vendidos": [
                {
                    "id": row.producto_id,
                    "nombre": row.nombre,
                    "total_vendido": int(row.total_vendido),
                }
                for row in mas_vendidos
            ],
        }
