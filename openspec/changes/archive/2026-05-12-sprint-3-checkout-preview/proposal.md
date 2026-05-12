# Proposal: sprint-3-checkout-preview

## What & Why

**What**: Implementar la vista previa del checkout antes de pagar, incluyendo validación de stock, cálculo de envío, y resumen de pedido.

**Why**: Antes de confirmar un pedido, el usuario necesita ver el resumen completo (items, subtotal, costo de envío, total), seleccionar una dirección de entrega, y validar que el stock esté disponible. Esto evita errores y mejora la experiencia de usuario.

**Goal**: Checkout page completo con validación de stock, cálculo de envío, selección de dirección, y resumen de pedido antes de crear el pedido.

## Scope

### Included
- Backend: Servicio de validación de pedido (stock suficiente, precios válidos)
- Backend: Servicio de cálculo de total (items + envío)
- Backend: Cálculo de envío (tarifa plana por ahora)
- Frontend: CheckoutPage con resumen de carrito
- Frontend: OrderSummary (items, subtotal, envío, total)
- Frontend: ShippingCalculator (seleccionar dirección, calcular costo)
- Frontend: SelectShippingAddressModal (mostrar direcciones guardadas)
- Frontend: PaymentMethodSelector (placeholder para método de pago)
- Frontend: ReviewOrderModal (revisar antes de confirmar)
- Frontend: useCheckout hook

### Excluded
- Creación del pedido en backend (se hace en sprint-4-creacion-pedidos)
- Integración con MercadoPago (se hace en sprint-5)
- Webhook de confirmación de pago
- Máquina de estados de pedidos

## Success Criteria

1. El usuario ve el resumen del pedido (items, precios, cantidades)
2. El usuario puede seleccionar una dirección de entrega guardada
3. El sistema calcula el costo de envío
4. El sistema muestra el total (subtotal + envío)
5. El sistema valida que hay stock disponible para todos los items
6. El usuario puede revisar el pedido antes de confirmar
7. Botón "Confirmar Pedido" presente (aunque la creación se hace en sprint-4)

## Dependencies

- sprint-3-carrito-compras ✅ Completado
- sprint-3-direcciones-entrega ✅ Completado
- sprint-2-catalogo-productos ✅ Completado