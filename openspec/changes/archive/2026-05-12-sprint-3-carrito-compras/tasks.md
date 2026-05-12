# Tasks: sprint-3-carrito-compras

## Cart Store Enhancement

### Existing (already implemented)
- [x] cart-store.ts con persistencia en localStorage
- [x] Métodos: addItem, removeItem, updateQuantity, clearCart, getTotalPrice

### Enhancement Needed
- [x] 1. Actualizar tipo `CartItem` en `frontend/src/shared/types/index.ts` para incluir `ingredientesExcluidos: number[]`
- [x] 2. Actualizar cart-store.ts para soportar personalizacion con ingredientesExcluidos
- [x] 3. Agregar método en cart-store para verificar si ingrediente puede excluirse

## Components

- [x] 4. Crear `QuantityControl` en `frontend/src/features/carrito/components/quantity-control.tsx`
- [x] 5. Crear `CartItemComponent` en `frontend/src/features/carrito/components/cart-item.tsx'
- [x] 6. Crear `CartSummary` en `frontend/src/features/carrito/components/cart-summary.tsx'
- [x] 7. Crear `ProductPersonalizationModal` en `frontend/src/features/carrito/components/product-personalization-modal.tsx'

## Pages

- [x] 8. Crear `ShoppingCartPage` en `frontend/src/pages/carrito/shopping-cart-page.tsx'
- [x] 9. Actualizar router para incluir ruta `/carrito` → ShoppingCartPage

## Integration

- [x] 10. Buscar ProductDetailModal en `frontend/src/pages/productos/` 
- [x] 11. Agregar `AddToCartButton` que abra PersonalizationModal si el producto tiene ingredientes
- [x] 12. Si el producto NO tiene ingredientes → agregar directamente al carrito
- [x] 13. Si tiene ingredientes → abrir modal, luego agregar

## Hooks

- [x] 14. Crear `useCart` hook wrapper en `frontend/src/features/carrito/hooks/use-cart.ts'

## Navigation

- [x] 15. Verificar que `/carrito` esté en el router
- [x] 16. Verificar que la navegación del header linkee a `/carrito`

## Testing

- [x] 17. Test: persistencia sobrevive refresh del navegador (QA manual)
- [x] 18. Test: persistencia sobrevive logout/login (QA manual)
- [x] 19. Test: excluir ingrediente que NO está en producto → no permitido (QA manual)
- [x] 20. Test: misma cantidad + diferente personalización → items separados (QA manual)

## Total: 20 tasks (20 completadas) - Tests son QA manual/client-side