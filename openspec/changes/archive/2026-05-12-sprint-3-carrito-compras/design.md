# Design: sprint-3-carrito-compras

## Architecture

### Existing Cart Store (already implemented)

El cart store ya existe en `frontend/src/app/store/cart-store.ts` con:
- Persistencia en localStorage (name: 'cart-store')
- Métodos: addItem, removeItem, updateQuantity, clearCart, getTotalPrice, totalItems, totalPrice

**Current limitation**: `personalizacion` es solo un string, no permite excluir ingredientes específicos.

### What's Needed

**1. Enhanced CartStore**
```
frontend/src/app/store/cart-store.ts
```
Actualizar para soportar:
- `personalizacion` como objeto con `ingredientesExcluidos: number[]`
- Método para verificar si un ingrediente puede excluirse

**2. Shopping Cart Page**
```
frontend/src/pages/carrito/shopping-cart-page.tsx
```
- Lista de CartItem
- Resumen de totals
- Botón checkout

**3. Components**
```
frontend/src/features/carrito/
├── components/
│   ├── cart-item.tsx
│   ├── quantity-control.tsx
│   ├── cart-summary.tsx
│   └── product-personalization-modal.tsx
├── hooks/
│   └── use-cart.ts
└── pages/
    └── shopping-cart-page.tsx
```

**4. Integration with Product Detail**
- Agregar AddToCartButton en ProductDetailModal existente
- Abrir ProductPersonalizationModal si el producto tiene ingredientes

## Data Structures

### Enhanced CartItem (TypeScript)
```typescript
interface CartItem {
  producto: Product;
  cantidad: number;
  personalizacion: {
    ingredientesExcluidos: number[]; // IDs de ingredientes
  } | null;
}
```

### Personalization Modal Flow
1. User hace click en "Agregar al carrito"
2. Si el producto tiene ingredientes → mostrar ProductPersonalizationModal
3. Modal muestra lista de ingredientes del producto con checkboxes
4. User selecciona/deselecciona ingredientes a excluir
5. Al confirmar → agregar al carrito con personalización

## Storage

- **localStorage**: 'cart-store' (ya configurado)
- **Persist behavior**: survive refresh, survive logout
- **No backend required**: es client-side

## Edge Cases

1. **Producto sin ingredientes** → agregar directamente sin modal
2. **Cantidad = 0** → eliminar item
3. **Carrito vacío** → mostrar empty state
4. **Ingredient excluido no existe en producto** → validar y no permitir
5. **Mismo producto con diferente personalización** → treat as separate items

## Component Specs

### QuantityControl
- Botón "-" para decrementar (remove if 1→0)
- Input number para seteo directo
- Botón "+" para incrementar
- Validar cantidad mínima 1

### CartItem
- Imagen del producto (thumbnail)
- Nombre del producto
- Precio unitario
- Personalización (ingredientes excluidos como tags)
- QuantityControl
- Remove button
- Subtotal (precio × cantidad)

### CartSummary
- Total de items
- Subtotal
- Botón "Ir al checkout" (disabled if empty)

### ProductPersonalizationModal
- Lista de ingredientes del producto
- Checkbox para cada ingrediente
- Info: "Los ingredientes seleccionados serán excluidos"
- Confirmar / Cancelar buttons

## Testing Strategy

- Unit tests: cart store actions
- Integration: persist survived refresh, logout
- Component tests: modal interactions