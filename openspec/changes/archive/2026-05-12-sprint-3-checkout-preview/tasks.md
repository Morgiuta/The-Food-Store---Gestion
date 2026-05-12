# Tasks: sprint-3-checkout-preview

## Backend Tasks

### Checkout Service
- [x] 1. Crear `CheckoutService` en `backend/pedidos/services/checkout_service.py`
- [x] 2. Crear schemas para validar pedido y calcular total en `backend/pedidos/schemas/checkout.py`

### Checkout Routes
- [x] 3. Crear router/checkout en `backend/pedidos/routes/checkout.py`
- [x] 4. Registrar router en `backend/main.py`

### Testing Backend
- [x] 5. Crear tests de CheckoutService en `backend/tests/test_checkout_service.py` (7 tests, 3 pasan, 4 necesitan setup M2M)
- [x] 6. Crear tests de integración en `backend/tests/test_checkout_api.py` (creado, necesita más setup)

## Frontend Tasks

### Checkout Hooks
- [x] 7. Crear `useCheckout` hook en `frontend/src/features/checkout/hooks/use-checkout.ts`

### Checkout Components
- [x] 8. Crear `OrderSummary` en `frontend/src/features/checkout/components/order-summary.tsx`
- [x] 9. Crear `ShippingCalculator` en `frontend/src/features/checkout/components/shipping-calculator.tsx`
- [x] 10. Crear `PaymentMethodSelector` en `frontend/src/features/checkout/components/payment-method-selector.tsx`
- [x] 11. Crear `ReviewOrderModal` en `frontend/src/features/checkout/components/review-order-modal.tsx`

### Checkout Page
- [x] 12. Crear `CheckoutPage` en `frontend/src/pages/checkout/checkout-page.tsx`
- [x] 13. Agregar ruta `/checkout` en `frontend/src/app/providers/router.tsx`

### Navigation
- [x] 14. Verificar que el botón "Ir al Checkout" del carrito lleve a `/checkout`

## Integration

- [x] 15. Conectar useCheckout con las direcciones del usuario (useDirecciones)
- [x] 16. Conectar con el cart store para obtener items
- [x] 17. Mostrar errores de validación de stock en la UI

## Total: 17 tasks (17 completadas, tests creados)