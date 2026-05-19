"""Demo data seed for local dashboard and ABM screens.

Creates categories, ingredients, products, customers, orders and payments
that make the admin dashboard charts and CRUD tables show useful data.
The script is idempotent for demo orders through the payment external_reference.
"""

import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select

from backend.auth.models import Rol, Usuario, UsuarioRol
from backend.core.database import async_session_factory
from backend.core.security import get_password_hash
from backend.ingredientes.models import Ingrediente
from backend.categorias.models import Categoria
from backend.pagos.models import FormaPago, Pago
from backend.pedidos.models import DetallePedido, EstadoPedido, HistorialEstadoPedido, Pedido
from backend.productos.models import Producto, ProductoCategoria, ProductoIngrediente
from backend.seed import seed_database


DEMO_PREFIX = "Demo"
DEMO_ORDER_PREFIX = "demo-dashboard"


async def get_or_create(session, model, defaults: dict | None = None, **lookup):
    result = await session.execute(select(model).filter_by(**lookup))
    instance = result.scalar_one_or_none()
    if instance:
        return instance

    data = {**lookup, **(defaults or {})}
    instance = model(**data)
    session.add(instance)
    await session.flush()
    return instance


async def ensure_role(session, user: Usuario, role_name: str) -> None:
    role = (await session.execute(select(Rol).where(Rol.nombre == role_name))).scalar_one()
    existing = await session.execute(
        select(UsuarioRol).where(
            UsuarioRol.usuario_id == user.id,
            UsuarioRol.rol_id == role.id,
        )
    )
    if not existing.scalar_one_or_none():
        session.add(UsuarioRol(usuario_id=user.id, rol_id=role.id))


