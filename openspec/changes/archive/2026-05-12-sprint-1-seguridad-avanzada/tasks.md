# Tasks: Sprint 1 — Seguridad Avanzada

## Phase 1: Backend — Rate Limiting

- [x] 1.1 Update `backend/auth/routes/auth.py`: register rate limit de `10/minute` a `3/hour`
- [x] 1.2 Add rate limit config to `backend/core/config.py`: `RATE_LIMIT_REGISTER`, `RATE_LIMIT_LOGIN`, `RATE_LIMIT_PEDIDOS`

## Phase 2: Backend — Segregación de Roles

- [x] 2.1 Create permission map in `backend/core/permissions.py` with explicit endpoint → roles mapping
- [x] 2.2 Verify all existing endpoints have correct role guards (require_role)

## Phase 3: Frontend — Navegación por Rol

- [x] 3.1 Update `frontend/src/app/layouts/main-layout.tsx` with role-based nav (public, CLIENT, STOCK, PEDIDOS, ADMIN)
- [x] 3.2 Update `frontend/src/app/layouts/admin-layout.tsx` with full admin sidebar navigation

## Phase 4: Frontend — Páginas de Error

- [x] 4.1 Complete `frontend/src/pages/dashboard/not-found-page.tsx` (404) with design + navigation
- [x] 4.2 Complete `frontend/src/pages/dashboard/forbidden-page.tsx` (403) with design + navigation
- [x] 4.3 Create `frontend/src/pages/dashboard/unauthorized-page.tsx` (401) with design + login button
- [x] 4.4 Add /401 route to `router.tsx`

## Phase 5: Frontend — Notificaciones

- [x] 5.1 Create `frontend/src/shared/ui/notification-display.tsx` — toast component
- [x] 5.2 Add NotificationDisplay in `App.tsx` for global notifications
- [x] 5.3 Update Axios interceptor to show notification on 401/403

## Phase 6: Integration & Final Checks

- [x] 6.1 All backend tests: 120 passed, 0 failed (3 nuevos de seguridad)
- [x] 6.2 Frontend tests: 7 passed
- [x] 6.3 TypeScript: tsc --noEmit exit 0
- [x] 6.4 All tasks completed
