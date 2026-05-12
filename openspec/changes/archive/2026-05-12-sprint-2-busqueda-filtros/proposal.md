## Why

El catálogo de productos ya tiene CRUD y visualización, pero los clientes no pueden buscar productos por texto ni filtrar por precio o alérgenos. Sin búsqueda, la navegación del catálogo es limitada.

## What Changes

- **Backend**: Endpoint de búsqueda full-text en productos con filtros combinados (texto, precio min/max, categoría, alérgenos)
- **Frontend**: SearchBar con filtros en el catálogo público

## Capabilities

### New Capabilities
- `product-search`: Búsqueda full-text en productos con filtros combinados

## Impact

- **Backend**: Endpoint GET /api/v1/productos/search en routes existentes
- **Frontend**: SearchBar + filtros en catalog-page.tsx
