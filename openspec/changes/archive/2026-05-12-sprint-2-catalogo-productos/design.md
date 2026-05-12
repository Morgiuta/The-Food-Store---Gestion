# Design: Sprint 2 — Catálogo de Productos

## Architecture Overview

CRUD de productos con M2M a categorías e ingredientes. Catálogo público visible sin auth.

## Components

### Routes — `backend/productos/routes/productos.py`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/productos | Público | Catálogo (paginado, filtro categoría) |
| GET | /api/v1/productos/admin | STOCK, ADMIN | Todos (incluye no disponibles) |
| GET | /api/v1/productos/{id} | Público | Detalle con categorías e ingredientes |
| POST | /api/v1/productos | STOCK, ADMIN | Crear |
| PUT | /api/v1/productos/{id} | STOCK, ADMIN | Editar |
| DELETE | /api/v1/productos/{id} | STOCK, ADMIN | Soft delete |

### Service — `backend/productos/services/producto_service.py`
- `list_public(session, skip, limit, categoria_id)` — solo disponibles + no eliminados
- `list_admin(session, skip, limit)` — todos
- `get_by_id(session, id)` — detalle con categorías e ingredientes
- `create(session, data)` — crear con asignación de categorías e ingredientes
- `update(session, id, data)` — editar + reasignar relaciones M2M
- `delete(session, id)` — soft delete

### Frontend Admin — ProductosPage
- Tabla con nombre, precio, stock, disponible, acciones
- Modal crear/editar con selector de categorías e ingredientes

### Frontend Público — CatalogPage
- Grid de productos con precio y disponibilidad
- Filtro por categoría
