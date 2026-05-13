# Tasks: sprint-4-fsm-pedidos

## 1. Backend — FSM Service

- [x] 1.1 Crear `backend/pedidos/services/pedido_fsm_service.py` con clase `PedidoFsmService`
- [x] 1.2 Implementar mapa de transiciones válidas como constante `TRANSICIONES_VALIDAS`
- [x] 1.3 Implementar método `validar_transicion(estado_actual_codigo, nuevo_estado_codigo)` que verifique el mapa FSM
- [x] 1.4 Implementar método `avanzar_estado(uow, pedido_id, nuevo_estado_codigo, observacion, usuario_id, roles)`:
  - Validar transición permitida en el mapa FSM
  - Si PENDIENTE→CONFIRMADO: decrementar stock atómicamente
  - Actualizar estado del pedido
  - Registrar en HistorialEstadoPedido
  - Devolver pedido actualizado con relaciones
- [x] 1.5 Implementar método `cancelar(uow, pedido_id, motivo, usuario_id, roles)`:
  - Validar que la cancelación sea posible desde el estado actual
  - Validar permisos según el estado actual
  - Si viene de CONFIRMADO: restaurar stock atómicamente
  - Actualizar estado a CANCELADO
  - Registrar en HistorialEstadoPedido con motivo obligatorio
  - Devolver pedido actualizado

## 2. Backend — Schemas

- [x] 2.1 Agregar `CancelarPedidoRequest` (motivo: str = Field(..., min_length=5)) en schemas
- [x] 2.2 Asegurar que `AvanzarEstadoRequest` tenga `nuevo_estado` y `observacion` opcional

## 3. Backend — Routes

- [x] 3.1 Agregar endpoint `PATCH /api/v1/pedidos/{id}/estado` en router de pedidos
- [x] 3.2 Agregar endpoint `PATCH /api/v1/pedidos/{id}/cancelar` en router de pedidos
- [x] 3.3 Agregar endpoint `GET /api/v1/pedidos/{id}/historial` en router de pedidos

## 4. Frontend — Componentes FSM

- [x] 4.1 Crear `OrderHistoryTimeline` en `frontend/src/features/pedidos/components/order-history-timeline.tsx`
  - Timeline visual con burbujas conectadas por líneas
  - Muestra: estado anterior → nuevo, timestamp, usuario/actor
  - Cada transición en orden cronológico ascendente
- [x] 4.2 Crear `CancelOrderModal` en `frontend/src/features/pedidos/components/cancel-order-modal.tsx`
  - Campo de motivo (textarea, obligatorio)
  - Confirmación con advertencia visual
  - Submit llama al endpoint de cancelación
- [x] 4.3 Crear `ChangeStatusModal` en `frontend/src/features/pedidos/components/change-status-modal.tsx`
  - Selector de nuevo estado (solo opciones válidas)
  - Botón "Avanzar estado"
  - Submit llama al endpoint PATCH

## 5. Frontend — Hooks

- [x] 5.1 Agregar `useAvanzarEstado()` mutation en `useOrders.ts`
- [x] 5.2 Agregar `useCancelarPedido()` mutation en `useOrders.ts`
- [x] 5.3 Agregar `useHistorialPedido(id)` query en `useOrders.ts`

## 6. Frontend — Integración en UI existente

- [x] 6.1 Actualizar `OrderDetailModal` para incluir:
  - Timeline visual de historial (usar OrderHistoryTimeline)
  - Botón "Cancelar pedido" si el estado lo permite y el usuario tiene permisos
  - Botón "Avanzar estado" si es ADMIN/PEDIDOS y hay transición válida
- [x] 6.2 Actualizar `OrderCard` para mostrar botón de cancelar si corresponde

## 7. Backend — Tests

- [x] 7.1 Tests unitarios para `PedidoFsmService`:
  - Transición válida de CONFIRMADO→EN_PREPARACION
  - Transición inválida de PENDIENTE→EN_PREPARACION (salto)
  - Transición inválida desde ENTREGADO (terminal)
  - Cancelación desde PENDIENTE (CLIENT owner)
  - Cancelación desde CONFIRMADO con restauración de stock
  - Cancelación fallida desde ENTREGADO (terminal)
  - Cancelación desde EN_PREPARACIÓN sin rol ADMIN → rechazada
- [x] 7.2 Tests de integración:
  - PATCH /pedidos/{id}/estado → 200 con estado cambiado
  - PATCH /pedidos/{id}/estado → 400 si transición inválida
  - PATCH /pedidos/{id}/cancelar → 200 con cancelación
  - PATCH /pedidos/{id}/cancelar → 400 si falta motivo
  - GET /pedidos/{id}/historial → 200 con historial cronológico
