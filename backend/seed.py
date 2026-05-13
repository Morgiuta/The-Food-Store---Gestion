"""
Seed script for The Food Store database.
Creates initial roles, admin user, order states, and payment methods.
Idempotent: safe to run multiple times (uses INSERT ON CONFLICT DO NOTHING).
"""

import asyncio

from sqlalchemy import select, text

from backend.auth.models import Rol, Usuario, UsuarioRol
from backend.core.database import async_session_factory
from backend.core.security import get_password_hash
from backend.pagos.models import FormaPago
from backend.pedidos.models import EstadoPedido


async def seed_database() -> None:
    """Seed initial data into the database. Idempotent."""

    async with async_session_factory() as session:
        async with session.begin():
            # Roles — ON CONFLICT DO NOTHING por nombre UNIQUE
            roles_data = [
                {"nombre": "ADMIN", "descripcion": "Acceso total al sistema"},
                {"nombre": "STOCK", "descripcion": "Gestión de inventario y productos"},
                {"nombre": "PEDIDOS", "descripcion": "Gestión de pedidos"},
                {"nombre": "CLIENT", "descripcion": "Usuario cliente"},
            ]
            for r in roles_data:
                existing = await session.execute(select(Rol).where(Rol.nombre == r["nombre"]))
                if not existing.scalar_one_or_none():
                    session.add(Rol(**r))

            await session.flush()

            # Admin user — ON CONFLICT DO NOTHING por email UNIQUE
            admin_user = None
            result = await session.execute(select(Usuario).where(Usuario.email == "admin@foodstore.com"))
            admin_user = result.scalar_one_or_none()
            if not admin_user:
                admin_user = Usuario(
                    nombre="Administrador",
                    email="admin@foodstore.com",
                    password_hash=get_password_hash("Admin123!"),
                    telefono=None,
                )
                session.add(admin_user)
                await session.flush()

                # Asignar rol ADMIN
                admin_role = await session.execute(select(Rol).where(Rol.nombre == "ADMIN"))
                admin_role = admin_role.scalar_one()
                session.add(UsuarioRol(usuario_id=admin_user.id, rol_id=admin_role.id))

            # Estados de pedido — ON CONFLICT DO NOTHING por nombre UNIQUE
            estados_data = [
                {"nombre": "PENDIENTE", "descripcion": "Pedido creado, esperando confirmación", "es_terminal": False},
                {"nombre": "CONFIRMADO", "descripcion": "Pedido confirmado", "es_terminal": False},
                {"nombre": "EN_PREPARACIÓN", "descripcion": "Pedido en preparación", "es_terminal": False},
                {"nombre": "EN_CAMINO", "descripcion": "Pedido en camino al cliente", "es_terminal": False},
                {"nombre": "ENTREGADO", "descripcion": "Pedido entregado al cliente", "es_terminal": True},
                {"nombre": "CANCELADO", "descripcion": "Pedido cancelado", "es_terminal": True},
            ]
            for e in estados_data:
                existing = await session.execute(select(EstadoPedido).where(EstadoPedido.nombre == e["nombre"]))
                if not existing.scalar_one_or_none():
                    session.add(EstadoPedido(**e))

            # Formas de pago — ON CONFLICT DO NOTHING por nombre UNIQUE
            formas_data = [
                {"nombre": "Tarjeta de crédito", "activo": True},
                {"nombre": "Tarjeta de débito", "activo": True},
            ]
            for f in formas_data:
                existing = await session.execute(select(FormaPago).where(FormaPago.nombre == f["nombre"]))
                if not existing.scalar_one_or_none():
                    session.add(FormaPago(**f))

        print("✅ Seed completed successfully (idempotent).")


if __name__ == "__main__":
    asyncio.run(seed_database())
