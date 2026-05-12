# Proposal: sprint-3-carrito-compras

## What & Why

**What**: Implementar el sistema completo de carrito de compras client-side con persistencia y personalización de productos.

**Why**: Los usuarios necesitan un carrito de compras funcional que mantenga sus items entre sesiones, permita modificar cantidades, eliminar productos, y personalizar productos (excluir ingredientes específicos).

**Goal**: Carrito de compras completo con persistencia en localStorage, gestión de items, y personalización de productos con exclusión de ingredientes.

## Scope

### Included
- Cart store con Zustand + persistencia en localStorage
- ShoppingCartPage para visualizar items
- CartItem componente con controls de cantidad
- QuantityControl, RemoveItemButton, ClearCartButton
- CartSummary con subtotal, total items, botón checkout
- AddToCartButton en ProductDetailModal
- ProductPersonalizationModal para excluir ingredientes
- useCart hook con métodos completos
- Validación: solo excluir ingredientes que el producto tenga

### Excluded
- Checkout flow (se hace en sprint-3-checkout-preview)
- Integración con backend de pedidos (se hace en sprint-4)
- Pasarela de pago (se hace en sprint-5)

## Success Criteria

1. El carrito persiste en localStorage (sobrevive refresh y logout)
2. El usuario puede agregar productos con cantidad
3. El usuario puede modificar la cantidad de cada item
4. El usuario puede eliminar items individualment
5. El usuario puede vaciar el carrito completamente
6. El usuario puede personalizar productos (excluir ingredientes)
7. Solo se pueden excluir ingredientes que el producto tenga
8. El resumen muestra subtotal y total correctamente
9. El botón de checkout redirige a la página de checkout

## Dependencies

- sprint-2-catalogo-productos (para productos en carrito) ✅ Completado
- sprint-3-direcciones-entrega (primero en ejecutarse) — en progreso