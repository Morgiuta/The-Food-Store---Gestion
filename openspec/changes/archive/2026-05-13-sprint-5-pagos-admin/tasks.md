# Tasks: sprint-5-pagos-admin

## 1. Backend — Admin Pago Repository

- [x] 1.1 Agregar `list_by_date_range` en `PagoRepository`
- [x] 1.2 Agregar `count_by_status` en `PagoRepository`

## 2. Backend — Admin Pago Service

- [x] 2.1 Crear `backend/admin/services/admin_pago_service.py` con clase `AdminPagoService`
- [x] 2.2 Implementar `listar_pagos(uow, page, size, mp_status, fecha_desde, fecha_hasta)`
- [x] 2.3 Implementar `obtener_detalle(uow, pago_id)`
- [x] 2.4 Implementar `reembolsar(uow, pago_id, motivo)`:
  - Validar pago existe y está "approved"
  - Llamar a API de MP para reembolsar
  - Actualizar mp_status a "refunded"
  - Registrar en historial del pedido

## 3. Backend — Admin Pago Routes

- [x] 3.1 Crear `backend/admin/routes/pagos.py` con endpoints
- [x] 3.2 Registrar router en `backend/main.py`

## 4. Frontend — Admin Pago Page

- [x] 4.1 Crear `frontend/src/pages/admin/pagos-page.tsx` con tabla, filtros
- [x] 4.2 Crear `PaymentDetailModal` en `frontend/src/features/pagos/components/payment-detail-modal.tsx`
- [x] 4.3 Crear `RefundModal` en `frontend/src/features/pagos/components/refund-modal.tsx`
- [x] 4.4 Agregar ruta en router admin
- [x] 4.5 Agregar `API_ENDPOINTS` de admin pagos

## 5. Backend — Tests

- [x] 5.1 Verificar tests existentes pasan
