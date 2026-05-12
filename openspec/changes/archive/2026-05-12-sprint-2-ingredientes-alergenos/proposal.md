## Why

Los ingredientes y alérgenos son fundamentales para la venta de productos alimenticios. Aunque el modelo Ingrediente existe (creado en Sprint 0), no hay endpoints CRUD ni interfaz de administración. Los clientes necesitan poder ver los ingredientes y alérgenos de cada producto para tomar decisiones informadas.

## What Changes

- **Backend**: Endpoints CRUD para ingredientes con filtro por alérgeno
- **Frontend Admin**: Página de ingredientes con listado y gestión CRUD
- **Frontend Público**: Los alérgenos se muestran en las fichas de producto (en change de productos)

## Capabilities

### New Capabilities
- `ingrediente-crud`: CRUD de ingredientes con flag de alérgeno y filtro

## Impact

- **Backend**: Se crean `backend/ingredientes/routes/ingredientes.py` y `backend/ingredientes/services/ingrediente_service.py`
- **Frontend**: Página admin de ingredientes con tabla, filtro por alérgeno y CRUD modal
- **Roles**: STOCK y ADMIN pueden CRUD
