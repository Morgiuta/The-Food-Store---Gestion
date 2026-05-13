# Fix Map — Correcciones Post-Exploración

## Resumen del Explore

Se realizó una exploración completa del proyecto comparando el código existente contra las especificaciones en `docs/Descripcion.txt`, `docs/Integrador.txt` (ERD v5) y `docs/Historias_de_usuario.txt`. Se identificaron **20 gaps** entre lo especificado y lo implementado.

## Clasificación

| Severidad | Cantidad | Criterio |
|-----------|----------|----------|
| 🔴 Crítico | 8 | Incumplen funcionalidad requerida, rompen reglas de negocio explícitas |
| 🟡 Moderado | 7 | Incumplen especificaciones pero no bloquean funcionalidad |
| 🟢 Menor | 5 | Convenciones, naming, cosmetica |

---

## 🔴 Critical Fixes

| ID | Problema | Localización | Síntoma | Fix aplicado |
|----|----------|--------------|---------|--------------|
| CF-01 | `GET /api/v1/auth/me` **no implementado** | `auth/routes/` no existe `me.py` | No hay forma de obtener usuario actual post-refresh. Especificado en docs (`GET /api/v1/auth/me → 200 UserResponse`) | ✅ Creado `auth/routes/me.py` |
| CF-02 | `PATCH /productos/{id}/disponibilidad` **no implementado** | `productos/routes/productos.py` | ADMIN/STOCK no puede toggle disponibilidad | ✅ Agregado endpoint |
| CF-03 | `GET/POST/DELETE /productos/{id}/ingredientes` **no implementados** | `productos/routes/productos.py` | No se pueden gestionar ingredientes de un producto | ✅ Agregados 3 endpoints |
| CF-04 | `HistorialEstadoPedido` tiene `actualizado_en` | `pedidos/models/historial_estado.py` | Viola **RN-03**: tabla append-only NO puede tener `updated_at` | ✅ Eliminado campo |
| CF-05 | `DetallePedido` no tiene `nombre_snapshot` | `pedidos/models/detalle_pedido.py` | Viola **RN-04** y **Snapshot Pattern**: el nombre del producto debe congelarse al crear el pedido | ✅ Agregado campo |
| CF-06 | `EstadoPedido` no tiene `es_terminal` | `pedidos/models/estado_pedido.py` | FSM no puede validar estados terminales a nivel modelo. Viola **RN-01** | ✅ Agregado campo |
| CF-07 | `ProductoIngrediente` no tiene `es_removible` | `productos/models/producto_ingrediente.py` | No se puede controlar qué ingredientes son removibles en personalización | ✅ Agregado campo |
| CF-08 | `RefreshToken` almacena UUID raw en vez de SHA-256 | `auth/models/refresh_token.py` | Especificación dice `token_hash CHAR(64) SHA-256` | ⏸️ Pospuesto (rompe AuthService y repositorio) |

## 🟡 Moderate Fixes

| ID | Problema | Localización | Síntoma | Fix aplicado |
|----|----------|--------------|---------|--------------|
| MF-01 | `authStore` sin `hasRole()`, persist key incorrecto, sin `partialize` | `app/store/auth-store.ts` | Docs especifican key `food-store-auth`, `partialize` solo accessToken, y selector `hasRole()` | ✅ Corregido |
| MF-02 | `BaseRepository.get_by_id()` y `list_all()` no filtran soft-delete | `core/base_repository.py` | Docs especifican `eliminado_en IS NULL` automático | ✅ Corregido |
| MF-03 | `UsuarioRol` no tiene `asignado_por_id` | `auth/models/usuario_rol.py` | No se puede trackear quién asignó el rol | ⏸️ Pospuesto |
| MF-04 | Tablas `configuraciones` y `audit_logs` no están en migración | `alembic/versions/` | Solo se crean via `Base.metadata.create_all` en lifespan | ⏸️ Pospuesto |
| MF-05 | UoW con patrón inconsistente (auth usa UoW interno, pedidos externo) | `auth/services/` vs `pedidos/routes/` | Inconsistencia arquitectónica | ⏸️ Pospuesto |
| MF-06 | `DireccionEntrega` fields no coinciden con spec (`alias`, `linea1`) | `auth/models/direccion.py` | Docs especifican `alias`, `linea1`; actual usa `calle`, `numero` | ⏸️ Pospuesto (cambio breaking) |
| MF-07 | RefreshToken no almacena SHA-256 | `auth/models/refresh_token.py` | Docs especifican `token_hash` | ⏸️ Pospuesto (rompe auth) |

## 🟢 Minor Fixes

| ID | Problema | Localización | Fix |
|----|----------|--------------|-----|
| mF-01 | Seed script no usa `ON CONFLICT DO NOTHING` | `backend/seed.py` | ⏸️ Pospuesto |
| mF-02 | `widgets/` layer ausente en frontend | `frontend/src/` | ⏸️ Pospuesto (no bloquea) |
| mF-03 | `Rol` usa autoincrement INT en vez de VARCHAR PK | `auth/models/rol.py` | ⏸️ Pospuesto (cambio breaking) |
| mF-04 | Sin tests frontend para cartStore ni paymentStore | `frontend/src/app/store/__tests__/` | ⏸️ Pospuesto |
| mF-05 | `profile-page.tsx` referencia `telefono` que no existe en type User | `pages/auth/profile-page.tsx` | ⏸️ Pospuesto |
