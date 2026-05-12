from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import ValidationException
from backend.productos.models.producto import Producto

# Tarifa plana de envío
COSTO_ENVIO = Decimal("500.00")


class CheckoutService:
    """Servicio para validar checkout y calcular totales."""

    async def validar_stock(
        self, session: AsyncSession, items: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Valida que haya stock disponible para todos los items.
        Usa SELECT FOR UPDATE para evitar race conditions.
        """
        errores = []
        items_validados = []

        for item in items:
            producto_id = item.get("producto_id")
            cantidad = item.get("cantidad", 1)

            if not producto_id:
                errores.append("Producto sin ID especificado")
                continue

            # SELECT FOR UPDATE para bloquear la fila
            stmt = select(Producto).where(Producto.id == producto_id).with_for_update()
            result = await session.execute(stmt)
            producto = result.scalar_one_or_none()

            if not producto:
                errores.append(f"Producto ID {producto_id} no encontrado")
                continue

            if producto.eliminado_en:
                errores.append(f"Producto '{producto.nombre}' ya no está disponible")
                continue

            if not producto.disponible:
                errores.append(f"Producto '{producto.nombre}' no está disponible")
                continue

            if producto.stock_cantidad < cantidad:
                errores.append(
                    f"Stock insuficiente para '{producto.nombre}': "
                    f"disponible {producto.stock_cantidad}, solicitado {cantidad}"
                )
                continue

            items_validados.append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio": float(producto.precio),
                "nombre": producto.nombre,
            })

        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "items_validados": items_validados,
        }

    async def calcular_total(
        self, items: list[dict[str, Any]], direccion_id: int | None = None
    ) -> dict[str, Any]:
        """
        Calcula el subtotal, costo de envío y total.
        Por ahora usa tarifa plana de $500.
        """
        subtotal = Decimal("0")
        for item in items:
            cantidad = item.get("cantidad", 1)
            precio = Decimal(str(item.get("precio", 0)))
            subtotal += precio * cantidad

        # Tarifa plana de envío
        costo_envio = COSTO_ENVIO
        total = subtotal + costo_envio

        return {
            "subtotal": float(subtotal),
            "costo_envio": float(costo_envio),
            "total": float(total),
            "direccion_id": direccion_id,
        }