# Tasks: Sprint 2 — Categorías Jerárquicas

## Phase 1: Backend — Categoria Service

- [x] 1.1 Create `backend/categorias/services/__init__.py`
- [x] 1.2 Create `backend/categorias/services/categoria_service.py` with get_tree, get_by_id, create, update, delete

## Phase 2: Backend — Categoria Routes

- [x] 2.1 Create `backend/categorias/routes/categorias.py` with 5 endpoints (GET tree, GET detail, POST, PUT, DELETE)
- [x] 2.2 Register categorias router in `backend/main.py`

## Phase 3: Backend — Tests

- [x] 3.1 Create `backend/tests/test_categorias.py` — 12 tests (CRUD, jerarquía, ciclos, auth, productos)

## Phase 4: Frontend — Admin Categorías

- [x] 4.1 Create `frontend/src/pages/admin/categorias-page.tsx` with árbol visual expand/colapsar
- [x] 4.2 Create `frontend/src/features/categorias/components/categoria-modal.tsx` con nombre, descripción, selector padre
- [x] 4.3 Create `frontend/src/features/categorias/hooks/use-categorias.ts` con TanStack Query hooks
- [x] 4.4 Add `/admin/categorias` route in router.tsx

## Phase 5: Integration & Final Checks

- [x] 5.1 All backend tests: 132 passed, 0 failed
- [x] 5.2 Frontend tests: 7 passed
- [x] 5.3 TypeScript: tsc --noEmit exit 0
- [x] 5.4 All tasks completed
