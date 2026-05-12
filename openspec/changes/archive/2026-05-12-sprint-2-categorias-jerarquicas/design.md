# Design: Sprint 2 — Categorías Jerárquicas

## Architecture Overview

CRUD de categorías usando el modelo existente. El árbol jerárquico se construye desde la raíz hacia abajo usando relaciones SQLAlchemy.

```
CategoriaRouter → CategoriaService → CategoriaRepository → Categoria (modelo)
                                                          → ProductoCategoria (count)
```

## Components

### Categoria Routes
- **Location**: `backend/categorias/routes/categorias.py`
- **Endpoints**:

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/categorias | Público | Árbol completo de categorías |
| GET | /api/v1/categorias/{id} | Público | Detalle de categoría con subcategorías |
| POST | /api/v1/categorias | STOCK, ADMIN | Crear categoría |
| PUT | /api/v1/categorias/{id} | STOCK, ADMIN | Editar categoría (valida ciclos) |
| DELETE | /api/v1/categorias/{id} | STOCK, ADMIN | Soft delete (valida sin productos) |

### Categoria Service
- **Location**: `backend/categorias/services/categoria_service.py`
- **Key methods**:
  - `get_tree(session)` → árbol completo de categorías
  - `get_by_id(session, id)` → detalle con subcategorías
  - `create(session, data)` → crear, validar nombre único en nivel, padre existe
  - `update(session, id, data)` → editar, validar no ciclos, no self-parent
  - `delete(session, id)` → soft delete, validar sin productos activos

### Frontend — Admin
- **CategoriasPage**: Árbol visual con expandir/colapsar, botones crear/editar/eliminar
- **CreateCategoriaModal**: Formulario con nombre, descripción, selector de categoría padre
- **EditCategoriaModal**: Similar con valores pre-cargados
- **DeleteConfirmDialog**: Confirmación con verificación de productos asociados
- **useCategorias hook**: TanStack Query para CRUD

### Frontend — Público
- El endpoint GET /api/v1/categorias se usará desde el catálogo para filtrar productos

## Data Model

Usa el modelo existente `Categoria` con:
- `id`, `nombre`, `descripcion`, `imagen_url`, `padre_id` (self-referential FK)
- `subcategorias` (relationship), `productos` (relationship M2M via ProductoCategoria)
- Soft delete via `eliminado_en`

## Implementation Notes

- **Árbol**: Cargar todas las categorías con `selectinload(Categoria.subcategorias)` y construir el árbol en memoria agrupando por padre_id
- **Validación de ciclos**: El método `validate_no_cycles` en CategoriaRepository ya existe. Recorre hacia arriba desde el nuevo padre y verifica que no se encuentre a sí misma.
- **Protección de eliminación**: Verificar `count_productos > 0` antes de soft delete. Si tiene productos, rechazar con mensaje.
- **Roles**: POST/PUT/DELETE requieren STOCK o ADMIN. GET es público.
