## Context

Ya existe:
- `GET /api/v1/pedidos/admin/all` con filtro por `estado_id` y paginación
- `PATCH /api/v1/pedidos/{id}/estado` para avanzar estado
- `PATCH /api/v1/pedidos/{id}/cancelar` para cancelar
- `GET /api/v1/pedidos/{id}` para detalle
- Panel admin con layout y navegación por secciones (sidebar)
- Componentes UI compartidos: tabla, botones, modales, badges, spinner

Lo que **no existe**:
- Página de gestión de pedidos en admin (placeholder actual)
- Tabla de pedidos con filtros
- Integración de acciones de FSM en la vista admin

## Goals / Non-Goals

**Goals:**
- Crear `AdminOrdersPage` en `frontend/src/pages/admin/orders-page.tsx`
- Tabla de pedidos paginada con columnas: ID, usuario, fecha, estado, total, acciones
- Filtros: por estado (dropdown), por rango de fechas
- Botón "Ver detalle" que abre el `OrderDetailModal`
- Botón "Avanzar estado" que abre `ChangeStatusModal`
- Botón "Cancelar" que abre `CancelOrderModal`
- Reemplazar el placeholder en `/admin/pedidos`
- Registrar lazy import en router

**Non-Goals:**
- Dashboard con métricas (será Sprint 6)
- Búsqueda avanzada con texto libre (será Sprint 7)
- Exportación de datos (fuera de alcance)

## Decisions

### 1. Reutilizar componentes FSM existentes
**Decisión**: Los modales `OrderDetailModal`, `ChangeStatusModal` y `CancelOrderModal` ya existen. Se reutilizan en la vista admin.

**Rationale**: Evita duplicación. Los modales ya manejan toda la lógica de FSM, permisos y estados.

### 2. Tabla con filtros inline
**Decisión**: Filtros en la parte superior de la página (estado, fechas) que actualizan la query de TanStack Query.

**Rationale**: Patrón ya usado en otras secciones admin (usuarios, productos). Mantiene consistencia.

### 3. Integración con router admin existente
**Decisión**: La ruta `/admin/pedidos` ya existe con un placeholder. Solo reemplazar el placeholder con el componente real.

## Frontend Components

### AdminOrdersPage
```
frontend/src/pages/admin/orders-page.tsx
```
- Tabla con columnas: ID, Usuario, Fecha, Estado, Total, Acciones
- Filtros: estado (dropdown), fecha_desde, fecha_hasta (date inputs)
- Paginación integrada
- Acciones: Ver detalle, Avanzar estado, Cancelar

### Hooks
- `usePedidosAdmin(page, size, estadoId, fechaDesde, fechaHasta)` — query de TanStack Query
  (ya creado en Change 1, se actualiza para soportar filtros de fecha)

## API Usage

### `GET /api/v1/pedidos/admin/all`
**Params**: `page`, `size`, `estado_id`, `fecha_desde`, `fecha_hasta`

Actualmente el endpoint ya soporta `estado_id`. Se agregan `fecha_desde` y `fecha_hasta` al backend.

### `PATCH /api/v1/pedidos/{id}/estado`
Ya implementado en Change 2.

### `PATCH /api/v1/pedidos/{id}/cancelar`
Ya implementado en Change 2.

## Backend Changes

### Modificar `PedidoService.listar_admin()`
Agregar soporte para filtros `fecha_desde` y `fecha_hasta` (datetime opcionales).

### Modificar endpoint `GET /api/v1/pedidos/admin/all`
Agregar query params `fecha_desde` y `fecha_hasta`.

## Risks / Mitigations

| Risk | Mitigation |
|------|------------|
| Performance con muchos pedidos | Paginación obligatoria (20 por defecto, máx 100) |
| Usuario PEDIDOS ve datos sensibles de usuarios | El endpoint ya filtra por roles (PEDIDOS no ve datos financieros) |
| Doble clic en avanzar/cancelar | Las mutations de TanStack Query ya manejan estado isPending |
