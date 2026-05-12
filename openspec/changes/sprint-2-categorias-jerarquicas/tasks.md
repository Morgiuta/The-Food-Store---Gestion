# Tasks: Sprint 2 — Categorías Jerárquicas

## Phase 1: Backend — Categoria Service

- [ ] 1.1 Create `backend/categorias/services/__init__.py`
- [ ] 1.2 Create `backend/categorias/services/categoria_service.py`:
  - `get_tree(session)` — árbol completo con selectinload
  - `get_by_id(session, id)` — detalle con subcategorías
  - `create(session, data)` — validar nombre único, padre existe, guardar
  - `update(session, id, data)` — validar no ciclos, no self-parent
  - `delete(session, id)` — validar sin productos, soft delete

## Phase 2: Backend — Categoria Routes

- [ ] 2.1 Create `backend/categorias/routes/categorias.py`:
  - `GET /api/v1/categorias` — árbol público
  - `GET /api/v1/categorias/{id}` — detalle público
  - `POST /api/v1/categorias` — crear (STOCK, ADMIN)
  - `PUT /api/v1/categorias/{id}` — editar (STOCK, ADMIN)
  - `DELETE /api/v1/categorias/{id}` — soft delete (STOCK, ADMIN)
- [ ] 2.2 Register categorias router in `backend/main.py`

## Phase 3: Backend — Tests

- [ ] 3.1 Create `backend/tests/test_categorias.py`:
  - Test crear categoría raíz
  - Test crear subcategoría
  - Test crear con nombre duplicado → 409
  - Test obtener árbol devuelve jerarquía
  - Test editar categoría
  - Test editar con ciclo → 409
  - Test eliminar sin productos → 204
  - Test eliminar con productos → 409
  - Test GET público sin auth

## Phase 4: Frontend — Admin Categorías

- [ ] 4.1 Create `frontend/src/pages/admin/categorias-page.tsx`:
  - Árbol visual de categorías con expandir/colapsar
  - Botones de crear, editar, eliminar por nodo
  - Indicador visual de subcategorías
- [ ] 4.2 Create `frontend/src/features/categorias/components/categoria-modal.tsx`:
  - Formulario: nombre, descripción, selector de categoría padre (desplegable jerárquico)
- [ ] 4.3 Create `frontend/src/features/categorias/hooks/use-categorias.ts`:
  - useCategoriasQuery, useCreateCategoria, useUpdateCategoria, useDeleteCategoria
- [ ] 4.4 Add `/admin/categorias` route in router.tsx

## Phase 5: Integration & Final Checks

- [ ] 5.1 Run all tests: `pytest backend/tests/ -v`
- [ ] 5.2 Run frontend tests: `npm test`
- [ ] 5.3 Verify TypeScript: `npx tsc --noEmit`
- [ ] 5.4 Mark all tasks as completed
