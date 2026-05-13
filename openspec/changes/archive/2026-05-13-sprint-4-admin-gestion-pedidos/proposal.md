## Why

Ya existe la máquina de estados para pedidos (transiciones y cancelación), pero **no hay una interfaz administrativa** para que el Gestor de Pedidos y el Admin puedan gestionar los pedidos de forma eficiente. Actualmente solo hay un placeholder "Pedidos — próximamente" en el panel admin. Sin esta interfaz, los roles PEDIDOS y ADMIN no pueden operar el sistema.

## What Changes

- Completar la sección de pedidos en el panel de administración
- Tabla de pedidos con filtros por estado, rango de fechas y búsqueda
- Capacidad de avanzar estado desde la tabla (usando el endpoint PATCH existente)
- Capacidad de cancelar pedidos desde la tabla (usando el endpoint PATCH existente)
- Panel responsive con diseño consistente con el resto del admin

## Capabilities

### New Capabilities
- `admin-gestion-pedidos`: Panel administrativo para gestionar pedidos: listado paginado con filtros (estado, fechas), cambio de estado y cancelación con permisos por rol.

### Modified Capabilities
- *(ninguna — nueva funcionalidad de UI admin)*

## Impact

- **Frontend**: Nueva página `AdminOrdersPage` con tabla, filtros y acciones. Reemplaza el placeholder en `/admin/pedidos`.
- **Backend**: El endpoint `GET /api/v1/pedidos/admin/all` ya existe del Change 1. Los endpoints PATCH de estado y cancelación ya existen del Change 2. No se requieren cambios backend nuevos.
- **Dependencias**: Depende de `sprint-4-creacion-pedidos` y `sprint-4-fsm-pedidos` (ambos ya archivados).
