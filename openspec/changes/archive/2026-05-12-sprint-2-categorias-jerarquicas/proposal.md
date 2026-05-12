## Why

El catálogo de productos necesita categorías jerárquicas para organizar los productos de forma intuitiva. Aunque el modelo Categoria ya existe (creado en Sprint 0), no hay endpoints para CRUD ni interfaz de administración. Este change implementa el CRUD completo de categorías con soporte jerárquico (padre-hijo), validación de ciclos y soft delete.

## What Changes

- **Backend**: Endpoints CRUD completos para categorías con árbol jerárquico, validación de ciclos, y protección de eliminación si tiene productos
- **Frontend Admin**: Árbol de categorías visual con creación, edición y eliminación
- **Frontend Público**: Visualización del árbol de categorías para filtrar productos

## Capabilities

### New Capabilities
- `categoria-crud`: CRUD completo de categorías con árbol jerárquico (crear, listar árbol, editar, soft delete)
- `frontend-admin-categorias`: Interfaz de administración de categorías con árbol visual

### Modified Capabilities
- Ninguna (es funcionalidad nueva que usa el modelo existente)

## Impact

- **Backend**: Se crean `backend/categorias/routes/categorias.py` y `backend/categorias/services/categoria_service.py`
- **Frontend**: Página admin de categorías con árbol interactivo. Endpoints públicos GET /categorias para el catálogo.
- **Roles**: STOCK y ADMIN pueden crear/editar/eliminar. GET público.
