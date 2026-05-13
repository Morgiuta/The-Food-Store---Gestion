## Why

Los pedidos se crean en estado PENDIENTE pero **no pueden avanzar a CONFIRMADO** porque no hay integración con MercadoPago. Sin pagos, el flujo de compra está truncado: el usuario agrega productos al carrito, crea el pedido, pero no puede pagarlo.

## What Changes

- Integración con MercadoPago Checkout API para procesar pagos
- Endpoint `POST /api/v1/pagos/crear` para crear orden de pago (preferencia)
- Endpoint `POST /api/v1/pagos/webhook` para recibir notificaciones IPN de MercadoPago
- Endpoint `GET /api/v1/pedidos/{id}/pago` para consultar estado de pago
- Generación de idempotency_key para evitar cobros duplicados
- Procesamiento de webhook: approved → transición PENDIENTE→CONFIRMADO
- Frontend: integración con SDK de MercadoPago.js, formulario de pago embebido
- Frontend: PaymentStatusModal, botón de reintentar pago rechazado

## Capabilities

### New Capabilities
- `mercadopago-integration`: Integración completa con MercadoPago Checkout API: creación de preferencias, tokenización de tarjetas en frontend (PCI SAQ-A), webhook IPN con idempotencia, transición automática de estados de pedido según resultado del pago.

### Modified Capabilities
- *(ninguna — funcionalidad completamente nueva)*

## Impact

- **Backend**: Nuevo `PagoService` con lógica de creación de preferencias y procesamiento de webhooks. Endpoints en `pagos/routes/`. Dependencia del SDK `mercadopago` (ya listado en requirements).
- **Frontend**: Integración con `@mercadopago/sdk-react`. Nuevos componentes: `MercadoPagoButton`, `PaymentForm`, `PaymentStatusModal`, `RetryPaymentButton`.
- **Configuración**: Variables de entorno `MERCADOPAGO_ACCESS_TOKEN` y `MERCADOPAGO_PUBLIC_KEY` necesarias.
- **Dependencias**: Depende de `sprint-4-creacion-pedidos` (pedido existente para asociar pago).