async def seed_demo_data() -> None:
    await seed_database()

    now = datetime.now(timezone.utc)

    async with async_session_factory() as session:
        async with session.begin():
            client_users = []
            for index in range(1, 5):
                user = await get_or_create(
                    session,
                    Usuario,
                    nombre=f"Cliente Demo {index}",
                    email=f"cliente.demo{index}@foodstore.com",
                    defaults={
                        "password_hash": get_password_hash("Cliente123!"),
                        "telefono": f"11223344{index}",
                    },
                )
                await ensure_role(session, user, "CLIENT")
                client_users.append(user)

            categorias_data = [
                ("Demo Sandwiches", "Opciones listas para almuerzos y meriendas."),
                ("Demo Ensaladas", "Platos frescos con vegetales y proteínas."),
                ("Demo Bebidas", "Bebidas frías para acompañar pedidos."),
                ("Demo Postres", "Dulces y porciones individuales."),
                ("Demo Combos", "Promociones armadas para venta rápida."),
            ]
            categorias = {}
            for nombre, descripcion in categorias_data:
                categoria = await get_or_create(
                    session,
                    Categoria,
                    nombre=nombre,
                    defaults={"descripcion": descripcion, "imagen_url": None},
                )
                categoria.descripcion = descripcion
                categorias[nombre] = categoria

            ingredientes_data = [
                ("Pan artesanal", False),
                ("Pollo grillado", False),
                ("Queso", True),
                ("Tomate", False),
                ("Lechuga", False),
                ("Huevo", True),
                ("Nueces", True),
                ("Chocolate", False),
            ]
            ingredientes = {}
            for nombre, es_alergeno in ingredientes_data:
                ingrediente = await get_or_create(
                    session,
                    Ingrediente,
                    nombre=nombre,
                    defaults={"descripcion": None, "es_alergeno": es_alergeno},
                )
                ingrediente.es_alergeno = es_alergeno
                ingredientes[nombre] = ingrediente

            productos_data = [
                ("Demo Sandwich de pollo", "Pan artesanal, pollo grillado y vegetales.", "Demo Sandwiches", Decimal("6800.00"), 18, ["Pan artesanal", "Pollo grillado", "Tomate", "Lechuga"]),
                ("Demo Sandwich veggie", "Opción vegetariana con queso y vegetales.", "Demo Sandwiches", Decimal("5900.00"), 3, ["Pan artesanal", "Queso", "Tomate", "Lechuga"]),
                ("Demo Ensalada caesar", "Base verde con pollo, queso y croutons.", "Demo Ensaladas", Decimal("7200.00"), 9, ["Pollo grillado", "Queso", "Lechuga"]),
                ("Demo Ensalada proteica", "Mix fresco con huevo y vegetales.", "Demo Ensaladas", Decimal("6500.00"), 2, ["Huevo", "Tomate", "Lechuga"]),
                ("Demo Limonada grande", "Limonada natural fría.", "Demo Bebidas", Decimal("2400.00"), 24, []),
                ("Demo Agua saborizada", "Botella individual.", "Demo Bebidas", Decimal("1800.00"), 4, []),
                ("Demo Brownie", "Porción húmeda de chocolate.", "Demo Postres", Decimal("3200.00"), 14, ["Chocolate"]),
                ("Demo Tarta de nuez", "Porción individual con nueces.", "Demo Postres", Decimal("3900.00"), 1, ["Nueces"]),
                ("Demo Combo almuerzo", "Sandwich, bebida y postre.", "Demo Combos", Decimal("10900.00"), 12, ["Pan artesanal", "Pollo grillado", "Chocolate"]),
                ("Demo Combo saludable", "Ensalada y bebida.", "Demo Combos", Decimal("8900.00"), 7, ["Lechuga", "Tomate"]),
            ]
            productos = []
            for nombre, descripcion, categoria_nombre, precio, stock, ingredient_names in productos_data:
                producto = await get_or_create(
                    session,
                    Producto,
                    nombre=nombre,
                    defaults={
                        "descripcion": descripcion,
                        "imagen_url": None,
                        "precio": precio,
                        "stock_cantidad": stock,
                        "disponible": True,
                    },
                )
                producto.descripcion = descripcion
                producto.precio = precio
                producto.stock_cantidad = stock
                producto.disponible = True
                producto.eliminado_en = None
                productos.append(producto)
                await session.flush()

                categoria = categorias[categoria_nombre]
                await get_or_create(
                    session,
                    ProductoCategoria,
                    producto_id=producto.id,
                    categoria_id=categoria.id,
                )
                for ingredient_name in ingredient_names:
                    await get_or_create(
                        session,
                        ProductoIngrediente,
                        producto_id=producto.id,
                        ingrediente_id=ingredientes[ingredient_name].id,
                        defaults={"es_removible": True},
                    )

            existing_demo_orders = await session.execute(
                select(Pago.id).where(Pago.external_reference.like(f"{DEMO_ORDER_PREFIX}-%"))
            )
            if existing_demo_orders.scalars().first():
                print("Demo sales already exist; products/categories were refreshed.")
                return

            estados = {
                estado.nombre: estado
                for estado in (await session.execute(select(EstadoPedido))).scalars().all()
            }
            forma_pago = (
                await session.execute(select(FormaPago).where(FormaPago.nombre == "Tarjeta de crédito"))
            ).scalar_one()

            ventas_plan = [
                (0, "ENTREGADO", [(0, 2), (4, 2), (6, 1)]),
                (1, "CONFIRMADO", [(8, 1), (5, 2)]),
                (2, "ENTREGADO", [(2, 2), (6, 2)]),
                (3, "EN_PREPARACIÓN", [(1, 1), (4, 3), (7, 1)]),
                (5, "ENTREGADO", [(3, 2), (9, 1)]),
                (8, "ENTREGADO", [(0, 1), (8, 1)]),
                (12, "CONFIRMADO", [(2, 3), (5, 2)]),
                (18, "ENTREGADO", [(8, 2), (6, 3)]),
                (25, "ENTREGADO", [(1, 2), (4, 4)]),
                (40, "ENTREGADO", [(9, 3), (7, 2)]),
                (75, "ENTREGADO", [(0, 3), (2, 2), (6, 1)]),
                (120, "CONFIRMADO", [(8, 2), (5, 2)]),
            ]

            for order_index, (days_ago, estado_nombre, items) in enumerate(ventas_plan, start=1):
                created_at = now - timedelta(days=days_ago, hours=order_index)
                total = Decimal("0.00")
                detalles = []
                for product_index, cantidad in items:
                    producto = productos[product_index]
                    subtotal = Decimal(producto.precio) * cantidad
                    total += subtotal
                    detalles.append((producto, cantidad, subtotal))

                pedido = Pedido(
                    usuario_id=client_users[order_index % len(client_users)].id,
                    estado_id=estados[estado_nombre].id,
                    forma_pago_id=forma_pago.id,
                    total=total,
                    costo_envio=Decimal("0.00"),
                    direccion_snapshot="Av. Demo 123, CABA",
                    creado_en=created_at,
                    actualizado_en=created_at,
                )
                session.add(pedido)
                await session.flush()

                for producto, cantidad, subtotal in detalles:
                    session.add(
                        DetallePedido(
                            pedido_id=pedido.id,
                            producto_id=producto.id,
                            nombre_snapshot=producto.nombre,
                            cantidad=cantidad,
                            precio_snapshot=producto.precio,
                            subtotal=subtotal,
                            creado_en=created_at,
                            actualizado_en=created_at,
                        )
                    )

                session.add(
                    HistorialEstadoPedido(
                        pedido_id=pedido.id,
                        estado_anterior_id=None,
                        estado_nuevo_id=pedido.estado_id,
                        usuario_id=None,
                        observacion="Pedido demo para dashboard",
                        timestamp=created_at,
                        creado_en=created_at,
                    )
                )
                session.add(
                    Pago(
                        pedido_id=pedido.id,
                        monto=total,
                        mp_payment_id=f"demo-{order_index:03d}",
                        mp_status="approved",
                        external_reference=f"{DEMO_ORDER_PREFIX}-{order_index:03d}",
                        idempotency_key=f"{DEMO_ORDER_PREFIX}-{order_index:03d}",
                        creado_en=created_at,
                        actualizado_en=created_at,
                    )
                )

        print("Demo data completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
