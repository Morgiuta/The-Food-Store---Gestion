# Proposal: sprint-3-direcciones-entrega

## What & Why

**What**: Implementar el sistema de gestión de direcciones de entrega para usuarios autenticados.

**Why**: Los usuarios necesitan poder guardar, editar y gestionar múltiples direcciones de envío para sus pedidos. Una dirección debe poder marcarse como predeterminada.

**Goal**: Permitir que cada usuario pueda crear, editar, eliminar y gestionar múltiples direcciones de entrega, con una predeterminada por usuario.

## Scope

### Included
- Modelo DireccionEntrega con campos completos (calle, numero, piso, departamento, ciudad, codPostal, referencia, es_predeterminada)
- CRUD completo de direcciones (POST, GET, GET /{id}, PUT, DELETE)
- Primera dirección creada se marca como predeterminada automáticamente
- Solo una dirección predeterminada por usuario a la vez
- Validación de ownership (solo el usuario puede ver/editar sus direcciones)
- Snapshot de dirección en pedidos (copiar datos al crear pedido)
- Frontend: AddressListPage, AddressCard, AddAddressModal, EditAddressModal

### Excluded
- Cálculo de costo de envío por zona (se hace en sprint-3-checkout-preview)
- Integración con APIs de geolocalización
- Validación de direcciones con servicios externos

## Success Criteria

1. El usuario puede crear una dirección y verla en su lista
2. El usuario puede editar cualquier dirección propia
3. El usuario puede eliminar (soft delete) cualquier dirección propia
4. El usuario puede marcar una dirección como predeterminada
5. Solo una dirección está predeterminada a la vez
6. El ownership está validado en backend (403 si intenta acceder a dirección ajena)
7. Los datos de dirección se guardan como snapshot en los pedidos

## Dependencies

- sprint-1-autenticacion (get_current_user) ✅ Completado
- sprint-0-infraestructura (modelos base, repository pattern) ✅ Completado