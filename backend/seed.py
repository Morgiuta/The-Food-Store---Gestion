"""
Seed script for The Food Store database.
Creates initial roles, admin user, order states, and payment methods.
"""

import asyncio

from sqlalchemy import select

from backend.auth.models import Rol, Usuario, UsuarioRol
from backend.core.database import async_session_factory
from backend.core.security import get_password_hash
from backend.pagos.models import FormaPago
from backend.pedidos.models import EstadoPedido


async def seed_database() -> None:
    """Seed initial data into the database."""

    async with async_session_factory() as session:
        async with session.begin():
            existing_roles = await session.execute(select(Rol).limit(1))
            if existing_roles.scalars().first():
                print("Database already seeded. Skipping.")
                return

            admin_role = Rol(nombre="ADMIN", descripcion="Acceso total al sistema")
            stock_role = Rol(nombre="STOCK", descripcion="Gestión de inventario y productos")
            pedidos_role = Rol(nombre="PEDIDOS", descripcion="Gestión de pedidos")
            client_role = Rol(nombre="CLIENT", descripcion="Usuario cliente")
            session.add_all([admin_role, stock_role, pedidos_role, client_role])
            await session.flush()

            password_hash = get_password_hash("Admin123!")
            admin_user = Usuario(
                nombre="Administrador",
                email="admin@foodstore.com",
                password_hash=password_hash,
                telefono=None,
            )
            session.add(admin_user)
            await session.flush()

            admin_rol = UsuarioRol(usuario_id=admin_user.id, rol_id=admin_role.id)
            session.add(admin_rol)

            pendiente = EstadoPedido(nombre="PENDIENTE", descripcion="Pedido creado, esperando confirmación")
            confirmado = EstadoPedido(nombre="CONFIRMADO", descripcion="Pedido confirmado")
            en_preparacion = EstadoPedido(nombre="EN_PREPARACIÓN", descripcion="Pedido en preparación")
            en_camino = EstadoPedido(nombre="EN_CAMINO", descripcion="Pedido en camino al cliente")
            entregado = EstadoPedido(nombre="ENTREGADO", descripcion="Pedido entregado al cliente")
            cancelado = EstadoPedido(nombre="CANCELADO", descripcion="Pedido cancelado")
            session.add_all([pendiente, confirmado, en_preparacion, en_camino, entregado, cancelado])

            credito = FormaPago(nombre="Tarjeta de crédito", activo=True)
            debito = FormaPago(nombre="Tarjeta de débito", activo=True)
            session.add_all([credito, debito])

        print("Seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed_database())
