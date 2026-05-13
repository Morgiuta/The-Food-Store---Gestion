# Tasks: sprint-5-mercadopago-checkout

## 1. Backend — Pago Service

- [x] 1.1 Crear `backend/pagos/services/pago_service.py` con clase `PagoService`
- [x] 1.2 Implementar método `crear_preferencia(uow, pedido_id, usuario_id)`:
  - Validar pedido existe, en PENDIENTE, pertenece al usuario
  - Generar idempotency_key (UUID)
  - Obtener monto total del pedido
  - Llamar a API de MercadoPago para crear preferencia
  - Registrar Pago en BD con mp_status="pending"
  - Retornar preference_id, init_point, pago_id
- [x] 1.3 Implementar método `procesar_webhook(data)`:
  - Validar firma del webhook (X-Signature)
  - Extraer payment_id y external_reference
  - Consultar estado real en API de MP
  - Buscar pago por external_reference
  - Actualizar mp_payment_id y mp_status
  - Si approved: usar PedidoFsmService para transicionar a CONFIRMADO
  - Manejar idempotencia (verificar si ya se procesó)
- [x] 1.4 Implementar método `consultar_estado(uow, pedido_id, usuario_id, roles)`:
  - Obtener último pago del pedido
  - Validar ownership o rol admin

## 2. Backend — Schemas

- [x] 2.1 Revisar y completar schemas en `backend/pagos/schemas/pago.py`:
  - `CrearPagoRequest` (pedido_id: int)
  - `CrearPreferenciaResponse` (preference_id, init_point)
  - `PagoRead` (id, pedido_id, monto, mp_status, external_reference, creado_en)

## 3. Backend — Routes

- [x] 3.1 Crear `backend/pagos/routes/pagos.py` con router
- [x] 3.2 Implementar `POST /api/v1/pagos/crear` (CLIENT)
- [x] 3.3 Implementar `POST /api/v1/pagos/webhook` (público)
- [x] 3.4 Implementar `GET /api/v1/pedidos/{id}/pago` (propietario/ADMIN)
- [x] 3.5 Registrar router en `backend/main.py`

## 4. Frontend — usePago Hook

- [x] 4.1 Crear `frontend/src/features/pagos/hooks/usePago.ts` con:
  - `useCrearPago()` — mutation para crear preferencia
  - `useEstadoPago(pedidoId)` — query para consultar estado
- [x] 4.2 Agregar endpoints de pagos en `frontend/src/shared/api/endpoints.ts`

## 5. Frontend — Componentes

- [x] 5.1 Crear `PaymentForm` en `frontend/src/features/pagos/components/payment-form.tsx`
  - Integración con SDK MercadoPago.js
  - Formulario embebido de tarjeta (card token)
  - Botón "Pagar ahora"
  - Manejo de errores de tokenización
- [x] 5.2 Crear `PaymentStatusModal` en `frontend/src/features/pagos/components/payment-status-modal.tsx`
  - Muestra estado del pago: processing, approved, rejected
  - Iconos y colores según estado
  - Botón "Cerrar" / "Reintentar"
- [x] 5.3 Crear `RetryPaymentButton` en `frontend/src/features/pagos/components/retry-payment-button.tsx`
  - Visible solo si pedido en PENDIENTE con pago rechazado
  - Al hacer clic, crea nueva preferencia

## 6. Frontend — Integración en Checkout

- [x] 6.1 Integrar PaymentForm en la página de checkout
- [x] 6.2 Mostrar PaymentStatusModal después de crear pago
- [x] 6.3 Mostrar RetryPaymentButton si el pago fue rechazado
- [x] 6.4 Redirigir a OrderConfirmationPage cuando el pago se aprueba

## 7. Backend — Tests

- [x] 7.1 Crear tests unitarios para PagoService
- [x] 7.2 Crear tests de integración para endpoints de pagos
