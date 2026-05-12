## Why

El catálogo de productos es el corazón de la tienda. Sin endpoints CRUD para productos, los gestores de stock no pueden dar de alta productos, y los clientes no pueden verlos. Este change implementa el CRUD completo de productos con asignación a categorías e ingredientes, visibilidad pública del catálogo y gestión de stock.

## What Changes

- **Backend**: CRUD de productos con M2M a categorías e ingredientes, catálogo público filtrado, stock validation
- **Frontend Admin**: Página de gestión de productos con tabla y modal CRUD
- **Frontend Público**: Catálogo de productos con filtro por categoría

## Capabilities

### New Capabilities
- `producto-crud`: CRUD de productos con relaciones M2M y catálogo público

## Impact

- **Backend**: `backend/productos/routes/productos.py`, `backend/productos/services/producto_service.py`
- **Frontend**: Página admin productos + catálogo público
- **Roles**: STOCK/ADMIN para CRUD, público para GET catálogo
