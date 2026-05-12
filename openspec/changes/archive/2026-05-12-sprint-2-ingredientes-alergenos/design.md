# Design: Sprint 2 — Ingredientes y Alérgenos

## Architecture Overview

CRUD de ingredientes usando modelo existente. Misma estructura que categorías.

## Components

### Routes — `backend/ingredientes/routes/ingredientes.py`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/ingredientes | STOCK, ADMIN | Listar (filtro es_alergeno, paginado) |
| GET | /api/v1/ingredientes/{id} | STOCK, ADMIN | Detalle |
| POST | /api/v1/ingredientes | STOCK, ADMIN | Crear |
| PUT | /api/v1/ingredientes/{id} | STOCK, ADMIN | Editar |
| DELETE | /api/v1/ingredientes/{id} | STOCK, ADMIN | Soft delete |

### Service — `backend/ingredientes/services/ingrediente_service.py`
- `list(session, es_alergeno, skip, limit)` — listar con filtro opcional
- `get_by_id(session, id)` — detalle
- `create(session, data)` — validar nombre único
- `update(session, id, data)` — editar
- `delete(session, id)` — soft delete

### Frontend Admin — IngredientesPage
- Tabla con nombre, flag alérgeno (badge), acciones
- Filtro por alérgeno
- Modal de crear/editar
- Confirmación de eliminación
