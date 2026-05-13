## Context

Ya existe:
- Modelo `Pago` con campos: pedido_id, monto, mp_payment_id, mp_status, external_reference, idempotency_key
- `PagoRepository` con métodos: get_by_pedido, get_by_preference, get_by_idempotency_key, list_by_status
- `FormaPago` catálogo con seed data
- Esquemas `PagoCreate`, `PagoRead`, `CrearPreferenciaResponse`
- `PedidoFsmService.avanzar_estado()` para transiciones de estado
- `UnitOfWork` para operaciones atómicas

Lo que **no existe**:
- `PagoService` con lógica de integración MercadoPago
- Endpoints de pagos (crear preferencia, webhook, consultar)
- Frontend con SDK de MercadoPago.js

## Goals / Non-Goals

**Goals:**
- Crear preferencia de pago en MercadoPago (`POST /api/v1/pagos/crear`)
- Registrar el pago en la tabla `Pago` con idempotency_key
- Procesar webhook IPN de MercadoPago (`POST /api/v1/pagos/webhook`)
- Transición automática PENDIENTE→CONFIRMADO cuando pago es approved
- Consultar estado de pago (`GET /api/v1/pedidos/{id}/pago`)
- Frontend: formulario de pago con SDK MercadoPago.js
- Frontend: PaymentStatusModal con estado del pago
- Frontend: botón reintentar para pagos rechazados

**Non-Goals:**
- Reembolsos (será en sprint-5-pagos-admin)
- Panel admin de pagos (será en sprint-5-pagos-admin)
- Múltiples formas de pago configurables (ya existe catálogo)

## Decisions

### 1. MercadoPago Checkout API con tokenización browser-side
**Decisión**: Usar MercadoPago Checkout API (Orders). El frontend tokeniza la tarjeta con `@mercadopago/sdk-react` y envía el `card_token` al backend para crear el pago.

**Rationale**: PCI SAQ-A compliance. Los datos de tarjeta nunca pasan por nuestro servidor. El SDK de MercadoPago.js maneja la tokenización.

### 2. Idempotency key por intento de pago
**Decisión**: Generar UUID como idempotency_key en cada intento de pago. Almacenar en la tabla `Pago` con constraint UNIQUE.

**Rationale**: RN-PA02. Si el webhook se recibe duplicado, la key unique evita doble procesamiento.

### 3. Webhook con respuesta 200 inmediata
**Decisión**: El webhook responde HTTP 200 inmediatamente. El procesamiento ocurre dentro de la misma request (síncrono pero rápido, solo consultas a BD y API de MP).

**Rationale**: RN-PA03. MercadoPago espera respuesta 200 rápido. Si falla, MP reintenta.

### 4. Verificación de estado contra API de MP
**Decisión**: Al recibir webhook, verificar el estado real del pago consultando la API de MercadoPago antes de actualizar el pedido.

**Rationale**: RN-PA04. No confiar ciegamente en los datos del webhook.

### 5. External reference = pedido_id como string
**Decisión**: Usar `str(pedido_id)` como external_reference al crear la preferencia.

**Rationale**: RN-PA09. Es la clave para vincular el webhook de MP con nuestro pedido.

## Data Model

No se modifican los modelos existentes. Se reutiliza el modelo `Pago`:

| Campo | Tipo | Nota |
|-------|------|------|
| pedido_id | Integer FK | Pedido asociado |
| monto | Numeric(10,2) | Total del pedido |
| mp_payment_id | String | ID devuelto por MP (nullable hasta confirmación) |
| mp_status | String | pending / approved / rejected / in_process / cancelled |
| external_reference | String | pedido_id como string para vincular webhook |
| idempotency_key | String UUID | Unique, evita duplicados |

## API Changes

### `POST /api/v1/pagos/crear` (CLIENT)
- **Request body**: `CrearPagoRequest` (pedido_id: int)
- **Response**: `201 CrearPreferenciaResponse` (preference_id, init_point, id)
- **Lógica**:
  1. Validar pedido existe, está en PENDIENTE, pertenece al usuario
  2. Generar idempotency_key (UUID)
  3. Crear preferencia en MercadoPago via Orders API
  4. Registrar Pago en BD con mp_status = "pending"
  5. Devolver preference_id + init_point

### `POST /api/v1/pagos/webhook` (Público — validar firma)
- **Request body**: Notificación IPN de MercadoPago
- **Response**: `200 OK`
- **Lógica**:
  1. Validar firma del webhook
  2. Extraer payment_id y external_reference
  3. Consultar estado real en API de MP
  4. Buscar pago por external_reference
  5. Actualizar mp_payment_id y mp_status
  6. Si approved: transicionar pedido a CONFIRMADO via FSM service
  7. Si rejected/pending/in_process: solo actualizar estado del pago

### `GET /api/v1/pedidos/{id}/pago` (Propietario/ADMIN)
- **Response**: `200 PagoRead` (último pago del pedido)

## Frontend Components

```
frontend/src/features/pagos/
├── hooks/
│   └── usePago.ts          ← crear pago, consultar estado
├── components/
│   ├── payment-form.tsx     ← Formulario embebido con SDK MP
│   ├── payment-status-modal.tsx  ← Modal con estado del pago
│   └── retry-payment-button.tsx  ← Botón reintentar si rechazado
```

## Risks / Mitigations

| Risk | Mitigation |
|------|------------|
| Webhook duplicado de MP | Idempotency key UNIQUE en tabla Pago |
| Webhook con datos falsificados | Validación de firma + verificación contra API de MP |
| Pago aprobado pero webhook no llega | Consulta periódica de estado desde frontend (polling) |
| Token de MP expirado | El SDK de MP maneja renovación automática |
| Cliente cierra browser antes de confirmar | El webhook eventualmente notificará el estado real |
