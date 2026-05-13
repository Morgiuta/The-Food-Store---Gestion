## Context

Ya existe:
- `PagoService` con métodos para crear preferencia, procesar webhook y consultar estado
- `PagoRepository` con: get_by_pedido, get_by_preference, get_by_idempotency_key, list_by_status
- Modelo `Pago` con pedido_id, monto, mp_payment_id, mp_status, external_reference
- Panel admin con layout y navegación por secciones
- SDK de MercadoPago (`mercadopago` package) ya instalado

## Goals / Non-Goals

**Goals:**
- Listar pagos en admin con filtros por estado y rango de fechas
- Ver detalle completo de un pago
- Reembolsar un pago aprobado vía API de MercadoPago
- Frontend: tabla de pagos, filtros, modal de detalle, modal de reembolso

**Non-Goals:**
- Editar pagos manualmente (solo reembolso vía MP)
- Exportar datos (será Sprint 7)

## Decisions

### 1. Reembolso vía API de MercadoPago
**Decisión**: Usar `sdk.payment().refund(payment_id)` de MercadoPago. Al reembolsar, actualizar mp_status a "refunded" en BD.

**Rationale**: MP maneja todo el flujo de reembolso (tiempos, medios de pago). Solo registramos el resultado.

### 2. Endpoints separados en admin
**Decisión**: Los endpoints de admin de pagos van en `backend/admin/routes/pagos.py` con dependencia `RoleRequired(["ADMIN"])`.

## API Changes

### `GET /api/v1/admin/pagos` (ADMIN)
- **Query params**: page, size, mp_status, fecha_desde, fecha_hasta
- **Response**: PaginatedResponse[PagoRead]

### `GET /api/v1/admin/pagos/{id}` (ADMIN)
- **Response**: PagoRead (con pedido info)

### `POST /api/v1/admin/pagos/{id}/reembolsar` (ADMIN)
- **Body**: { motivo: str }
- **Response**: PagoRead actualizado

## Frontend Components

```
AdminPagosPage (pages/admin/pagos-page.tsx)
├── Filtros (estado dropdown, fechas)
├── PaymentsTable (ID, pedido, monto, estado, fecha, acciones)
├── PaymentDetailModal (detalle completo)
└── RefundModal (confirmación + motivo)
```
