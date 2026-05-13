# Tasks: sprint-6-admin-configuracion

## 1. Backend — Modelo Configuracion

- [x] 1.1 Crear `backend/admin/models/configuracion.py` con modelo `Configuracion`
- [x] 1.2 Crear `backend/admin/repositories/configuracion.py` con `ConfiguracionRepository`

## 2. Backend — Service

- [x] 2.1 Crear `backend/admin/services/admin_config_service.py` con `AdminConfigService`
- [x] 2.2 Implementar `get_config(uow)` — obtener todas las configuraciones
- [x] 2.3 Implementar `update_config(uow, configs: list[dict])` — upsert configuraciones
- [x] 2.4 Implementar `get_formas_pago(uow)` — listar formas de pago
- [x] 2.5 Implementar `toggle_forma_pago(uow, id, activo)` — habilitar/deshabilitar

## 3. Backend — Schemas + Routes

- [x] 3.1 Crear schemas en `backend/admin/schemas/config.py`
- [x] 3.2 Crear `backend/admin/routes/config.py` con endpoints
- [x] 3.3 Registrar router en `backend/main.py`

## 4. Frontend — AdminConfigPage

- [x] 4.1 Crear hook `useAdminConfig` en `frontend/src/features/admin/hooks/useAdminConfig.ts`
- [x] 4.2 Agregar endpoints en `frontend/src/shared/api/endpoints.ts`
- [x] 4.3 Crear `frontend/src/pages/admin/config-page.tsx` con formularios
- [x] 4.4 Agregar ruta en router admin

## 5. Verify

- [x] 5.1 Verificar tests backend pasan
- [x] 5.2 Verificar frontend compila sin errores
