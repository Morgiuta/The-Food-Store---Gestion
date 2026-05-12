# Tasks: sprint-3-direcciones-entrega

## Backend Tasks

### Model & Repository
- [x] 1. Crear modelo `DireccionEntrega` en `backend/direcciones/models/direccion.py` (ya existía en auth/models)
- [x] 2. Crear `DireccionRepository` en `backend/direcciones/repositories/direccion_repository.py` con métodos: get_by_user, get_by_id, create, update, soft_delete, set_predeterminada, get_predeterminada
- [x] 3. Crear schema Pydantic `DireccionCreate`, `DireccionUpdate`, `DireccionResponse` en `backend/direcciones/schemas/direccion.py`

### Service Layer
- [x] 4. Crear `DireccionService` en `backend/direcciones/services/direccion_service.py` con lógica de:
  - create (primera dirección = predeterminada)
  - update
  - delete (si era predeterminada, despejar)
  - set_predeterminada (transactional)
  - list_by_user (ordenar predeterminada primero)
- [x] 5. Implementar validación de ownership

### Routes
- [x] 6. Crear router en `backend/direcciones/routes/direcciones.py` con endpoints:
  - POST / — crear
  - GET / — listar del usuario
  - GET /{id} — obtener una
  - PUT /{id} — editar
  - DELETE /{id} — soft delete
  - POST /{id}/predeterminada — marcar predeterminada
- [x] 7. Registrar router en `backend/main.py`
- [x] 8. Proteger todos los endpoints con `get_current_user`

### Testing
- [x] 9. Crear tests de repository en `backend/tests/test_direcciones_repository.py` (5 tests ✅)
- [x] 10. Crear tests de service en `backend/tests/test_direcciones_service.py` (5 tests ✅)
- [x] 11. Crear tests de integración en `backend/tests/test_direcciones_api.py` (creado, necesita más setup)

## Frontend Tasks

### API Layer
- [x] 12. Agregar endpoints en `frontend/src/shared/api/endpoints.ts`

### Hooks
- [x] 13. Crear `useDirecciones` hook en `frontend/src/features/direcciones/hooks/use-direcciones.ts`:
  - useDirecciones() — listar
  - useCreateDireccion() — crear
  - useUpdateDireccion() — editar
  - useDeleteDireccion() — eliminar
  - useSetPredeterminada() — marcar predeterminada
  - Invalidar queries apropiadamente

### Components
- [x] 14. Crear `AddressCard` en `frontend/src/features/direcciones/components/address-card.tsx`
- [x] 15. Crear `AddressForm` en `frontend/src/features/direcciones/components/address-form.tsx`

### Pages
- [x] 16. Crear `DireccionesPage` en `frontend/src/features/direcciones/pages/direcciones-page.tsx`
- [x] 17. El modal de edición está integrado en DireccionesPage
- [x] 18. Agregar rutas en `frontend/src/app/providers/router.tsx`

### Integration
- [x] 19. Agregar enlace en navegación hacia "Mis Direcciones"
- [x] 20. Verificar que no haya errores de TypeScript

## Total: 20 tasks (19 completadas, 1 con setup pendiente)