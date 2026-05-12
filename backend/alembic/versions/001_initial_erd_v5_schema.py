"""Initial ERD v5 schema

Revision ID: 001
Revises:
Create Date: 2026-05-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ─── Roles ────────────────────────────────────────────────────────────
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_roles_id"), "roles", ["id"])

    # ─── Usuarios ─────────────────────────────────────────────────────────
    op.create_table(
        "usuarios",
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("telefono", sa.String(length=20), nullable=True),
        sa.Column(
            "eliminado_en", sa.DateTime(timezone=True), nullable=True, index=True
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=True)
    op.create_index(op.f("ix_usuarios_id"), "usuarios", ["id"])

    # ─── UsuarioRol (M2M) ─────────────────────────────────────────────────
    op.create_table(
        "usuario_roles",
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("rol_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["rol_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("usuario_id", "rol_id"),
    )
    op.create_index(op.f("ix_usuario_roles_id"), "usuario_roles", ["id"])

    # ─── RefreshTokens ────────────────────────────────────────────────────
    op.create_table(
        "refresh_tokens",
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revocado_en", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        op.f("ix_refresh_tokens_id"), "refresh_tokens", ["id"]
    )
    op.create_index(
        op.f("ix_refresh_tokens_token"), "refresh_tokens", ["token"], unique=True
    )

    # ─── Direcciones ──────────────────────────────────────────────────────
    op.create_table(
        "direcciones",
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("calle", sa.String(length=200), nullable=False),
        sa.Column("numero", sa.String(length=20), nullable=False),
        sa.Column("piso", sa.String(length=10), nullable=True),
        sa.Column("departamento", sa.String(length=10), nullable=True),
        sa.Column("ciudad", sa.String(length=100), nullable=False),
        sa.Column("codigo_postal", sa.String(length=20), nullable=False),
        sa.Column("referencia", sa.Text(), nullable=True),
        sa.Column("es_predeterminada", sa.Boolean(), nullable=False, default=False),
        sa.Column(
            "eliminado_en", sa.DateTime(timezone=True), nullable=True, index=True
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_direcciones_id"), "direcciones", ["id"])

    # ─── Categorias ───────────────────────────────────────────────────────
    op.create_table(
        "categorias",
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("imagen_url", sa.String(length=500), nullable=True),
        sa.Column("padre_id", sa.Integer(), nullable=True),
        sa.Column(
            "eliminado_en", sa.DateTime(timezone=True), nullable=True, index=True
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["padre_id"],
            ["categorias.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categorias_id"), "categorias", ["id"])

    # ─── Ingredientes ─────────────────────────────────────────────────────
    op.create_table(
        "ingredientes",
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("es_alergeno", sa.Boolean(), nullable=False, default=False),
        sa.Column(
            "eliminado_en", sa.DateTime(timezone=True), nullable=True, index=True
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ingredientes_id"), "ingredientes", ["id"])

    # ─── Productos ────────────────────────────────────────────────────────
    op.create_table(
        "productos",
        sa.Column("nombre", sa.String(length=200), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("imagen_url", sa.String(length=500), nullable=True),
        sa.Column(
            "precio", sa.Numeric(precision=10, scale=2), nullable=False
        ),
        sa.Column("stock_cantidad", sa.Integer(), nullable=False, default=0),
        sa.Column("disponible", sa.Boolean(), nullable=False, default=True),
        sa.Column(
            "eliminado_en", sa.DateTime(timezone=True), nullable=True, index=True
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_productos_id"), "productos", ["id"])

    # ─── ProductoCategoria (M2M) ──────────────────────────────────────────
    op.create_table(
        "producto_categorias",
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("categoria_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["categoria_id"],
            ["categorias.id"],
        ),
        sa.ForeignKeyConstraint(
            ["producto_id"],
            ["productos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("producto_id", "categoria_id"),
    )
    op.create_index(op.f("ix_producto_categorias_id"), "producto_categorias", ["id"])

    # ─── ProductoIngrediente (M2M) ────────────────────────────────────────
    op.create_table(
        "producto_ingredientes",
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("ingrediente_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["ingrediente_id"],
            ["ingredientes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["producto_id"],
            ["productos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("producto_id", "ingrediente_id"),
    )
    op.create_index(
        op.f("ix_producto_ingredientes_id"), "producto_ingredientes", ["id"]
    )

    # ─── FormasPago ───────────────────────────────────────────────────────
    op.create_table(
        "formas_pago",
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, default=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_formas_pago_id"), "formas_pago", ["id"])

    # ─── EstadosPedido ────────────────────────────────────────────────────
    op.create_table(
        "estados_pedido",
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_estados_pedido_id"), "estados_pedido", ["id"])

    # ─── Pedidos ──────────────────────────────────────────────────────────
    op.create_table(
        "pedidos",
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("estado_id", sa.Integer(), nullable=False),
        sa.Column("direccion_id", sa.Integer(), nullable=True),
        sa.Column("forma_pago_id", sa.Integer(), nullable=True),
        sa.Column("total", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "costo_envio", sa.Numeric(precision=10, scale=2), nullable=False, default=0
        ),
        sa.Column("direccion_snapshot", sa.Text(), nullable=True),
        sa.Column(
            "eliminado_en", sa.DateTime(timezone=True), nullable=True, index=True
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["direccion_id"],
            ["direcciones.id"],
        ),
        sa.ForeignKeyConstraint(
            ["estado_id"],
            ["estados_pedido.id"],
        ),
        sa.ForeignKeyConstraint(
            ["forma_pago_id"],
            ["formas_pago.id"],
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pedidos_id"), "pedidos", ["id"])

    # ─── DetallesPedido ───────────────────────────────────────────────────
    op.create_table(
        "detalles_pedido",
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("producto_id", sa.Integer(), nullable=True),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column(
            "precio_snapshot", sa.Numeric(precision=10, scale=2), nullable=False
        ),
        sa.Column("subtotal", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("personalizacion", sa.ARRAY(sa.Integer()), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["pedido_id"],
            ["pedidos.id"],
        ),
        sa.ForeignKeyConstraint(
            ["producto_id"],
            ["productos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_detalles_pedido_id"), "detalles_pedido", ["id"])

    # ─── HistorialEstadosPedido ───────────────────────────────────────────
    op.create_table(
        "historial_estados_pedido",
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("estado_anterior_id", sa.Integer(), nullable=True),
        sa.Column("estado_nuevo_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("observacion", sa.Text(), nullable=True),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["estado_anterior_id"],
            ["estados_pedido.id"],
        ),
        sa.ForeignKeyConstraint(
            ["estado_nuevo_id"],
            ["estados_pedido.id"],
        ),
        sa.ForeignKeyConstraint(
            ["pedido_id"],
            ["pedidos.id"],
        ),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_historial_estados_pedido_id"),
        "historial_estados_pedido",
        ["id"],
    )

    # ─── Pagos ────────────────────────────────────────────────────────────
    op.create_table(
        "pagos",
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("monto", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("mp_payment_id", sa.String(length=255), nullable=True),
        sa.Column("mp_status", sa.String(length=50), nullable=True),
        sa.Column("external_reference", sa.String(length=255), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["pedido_id"],
            ["pedidos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pagos_id"), "pagos", ["id"])
    op.create_index(
        op.f("ix_pagos_external_reference"),
        "pagos",
        ["external_reference"],
    )
    op.create_index(
        op.f("ix_pagos_idempotency_key"),
        "pagos",
        ["idempotency_key"],
        unique=True,
    )


def downgrade() -> None:
    """Drop all tables in reverse order of creation."""
    op.drop_table("historial_estados_pedido")
    op.drop_table("detalles_pedido")
    op.drop_table("pagos")
    op.drop_table("pedidos")
    op.drop_table("estados_pedido")
    op.drop_table("formas_pago")
    op.drop_table("producto_ingredientes")
    op.drop_table("producto_categorias")
    op.drop_table("productos")
    op.drop_table("ingredientes")
    op.drop_table("categorias")
    op.drop_table("direcciones")
    op.drop_table("refresh_tokens")
    op.drop_table("usuario_roles")
    op.drop_table("usuarios")
    op.drop_table("roles")
