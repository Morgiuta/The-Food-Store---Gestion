# Tasks: Sprint 1 — Seguridad Avanzada

## Phase 1: Backend — Rate Limiting

- [ ] 1.1 Update `backend/auth/routes/auth.py`: cambiar register rate limit de `10/minute` a `3/hour`
- [ ] 1.2 Add rate limit config to `backend/core/config.py`: `RATE_LIMIT_REGISTER`, `RATE_LIMIT_PEDIDOS`
- [ ] 1.3 Add rate limiting headers middleware (Retry-After, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)

## Phase 2: Backend — Segregación de Roles

- [ ] 2.1 Create permission map in `backend/core/permissions.py` with explicit endpoint → roles mapping
- [ ] 2.2 Verify all existing endpoints have correct role guards (require_role)
- [ ] 2.3 Update `backend/main.py` to apply rate limits globally

## Phase 3: Frontend — Navegación por Rol

- [ ] 3.1 Update `frontend/src/app/layouts/main-layout.tsx`:
  - Create navigation items array with role requirements
  - Render items based on `useAuth().hasRole()` or `isAuthenticated`
  - Show different menus for: no auth, CLIENT, STOCK, PEDIDOS, ADMIN
- [ ] 3.2 Update `frontend/src/app/layouts/admin-layout.tsx` with full admin sidebar navigation

## Phase 4: Frontend — Páginas de Error

- [ ] 4.1 Complete `frontend/src/pages/dashboard/not-found-page.tsx` with design + navigation
- [ ] 4.2 Complete `frontend/src/pages/dashboard/forbidden-page.tsx` with design + navigation
- [ ] 4.3 Create `frontend/src/pages/dashboard/unauthorized-page.tsx` (401) with design + login button
- [ ] 4.4 Add /401 route to `router.tsx`

## Phase 5: Frontend — Notificaciones

- [ ] 5.1 Update `frontend/src/app/store/ui-store.ts` if needed
- [ ] 5.2 Add global notification display component in `App.tsx` or layout
- [ ] 5.3 Update Axios interceptor to show notification on 401/403

## Phase 6: Integration & Final Checks

- [ ] 6.1 Run all tests: `pytest backend/tests/ -v`
- [ ] 6.2 Run frontend tests: `npm test`
- [ ] 6.3 Verify TypeScript: `npx tsc --noEmit`
- [ ] 6.4 Mark all tasks as completed
