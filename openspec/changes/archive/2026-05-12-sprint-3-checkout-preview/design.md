# Design: sprint-3-checkout-preview

## Architecture

### Backend

**Dominio**: `backend/pedidos/` (ya existe)

**Servicios nuevos a crear/actualizar**:
```
backend/pedidos/services/
├── checkout_service.py   # Validación y cálculo de checkout
```

**Servicios existentes**:
- `backend/direcciones/services/direccion_service.py` — para obtener direcciones del usuario

**Modelo Pedido** (ya existe en `backend/pedidos/models/pedido.py`):
- id, usuario_id, estado_id, direccion_id
- total, costo_envio, direccion_snapshot
- creado_en, actualizado_en, eliminado_en

**Modelo DetallePedido** (ya existe):
- id, pedido_id, producto_id, cantidad, precio_snapshot, personalizacion

### Backend Service: CheckoutService

```python
class CheckoutService:
    async def validar_stock(self, session, items: list[CartItem]) -> ValidationResult:
        """Verifica stock disponible para todos los items"""
        # Por cada item: SELECT FOR UPDATE para evitar race conditions
        # Retorna: {valido: bool, errores: list[str], items_validados: list}

    async def calcular_total(
        self, items: list[CartItem], direccion_id: int
    ) -> CheckoutTotal:
        """Calcula subtotal, costo_envio, total"""
        # Tarifa plana de envío por ahora: $500
        subtotal = sum(item.producto.precio * item.cantidad for item in items)
        costo_envio = 500  # Tarifa plana
        total = subtotal + costo_envio
        return CheckoutTotal(subtotal, costo_envio, total)

    async def obtener_direcciones(self, session, usuario_id: int) -> list[Direccion]:
        """Obtiene las direcciones del usuario para seleccionar"""
```

### Frontend

**Estructura**:
```
frontend/src/features/checkout/
├── hooks/
│   └── use-checkout.ts        # Hook para validar, calcular, confirmar
├── components/
│   ├── order-summary.tsx       # Resumen de items
│   ├── shipping-calculator.tsx # Seleccionar dirección, calcular envío
│   ├── payment-method-selector.tsx # Selector de método de pago (placeholder)
│   └── review-order-modal.tsx  # Modal de revisión final
└── pages/
    └── checkout-page.tsx       # Página principal de checkout
```

## Data Flow

1. **Usuario llega a /checkout**:
   - Obtener items del cart-store
   - Obtener direcciones del usuario (API)
   - Calcular totals iniciales

2. **Usuario selecciona dirección**:
   - Mostrar lista de direcciones guardadas
   - Al seleccionar → recalcular costo de envío

3. **Usuario revisa pedido**:
   - Mostrar OrderSummary completo
   - Botón "Confirmar Pedido" → crear pedido (en sprint-4)

4. **Validación de stock**:
   - Llamar a backend para validar stock antes de mostrar checkout
   - Si stock insuficiente → mostrar error y bloquear checkout

## API Endpoints (Backend)

- `GET /api/v1/direcciones` — usado para obtener direcciones del usuario (ya existe)
- `POST /api/v1/pedidos/validar` — validar stock disponible (NUEVO)
- `POST /api/v1/pedidos/calcular-total` — calcular subtotal + envío (NUEVO)

## Frontend - CheckoutPage Layout

```
┌─────────────────────────────────────────────────────┐
│ Checkout - Resumen de tu pedido                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────┐  ┌──────────────────────┐  │
│  │ Order Summary       │  │ Shipping & Payment   │  │
│  │ - Item 1            │  │                      │  │
│  │   $10 x 2 = $20     │  │ [Seleccionar dirección]│ │
│  │ - Item 2            │  │ Costo de envío: $500  │  │
│  │   $15 x 1 = $15     │  │                      │  │
│  │                     │  │ [Método de pago]     │  │
│  │ ─────────────────── │  │ (Placeholder)        │  │
│  │ Subtotal: $35       │  │                      │  │
│  │ Envío: $500         │  │                      │  │
│  │ TOTAL: $535         │  │                      │  │
│  └─────────────────────┘  └──────────────────────┘  │
│                                                     │
│  [Revisar Pedido]  [Confirmar Pedido]              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Edge Cases

1. **Carrito vacío** → redirigir al catálogo
2. **Sin direcciones guardadas** → permitir crear nueva dirección (integrar con sprint-3)
3. **Stock insuficiente en algún item** → mostrar error, no permitir checkout
4. **Usuario no autenticado** → redirigir a login

## Testing Strategy

- Unit tests: CheckoutService.validar_stock, calcular_total
- Integration: validar stock, cálculo de total con diferentes items
- Frontend: checkout flow completo