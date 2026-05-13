# Tasks: sprint-4-creacion-pedidos

## 1. Backend — Pedido Service

- [x] 1.1 Crear `backend/pedidos/services/pedido_service.py` con clase `PedidoService`
- [x] 1.2 Implementar método `crear(uow, request, usuario_id)`:
  - Validar items: productos existen, disponibles, stock suficiente con SELECT FOR UPDATE
  - Validar dirección: existe y pertenece al usuario (si se envía direccion_id)
  - Calcular subtotal = Σ(precio_snapshot × cantidad)
  - Asignar costo_envio = 500.00 (tarifa plana)
  - Calcular total = subtotal + costo_envio
  - Generar snapshot de dirección como JSON string
  - Crear Pedido con estado_id = PENDIENTE (1)
  - Crear DetallePedido por cada item con precio_snapshot y subtotal
  - Crear HistorialEstadoPedido inicial (estado_anterior_id=NULL, estado_nuevo_id=1)
  - Devolver el pedido creado con relaciones cargadas
- [x] 1.3 Implementar método `listar_mis_pedidos(uow, usuario_id, skip, limit)` con paginación
- [x] 1.4 Implementar método `obtener_detalle(uow, pedido_id, usuario_id, roles)` con validación de ownership
- [x] 1.5 Implementar método `listar_admin(uow, skip, limit, estado_id)` para ADMIN/PEDIDOS

## 2. Backend — Schemas

- [x] 2.1 Revisar y completar schemas en `backend/pedidos/schemas/pedido.py`:
  - `CrearPedidoRequest` (items: list[ItemPedidoRequest], direccion_id, forma_pago_id)
  - `ItemPedidoRequest` (producto_id, cantidad, personalizacion)
  - `PedidoRead` (id, usuario_id, estado, total, costo_envio, creado_en)
  - `PedidoDetail` (PedidoRead + detalles, historial)
  - `DetallePedidoRead` (producto_id, producto_nombre, cantidad, precio_unitario, subtotal, personalizacion)
  - `HistorialEstadoRead` (estado_anterior, estado_nuevo, usuario_id, observacion, timestamp)
  - `PaginatedPedidos` (items, total, page, size, pages)

## 3. Backend — Routes

- [x] 3.1 Crear `backend/pedidos/routes/pedidos.py` con router
- [x] 3.2 Implementar endpoint `POST /api/v1/pedidos` (CLIENT) — crear pedido con UoW
- [x] 3.3 Implementar endpoint `GET /api/v1/pedidos` (CLIENT) — listar propios con paginación
- [x] 3.4 Implementar endpoint `GET /api/v1/pedidos/{id}` (CLIENT/ADMIN) — detalle
- [x] 3.5 Implementar endpoint `GET /api/v1/pedidos/admin` (ADMIN/PEDIDOS) — listar todos con filtros
- [x] 3.6 Registrar router en `backend/main.py`

## 4. Frontend — useOrders Hook

- [x] 4.1 Crear `frontend/src/features/pedidos/hooks/useOrders.ts` con:
  - `useMisPedidos(page, size)` — lista paginada de pedidos del usuario
  - `usePedidoDetail(id)` — detalle completo de un pedido
  - `useCrearPedido()` — mutation para crear pedido
- [x] 4.2 Agregar endpoints de pedidos en `frontend/src/shared/api/endpoints.ts`

## 5. Frontend — Componentes

- [x] 5.1 Crear `OrderStatusBadge` en `frontend/src/features/pedidos/components/order-status-badge.tsx`
  - Badge visual con color por estado (PENDIENTE=amarillo, CONFIRMADO=azul, EN_PREP=naranja, EN_CAMINO=celeste, ENTREGADO=verde, CANCELADO=rojo)
- [x] 5.2 Crear `OrderCard` en `frontend/src/features/pedidos/components/order-card.tsx`
  - Muestra: ID, estado (con badge), fecha, total, botón "Ver detalle"
- [x] 5.3 Crear `OrderDetailModal` en `frontend/src/features/pedidos/components/order-detail-modal.tsx`
  - Muestra: datos del pedido, lista de items, historial de estados, totales

## 6. Frontend — Páginas

- [x] 6.1 Crear `OrderListPage` en `frontend/src/pages/pedidos/order-list-page.tsx`
  - Lista paginada de pedidos usando OrderCard
  - Filtro por estado (opcional)
- [x] 6.2 Crear `OrderConfirmationPage` en `frontend/src/pages/pedidos/order-confirmation-page.tsx`
  - Pantalla de confirmación después de crear pedido
  - Muestra: número de pedido, estado, total, link a "Mis Pedidos"
- [x] 6.3 Agregar rutas en `frontend/src/app/providers/router.tsx`
  - `/mis-pedidos` → OrderListPage
  - `/pedidos/confirmacion/:id` → OrderConfirmationPage

## 7. Backend — Tests

- [x] 7.1 Crear tests unitarios para `PedidoService.crear()`:
  - Creación exitosa con items válidos
  - Error si producto no existe
  - Error si producto no disponible
  - Error si stock insuficiente
  - Error si dirección no pertenece al usuario
- [x] 7.2 Crear tests de integración para endpoints:
  - POST /api/v1/pedidos → 201 con pedido creado
  - POST /api/v1/pedidos → 400 si sin stock
  - GET /api/v1/pedidos → 200 con lista paginada
  - GET /api/v1/pedidos/{id} → 200 con detalle
  - GET /api/v1/pedidos/{id} → 404 si no existe
  - GET /api/v1/pedidos/admin → 200 para ADMIN
  - GET /api/v1/pedidos/admin → 403 para CLIENT

## 8. Frontend — Tests

- [x] 8.1 Crear tests para useOrders hook
- [x] 8.2 Crear tests para OrderListPage (renderizado, paginación)
- [x] 8.3 Crear tests para OrderConfirmationPage
