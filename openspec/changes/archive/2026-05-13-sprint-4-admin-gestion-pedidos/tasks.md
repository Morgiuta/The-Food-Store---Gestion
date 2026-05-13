# Tasks: sprint-4-admin-gestion-pedidos

## 1. Backend — Mejora de filtros en listado admin

- [x] 1.1 Agregar parámetros `fecha_desde` y `fecha_hasta` a `PedidoService.listar_admin()`
- [x] 1.2 Agregar query params `fecha_desde` y `fecha_hasta` al endpoint `GET /api/v1/pedidos/admin/all`
- [x] 1.3 Verificar que los filtros combinados (estado + fechas) funcionan correctamente

## 2. Frontend — AdminOrdersPage

- [x] 2.1 Crear `frontend/src/pages/admin/orders-page.tsx` con:
  - Tabla de pedidos con columnas: ID, Usuario, Fecha, Estado, Total, Acciones
  - Filtros: estado (dropdown), fecha_desde/fecha_hasta (date inputs)
  - Paginación (Anterior/Siguiente + info de página)
  - Badge de estado en cada fila (reutilizar OrderStatusBadge)
  - Botones de acción: Ver detalle, Avanzar estado, Cancelar
- [x] 2.2 Agregar lazy import y ruta en `frontend/src/app/providers/router.tsx`
  - Reemplazar placeholder de `/admin/pedidos` con `AdminOrdersPage`
- [x] 2.3 Actualizar `usePedidosAdmin` hook para soportar filtros de fecha

## 3. Frontend — Tests

- [x] 3.1 Verificar compilación TypeScript sin errores nuevos
