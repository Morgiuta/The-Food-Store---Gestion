"""Align initial schema with current ORM models.

Revision ID: 002
Revises: 001
Create Date: 2026-05-13

"""
from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF to_regclass('public.usuario_roles') IS NOT NULL
               AND to_regclass('public.usuarios_roles') IS NULL THEN
                ALTER TABLE usuario_roles RENAME TO usuarios_roles;
            END IF;

            IF to_regclass('public.producto_categorias') IS NOT NULL
               AND to_regclass('public.productos_categorias') IS NULL THEN
                ALTER TABLE producto_categorias RENAME TO productos_categorias;
            END IF;

            IF to_regclass('public.producto_ingredientes') IS NOT NULL
               AND to_regclass('public.productos_ingredientes') IS NULL THEN
                ALTER TABLE producto_ingredientes RENAME TO productos_ingredientes;
            END IF;
        END $$;
        """
    )

    op.execute(
        "ALTER TABLE usuarios_roles "
        "ADD COLUMN IF NOT EXISTS asignado_por_id INTEGER NULL REFERENCES usuarios(id)"
    )
    op.execute(
        "ALTER TABLE estados_pedido "
        "ADD COLUMN IF NOT EXISTS es_terminal BOOLEAN NOT NULL DEFAULT FALSE"
    )
    op.execute(
        "ALTER TABLE detalles_pedido "
        "ADD COLUMN IF NOT EXISTS nombre_snapshot VARCHAR(200) NULL"
    )
    op.execute(
        "ALTER TABLE productos_ingredientes "
        "ADD COLUMN IF NOT EXISTS es_removible BOOLEAN DEFAULT TRUE"
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS configuraciones (
            id SERIAL PRIMARY KEY,
            clave VARCHAR(100) NOT NULL UNIQUE,
            valor TEXT NOT NULL,
            descripcion TEXT NULL,
            creado_en TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            actualizado_en TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_configuraciones_id ON configuraciones (id)")
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_configuraciones_clave ON configuraciones (clave)"
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NULL REFERENCES usuarios(id),
            accion VARCHAR(20) NOT NULL,
            tabla VARCHAR(50) NOT NULL,
            registro_id INTEGER NULL,
            valor_anterior TEXT NULL,
            valor_nuevo TEXT NULL,
            ip_address VARCHAR(45) NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_audit_logs_id ON audit_logs (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_audit_logs_tabla ON audit_logs (tabla)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_registro_id ON audit_logs (registro_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pedidos_usuario_creado "
        "ON pedidos (usuario_id, creado_en)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pedidos_estado_creado "
        "ON pedidos (estado_id, creado_en)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_pagos_pedido_creado "
        "ON pagos (pedido_id, creado_en)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_pagos_pedido_creado")
    op.execute("DROP INDEX IF EXISTS ix_pedidos_estado_creado")
    op.execute("DROP INDEX IF EXISTS ix_pedidos_usuario_creado")
    op.execute("DROP TABLE IF EXISTS audit_logs")
    op.execute("DROP TABLE IF EXISTS configuraciones")
    op.execute("ALTER TABLE productos_ingredientes DROP COLUMN IF EXISTS es_removible")
    op.execute("ALTER TABLE detalles_pedido DROP COLUMN IF EXISTS nombre_snapshot")
    op.execute("ALTER TABLE estados_pedido DROP COLUMN IF EXISTS es_terminal")
    op.execute("ALTER TABLE usuarios_roles DROP COLUMN IF EXISTS asignado_por_id")

    op.execute(
        """
        DO $$
        BEGIN
            IF to_regclass('public.usuarios_roles') IS NOT NULL
               AND to_regclass('public.usuario_roles') IS NULL THEN
                ALTER TABLE usuarios_roles RENAME TO usuario_roles;
            END IF;

            IF to_regclass('public.productos_categorias') IS NOT NULL
               AND to_regclass('public.producto_categorias') IS NULL THEN
                ALTER TABLE productos_categorias RENAME TO producto_categorias;
            END IF;

            IF to_regclass('public.productos_ingredientes') IS NOT NULL
               AND to_regclass('public.producto_ingredientes') IS NULL THEN
                ALTER TABLE productos_ingredientes RENAME TO producto_ingredientes;
            END IF;
        END $$;
        """
    )
