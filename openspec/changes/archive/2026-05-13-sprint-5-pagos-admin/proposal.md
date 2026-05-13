## Why

Los pagos se crean y procesan vía MercadoPago, pero **no hay una interfaz administrativa** para que el Admin pueda ver los pagos, filtrarlos por estado, ver su detalle o realizar reembolsos. Sin esto, la operación de la tienda carece de trazabilidad financiera y capacidad de gestión de pagos.

## What Changes

- Endpoint `GET /api/v1/admin/pagos` para listar pagos con filtros (admin only)
- Endpoint `GET /api/v1/admin/pagos/{id}` para detalle de pago
- Endpoint `POST /api/v1/admin/pagos/{id}/reembolsar` para reembolsar un pago aprobado
- Servicio de reembolsos que llama a API de MercadoPago y registra en BD
- Frontend: PaymentsSection en admin con tabla, filtros y detalle
- Frontend: RefundModal con confirmación

## Capabilities

### New Capabilities
- `admin-pagos-gestion`: Panel administrativo de pagos con listado, filtros (estado, fechas), detalle de pago y reembolso con integración a API de MercadoPago.

### Modified Capabilities
- *(ninguna)*

## Impact

- **Backend**: Nuevo `AdminPagoService` para consultas admin y reembolsos. Nuevo endpoint `admin/pagos` en `admin/routes/`.
- **Frontend**: Nueva página `AdminPagosPage` con tabla, filtros, modales de detalle y reembolso.
- **Dependencias**: Depende de `sprint-5-mercadopago-checkout` (servicio de MP existente).
