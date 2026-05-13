# Tasks: sprint-7-historial-cambios-auditar

## 1. Backend — Modelo y Repositorio

- [x] 1.1 Crear `backend/admin/models/audit_log.py` con modelo `AuditLog`
- [x] 1.2 Crear `backend/admin/repositories/audit_log.py` con `AuditLogRepository`
- [x] 1.3 Agregar repositorio al UoW

## 2. Backend — Service y Routes

- [x] 2.1 Crear `backend/admin/services/audit_service.py` con `AuditService`
- [x] 2.2 Crear schemas en `backend/admin/schemas/audit.py`
- [x] 2.3 Crear `backend/admin/routes/audit.py` con endpoint GET /admin/audit
- [x] 2.4 Registrar router en `backend/main.py`

## 3. Backend — Integración

- [x] 3.1 Integrar audit logging en servicios existentes (usuarios, productos, pedidos)

## 4. Frontend — AdminAuditPage

- [x] 4.1 Crear hook `useAuditLog` en frontend
- [x] 4.2 Crear `frontend/src/pages/admin/audit-page.tsx`
- [x] 4.3 Agregar endpoints y ruta

## 5. Verify

- [x] 5.1 Verificar tests pasan
- [x] 5.2 Verificar frontend compila
