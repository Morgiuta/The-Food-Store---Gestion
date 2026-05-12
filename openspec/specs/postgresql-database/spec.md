# postgresql-database Specification

## Purpose
TBD - created by archiving change sprint-0-infraestructura. Update Purpose after archive.
## Requirements
### Requirement: PostgreSQL database connection
The system SHALL establish a persistent connection to PostgreSQL with SQLAlchemy ORM, configurable via environment variables (host, port, user, password, database).

#### Scenario: Database connection is established
- **WHEN** the application starts
- **THEN** a connection pool to PostgreSQL is initialized and the application is ready to accept queries

### Requirement: Alembic migration system
The system SHALL use Alembic for database schema versioning, with an initial migration creating the ERD v5 schema (16 tables).

#### Scenario: Migrations can be applied and reverted
- **WHEN** `alembic upgrade head` is executed
- **THEN** all pending migrations are applied and schema is current
- **WHEN** `alembic downgrade -1` is executed
- **THEN** the most recent migration is reverted

### Requirement: ERD v5 schema implementation
The system SHALL implement the complete ERD v5 with 16 tables: usuarios, roles, usuario_rol, categorias, ingredientes, productos, producto_categoria, producto_ingrediente, direcciones, detalles_pedido, pedidos, historial_estado_pedido, refresh_tokens, pagos, ingredientes_alergenicos_producto, and sesiones.

#### Scenario: All tables are created with correct relationships
- **WHEN** migrations are applied
- **THEN** all 16 tables exist in the database with correct foreign key constraints and indexes

### Requirement: Soft delete pattern
The system SHALL implement soft delete by adding an `eliminado_en` nullable TIMESTAMP column to user-facing entities (usuarios, productos, categorias, ingredientes, direcciones, pedidos).

#### Scenario: Soft deleted records are not returned by default
- **WHEN** a record is soft deleted (eliminado_en is set)
- **THEN** queries do not return this record unless explicitly filtering by eliminado_en

### Requirement: Audit timestamps
The system SHALL add audit columns (`creado_en`, `actualizado_en`) to all relevant tables to track creation and last modification timestamps.

#### Scenario: Timestamps are automatically managed
- **WHEN** a record is created
- **THEN** creado_en is set to current timestamp
- **WHEN** a record is updated
- **THEN** actualizado_en is updated to current timestamp

### Requirement: Seed data
The system SHALL provide an idempotent seed script that populates initial data: roles (ADMIN, STOCK, PEDIDOS, CLIENT), one admin user, and initial payment methods.

#### Scenario: Seed data is applied
- **WHEN** the seed script is run
- **THEN** roles and admin user are created (or skipped if already exist)

