# 🗺️ MAPA COMPLETO DE CHANGES — Food Store E-Commerce

**Documento de Planificación Estratégica (OPSX)**  
Generado: 2026-04-28 · Basado en: Descripción.txt, Historias_de_usuario.txt, CHANGES.md

---

## 📋 Índice de Contenidos

1. [Visión General](#visión-general)
2. [Principios de Agrupación](#principios-de-agrupación)
3. [Mapa Detallado de Changes (50 total)](#mapa-detallado-de-changes)
   - Sprint 0: Infraestructura [1 change]
   - Sprint 1: Autenticación [3 changes]
   - Sprint 2: Catálogo [5 changes]
   - Sprint 3: Direcciones & Carrito [3 changes]
   - Sprint 4: Pedidos Core [3 changes]
   - Sprint 5: Pagos MercadoPago [2 changes]
   - Sprint 6: Admin & Métricas [2 changes]
   - Sprint 7: Integraciones & Polish [5 changes]
4. [Matriz de Dependencias](#matriz-de-dependencias)
5. [Timeline Estimado](#timeline-estimado)

---

## 🎯 Visión General

Food Store se desarrolla en **7 sprints** con **50 changes totales**, organizados en capas verticales (features) que pueden implementarse en paralelo una vez resueltas sus dependencias.

**Principio de Agrupación**: Cada change agrupa de 5-15 historias de usuario estrechamente relacionadas (misma funcionalidad, mismo dominio, comparten modelos y repositorios). Esto minimiza los context switches y facilita la revisión en PR.

### Estadísticas

| Métrica | Valor |
|---------|-------|
| **Total de changes** | 50 |
| **Total de historias de usuario** | 75+ (US-000 through US-076) |
| **Epics/Sprints** | 8 (Sprint 0-7) |
| **Dependencias críticas** | 7 (bloqueos de sprint) |
| **Cambios en paralelo máximos** | 4-6 por sprint |
| **Tamaño promedio de change** | 12-20 tareas |

---

## 🔧 Principios de Agrupación

Cada change respeta estos criterios:

1. **Coherencia de Dominio**: Todas las historias en un change pertenecen al mismo dominio (ej: "Categorías Jerárquicas" agrupa US-007, US-008, US-009)

2. **Una Entidad Principal**: El change se centra en una tabla/modelo (ej: `Producto`, `Pedido`, `Usuario`)

3. **Flujo Completo**: Incluye backend (modelos + API) Y frontend (componentes + hooks) en el mismo change

4. **Tamaño Manejable**: 12-20 tareas por change (≈4-6 horas de implementación)

5. **Independencia Relativa**: Minimiza interdependencias intra-sprint; agrupa lo que SÍ debe estar junto

---

## 📊 Mapa Detallado de Changes

### **SPRINT 0: Infraestructura** ✅ COMPLETADO

#### `sprint-0-infraestructura` [ARCHIVADO]
- **Historias**: US-000, US-000a, US-000b, US-000c, US-000d, US-000e, US-068, US-074
- **Tareas**: 112
- **Funcionalidad**: 
  - Monorepo setup (Git, estructura, .gitignore, README)
  - FastAPI + PostgreSQL + Alembic
  - React + Vite + Zustand
  - BaseRepository[T] + UnitOfWork
  - JWT + RBAC (4 roles)
  - RFC 7807 error handling
  - 4 stores (auth, cart, payment, ui)
- **Dependencias**: Ninguna (es la base)
- **Estado**: ✅ 100% (archivado 2026-04-28)

---

### **SPRINT 1: Autenticación & Autorización**

#### `sprint-1-autenticacion` (US-001, US-002, US-003, US-004, US-005)
- **Funcionalidad**: Registro, login, refresh token, logout, RBAC avanzado
- **Backend Tasks** (~25):
  - [ ] Endpoint POST /api/v1/auth/register (validar email único, hash password, asignar rol CLIENT)
  - [ ] Endpoint POST /api/v1/auth/login (bcrypt verify, JWT generation, refresh token storage)
  - [ ] Endpoint POST /api/v1/auth/refresh (token rotation, replay attack detection)
  - [ ] Endpoint POST /api/v1/auth/logout (invalidate refresh token)
  - [ ] Service de autenticación con rate limiting (5 intentos / 15 min por IP)
  - [ ] Repository de RefreshToken con métodos: create, get_valid, invalidate_all
  - [ ] Dependency: get_current_user mejorada con extracción de roles
  - [ ] Dependency: require_role con validación de múltiples roles
  - [ ] Tests: auth service, dependency injection, rate limiting
- **Frontend Tasks** (~12):
  - [ ] LoginPage con formulario (email, password)
  - [ ] RegisterPage con validación en tiempo real
  - [ ] useAuth hook mejorado (login, register, logout, hasRole)
  - [ ] Interceptor de refresh token automático
  - [ ] Error handling para 401/403
  - [ ] Tests: auth flow, interceptor, hooks
- **Historias Cubiertas**:
  - US-001: Registro de cliente
  - US-002: Login de usuario
  - US-003: Refresh de token (rotación)
  - US-004: Logout
  - US-005: Gestión de roles (RBAC)
- **Dependencias**: sprint-0-infraestructura ✅
- **Estimated Time**: 6-8 horas

---

#### `sprint-1-gestion-usuarios` (US-049, US-050, US-054, US-055, US-063, US-064)
- **Funcionalidad**: CRUD de usuarios, asignación de roles (admin only), auditoría
- **Backend Tasks** (~18):
  - [ ] Endpoint GET /api/v1/usuarios/self (usuario actual con roles)
  - [ ] Endpoint GET /api/v1/usuarios (admin only, con paginación + filtros)
  - [ ] Endpoint GET /api/v1/usuarios/{id} (admin only)
  - [ ] Endpoint PUT /api/v1/usuarios/{id} (editar nombre, email, teléfono)
  - [ ] Endpoint DELETE /api/v1/usuarios/{id} (soft delete)
  - [ ] Endpoint POST /api/v1/usuarios/{id}/roles (asignar rol, admin only)
  - [ ] Endpoint DELETE /api/v1/usuarios/{id}/roles/{rol_id} (revocar rol, con protección last-admin)
  - [ ] UsuarioRepository con: get_by_email, list_with_roles, count
  - [ ] Validación: no puede quitarse ADMIN si es el último
  - [ ] Tests: CRUD, role management, last-admin protection
- **Frontend Tasks** (~14):
  - [ ] AdminDashboard → UsersSection (lista paginada de usuarios)
  - [ ] UserDetailModal (editar datos básicos)
  - [ ] RoleAssignmentModal (asignar/revocar roles)
  - [ ] useUsers hook (fetch, filter, paginate)
  - [ ] Tabla con acciones (editar, eliminar, asignar roles)
  - [ ] Confirmación para soft delete
  - [ ] Tests: user list, role management UI
- **Historias Cubiertas**:
  - US-049: Ver perfil propio
  - US-050: Editar datos propios
  - US-054: Gestión de usuarios (admin)
  - US-055: Eliminar usuarios (soft delete)
  - US-063: Cambiar contraseña
  - US-064: Auditoría de cambios
- **Dependencias**: sprint-1-autenticacion (para get_current_user)
- **Estimated Time**: 5-7 horas

---

#### `sprint-1-seguridad-avanzada` (US-006, US-073, US-075, US-076)
- **Funcionalidad**: Rate limiting, segregación de permisos por rol, validación
- **Backend Tasks** (~16):
  - [ ] Rate limiting en /login (slowapi), /register, endpoints sensibles
  - [ ] Middleware de validación de permisos por rol (STOCK ≠ PEDIDOS ≠ CLIENT)
  - [ ] Validación de propiedad (CLIENT solo ve sus datos)
  - [ ] Respuestas 403 vs 404 (no revelar existencia de recursos)
  - [ ] Sanitización de inputs (XSS prevention)
  - [ ] Validación de tipos (números, emails, etc.)
  - [ ] Logging de accesos no autorizados
  - [ ] Tests: role segregation, permission validation
- **Frontend Tasks** (~8):
  - [ ] Error pages (401 Unauthorized, 403 Forbidden, 404 Not Found)
  - [ ] RoleProtectedRoute mejorada (redirect a /403 si no tiene permiso)
  - [ ] Componentes deshabilitados por rol (no mostrar opciones no permitidas)
  - [ ] Toast notifications para errores de permisos
  - [ ] Tests: role guards, error handling
- **Historias Cubiertas**:
  - US-006: Control de acceso basado en roles
  - US-073: Rate limiting
  - US-075: Segregación de responsabilidades (Gestor Stock, Gestor Pedidos)
  - US-076: Manejo de errores 401/403
- **Dependencias**: sprint-1-autenticacion
- **Estimated Time**: 4-5 horas

---

### **SPRINT 2: Catálogo de Productos**

#### `sprint-2-categorias-jerarquicas` (US-007, US-008, US-009, US-010)
- **Funcionalidad**: Categorías con jerarquía (padre-hijo autoreferencial), CRUD
- **Backend Tasks** (~22):
  - [ ] Modelo Categoria con FK autoreferencial (padre_id)
  - [ ] Endpoint POST /api/v1/categorias (crear, validar no ciclos)
  - [ ] Endpoint GET /api/v1/categorias (arbol completo con CTE recursiva)
  - [ ] Endpoint GET /api/v1/categorias/{id} (con subcategorías)
  - [ ] Endpoint PUT /api/v1/categorias/{id} (editar, validar no ciclos)
  - [ ] Endpoint DELETE /api/v1/categorias/{id} (soft delete, validar sin productos)
  - [ ] CategoriaRepository con: get_tree, get_descendants, get_parent, validate_no_cycles
  - [ ] Validación: no asignar categoria como padre de sí misma
  - [ ] Validación: no eliminar si tiene productos
  - [ ] Tests: jerarquía, ciclos, soft delete
- **Frontend Tasks** (~16):
  - [ ] AdminDashboard → CategoriesSection (árbol jerárquico)
  - [ ] CategoryTreeView (componente recursivo para visualizar árbol)
  - [ ] CreateCategoryModal (nombre, descripción, padre, imagen)
  - [ ] EditCategoryModal
  - [ ] DeleteCategoryConfirmation (validar sin productos)
  - [ ] useCategories hook (fetch tree, create, update, delete)
  - [ ] Tests: tree rendering, CRUD
- **Historias Cubiertas**:
  - US-007: Categorías jerárquicas
  - US-008: Mostrar árbol de categorías
  - US-009: Validar no ciclos
  - US-010: No eliminar con productos
- **Dependencias**: sprint-0-infraestructura
- **Estimated Time**: 6-8 horas

---

#### `sprint-2-ingredientes-alergenos` (US-017, US-031, US-032)
- **Funcionalidad**: Ingredientes con flags de alérgenos, CRUD
- **Backend Tasks** (~18):
  - [ ] Modelo Ingrediente con es_alergeno flag
  - [ ] Endpoint POST /api/v1/ingredientes (crear con flag alérgeno)
  - [ ] Endpoint GET /api/v1/ingredientes (listar con filtro por alérgeno)
  - [ ] Endpoint PUT /api/v1/ingredientes/{id}
  - [ ] Endpoint DELETE /api/v1/ingredientes/{id} (soft delete)
  - [ ] IngredienteRepository con: list_by_allergen, count_by_allergen
  - [ ] Validación de alérgenos comunes (gluten, lactosa, frutos secos, maní, etc.)
  - [ ] Tests: CRUD, allergen flags
- **Frontend Tasks** (~12):
  - [ ] AdminDashboard → IngredientsSection
  - [ ] CreateIngredientModal (nombre, descripción, flag alérgeno)
  - [ ] IngredientList con filtro por alérgeno
  - [ ] AllergenTag componente (visual para alérgenos)
  - [ ] useIngredients hook
  - [ ] Tests: ingredient CRUD, allergen filtering
- **Historias Cubiertas**:
  - US-017: Ingredientes y alérgenos
  - US-031: Filtrar por alérgenos
  - US-032: Mostrar advertencias de alérgenos
- **Dependencias**: sprint-0-infraestructura
- **Estimated Time**: 4-5 horas

---

#### `sprint-2-catalogo-productos` (US-015, US-016, US-018, US-020, US-021, US-022)
- **Funcionalidad**: CRUD de productos, asignación a categorías/ingredientes, visibilidad pública
- **Backend Tasks** (~28):
  - [ ] Modelo Producto con NUMERIC precio, INTEGER stock, booleano disponible
  - [ ] Relación M2M ProductoCategoria
  - [ ] Relación M2M ProductoIngrediente
  - [ ] Endpoint POST /api/v1/productos (crear, asignar categorías/ingredientes, validar stock >= 0)
  - [ ] Endpoint GET /api/v1/productos (public, paginado, filtrar por categoría/disponibilidad)
  - [ ] Endpoint GET /api/v1/productos/admin (admin only, incluir soft deleted)
  - [ ] Endpoint GET /api/v1/productos/{id}
  - [ ] Endpoint PUT /api/v1/productos/{id} (editar precio, stock, disponibilidad)
  - [ ] Endpoint DELETE /api/v1/productos/{id} (soft delete)
  - [ ] ProductoRepository con: list_public, list_by_category, list_by_ingredient, search
  - [ ] Validación: stock nunca negativo, precio NUMERIC exacto
  - [ ] Stock snapshot en pedidos (ver sprint-4)
  - [ ] Tests: CRUD, M2M relations, visibility
- **Frontend Tasks** (~20):
  - [ ] CatalogPage (lista paginada de productos, filtrar por categoría)
  - [ ] ProductCard (imagen, nombre, precio, stock, ingredientes, alérgenos)
  - [ ] ProductDetailModal (descripción completa, ingredientes detallados, botón agregar al carrito)
  - [ ] AdminDashboard → ProductsSection (CRUD, editar stock, disponibilidad)
  - [ ] CreateProductModal (nombre, descripción, precio, stock, seleccionar categorías/ingredientes)
  - [ ] EditProductModal
  - [ ] SearchBar con filtro por categoría
  - [ ] useProducts hook (fetch catalog, admin CRUD)
  - [ ] Tests: product listing, filtering, detail view
- **Historias Cubiertas**:
  - US-015: Crear productos (admin + Gestor Stock)
  - US-016: M2M productos-categorías
  - US-018: Catálogo público (paginado, soft delete)
  - US-020: Mostrar precios
  - US-021: Validar stock
  - US-022: Soft delete de productos
- **Dependencias**: sprint-2-categorias-jerarquicas, sprint-2-ingredientes-alergenos
- **Estimated Time**: 8-10 horas

---

#### `sprint-2-busqueda-filtros` (US-023, US-051, US-052, US-053)
- **Funcionalidad**: Búsqueda full-text, filtros avanzados, recomendaciones
- **Backend Tasks** (~16):
  - [ ] FTS (Full-Text Search) en productos (nombre, descripción)
  - [ ] Endpoint GET /api/v1/productos/search (query, categoria, precios min/max, alérgenos)
  - [ ] ProductoRepository con: search_by_text, filter_by_price_range, filter_by_allergens
  - [ ] Índices en name, description, price para performance
  - [ ] Paginación con cursor o skip/limit
  - [ ] Tests: search accuracy, filter combinations
- **Frontend Tasks** (~12):
  - [ ] SearchBar avanzada (query + filtros)
  - [ ] FilterSidebar (categoría, precio, alérgenos)
  - [ ] Mostrar resultados con highlight (si aplica)
  - [ ] Faceted search UI
  - [ ] useSearch hook (query, filters, pagination)
  - [ ] Tests: search, filtering
- **Historias Cubiertas**:
  - US-023: Búsqueda de productos
  - US-051: Listado de productos con paginación
  - US-052: Filtro por precio
  - US-053: Filtro por alérgenos
- **Dependencias**: sprint-2-catalogo-productos
- **Estimated Time**: 5-6 horas

---

### **SPRINT 3: Direcciones de Entrega & Carrito de Compras**

#### `sprint-3-direcciones-entrega` (US-024, US-025, US-026, US-027, US-028, US-038)
- **Funcionalidad**: CRUD de direcciones de entrega, predeterminada por usuario
- **Backend Tasks** (~16):
  - [ ] Modelo DireccionEntrega (calle, numero, piso, departamento, ciudad, codPostal, referencia, es_predeterminada)
  - [ ] Endpoint POST /api/v1/direcciones (crear, primera es predeterminada automáticamente)
  - [ ] Endpoint GET /api/v1/direcciones (lista del usuario actual)
  - [ ] Endpoint GET /api/v1/direcciones/{id} (una dirección del usuario)
  - [ ] Endpoint PUT /api/v1/direcciones/{id} (editar, cambiar predeterminada)
  - [ ] Endpoint DELETE /api/v1/direcciones/{id} (soft delete)
  - [ ] DireccionRepository con: get_by_user_id, get_default_for_user
  - [ ] Validación: ownership (solo el usuario ve/edita sus direcciones)
  - [ ] Validación: solo una predeterminada por usuario
  - [ ] Snapshot en pedidos (copiar dirección al crear pedido)
  - [ ] Tests: CRUD, ownership, default validation
- **Frontend Tasks** (~14):
  - [ ] AddressListPage (mis direcciones)
  - [ ] AddressCard (mostrar dirección, marcar como predeterminada, editar, eliminar)
  - [ ] AddAddressModal (formulario completo)
  - [ ] EditAddressModal
  - [ ] DeleteAddressConfirmation
  - [ ] useAddresses hook (fetch, CRUD, setDefault)
  - [ ] Tests: address CRUD, ownership validation
- **Historias Cubiertas**:
  - US-024: Múltiples direcciones por usuario
  - US-025: Ver propias direcciones
  - US-026: Editar propias direcciones
  - US-027: Eliminar propias direcciones
  - US-028: Dirección predeterminada
  - US-038: Dirección snapshot en pedido
- **Dependencias**: sprint-1-autenticacion (get_current_user)
- **Estimated Time**: 5-7 horas

---

#### `sprint-3-carrito-compras` (US-029, US-030, US-033, US-034, US-035)
- **Funcionalidad**: Carrito cliente-side con Zustand, personalizaciones (exclusión de ingredientes)
- **Backend Tasks** (~0, es client-side):
  - (No hay backend changes, el carrito vive en Zustand + localStorage)
- **Frontend Tasks** (~18):
  - [ ] cartStore mejorado (items, personalizacion, totalPrice)
  - [ ] Carrito persistente en localStorage (sobrevive refresh, logout)
  - [ ] ShoppingCartPage (visualizar items del carrito)
  - [ ] CartItem componente (nombre, precio, cantidad, ingredientes excluidos, botón eliminar)
  - [ ] QuantityControl (incrementar/decrementar cantidad)
  - [ ] RemoveItemButton
  - [ ] ClearCartButton
  - [ ] CartSummary (subtotal, total items, botón checkout)
  - [ ] AddToCartButton en ProductDetailModal (cantidad, ingredientes a excluir)
  - [ ] ProductPersonalizationModal (seleccionar ingredientes a excluir, validar que sean del producto)
  - [ ] Validación: solo excluir ingredientes que el producto tenga
  - [ ] useCart hook (addItem, removeItem, updateQuantity, clearCart, getTotalPrice)
  - [ ] Tests: carrito persistence, personalization, quantity management
- **Historias Cubiertas**:
  - US-029: Carrito con persistencia
  - US-030: Personalización (exclusión de ingredientes)
  - US-033: Modificar cantidad en carrito
  - US-034: Eliminar items del carrito
  - US-035: Ir al checkout (initiate payment flow)
- **Dependencias**: sprint-2-catalogo-productos (para productos en carrito)
- **Estimated Time**: 4-5 horas

---

#### `sprint-3-checkout-preview` (US-036, US-037, US-040, US-044)
- **Funcionalidad**: Vista previa de pedido antes de pagar, calcular total con snapshots
- **Backend Tasks** (~12):
  - [ ] Servicio de validación de pedido (stock suficiente, precios, direcciones válidas)
  - [ ] Servicio de cálculo de total (suma de items + envío)
  - [ ] Validación: stock suficiente para todos los items (SELECT FOR UPDATE)
  - [ ] Cálculo de envío (zona + peso o tarifa plana)
  - [ ] Tests: order validation, total calculation
- **Frontend Tasks** (~16):
  - [ ] CheckoutPage (resumen de carrito + cálculo de envío)
  - [ ] OrderSummary (listar items, subtotal, envío, total)
  - [ ] ShippingCalculator (seleccionar dirección, calcular costo)
  - [ ] SelectShippingAddressModal (mostrar direcciones guardadas, crear nueva)
  - [ ] PaymentMethodSelector (tarjeta de crédito, etc.)
  - [ ] ReviewOrderModal (revisar antes de confirmar)
  - [ ] useCheckout hook (validate cart, calculate shipping, create order)
  - [ ] Tests: checkout flow, shipping calculation
- **Historias Cubiertas**:
  - US-036: Validar stock antes de crear pedido
  - US-037: Snapshot de precios en pedido
  - US-040: Ver resumen de pedido
  - US-044: Historial de estados de pedido (vista para usuario)
- **Dependencias**: sprint-3-carrito-compras, sprint-3-direcciones-entrega, sprint-2-catalogo-productos
- **Estimated Time**: 6-7 horas

---

### **SPRINT 4: Pedidos — Creación y Máquina de Estados**

#### `sprint-4-creacion-pedidos` (US-039, US-041, US-042, US-047)
- **Funcionalidad**: Crear pedidos (ATOMIC Unit of Work), generar snapshots, transición de estados
- **Backend Tasks** (~26):
  - [ ] Modelo Pedido (usuario_id, estado_id, dirección, total, dirección_snapshot)
  - [ ] Modelo DetallePedido (producto_id, cantidad, precio_snapshot, personalizacion INT[])
  - [ ] Modelo HistorialEstadoPedido (append-only, registro de transiciones)
  - [ ] Endpoint POST /api/v1/pedidos (crear desde carrito, transacción atómica)
    - Validar stock suficiente (SELECT FOR UPDATE)
    - Generar snapshots de precios y dirección
    - Crear DetallePedido para cada item
    - Estado inicial: PENDIENTE
    - Registrar en HistorialEstadoPedido
  - [ ] Endpoint GET /api/v1/pedidos (del usuario actual, paginado)
  - [ ] Endpoint GET /api/v1/pedidos/{id} (ver detalles del pedido)
  - [ ] Endpoint GET /api/v1/pedidos/admin (admin only, todos los pedidos)
  - [ ] PedidoRepository con: create_with_details, list_by_user, list_all, get_by_id
  - [ ] Servicio de creación (Unit of Work: productos.update_stock, pedidos.create, historial.log)
  - [ ] Validación: stock suficiente (atómica)
  - [ ] Snapshots: guardar precio actual de cada producto, dirección completa
  - [ ] Tests: order creation, atomicity, snapshots, history logging
- **Frontend Tasks** (~12):
  - [ ] OrderConfirmationPage (mostrar después de crear pedido)
  - [ ] OrderListPage (mis pedidos, paginado)
  - [ ] OrderCard (ID, fecha, estado, total, botón ver detalles)
  - [ ] OrderDetailModal (detalles completos, historial de estados)
  - [ ] useOrders hook (fetch user orders, fetch order detail)
  - [ ] Tests: order creation, order list, order detail
- **Historias Cubiertas**:
  - US-039: Crear pedido (transición PENDIENTE → CONFIRMADO automática con pago)
  - US-041: Ver estado de pedido
  - US-042: Estados terminales (ENTREGADO, CANCELADO)
  - US-047: Ver detalles de pedido
- **Dependencias**: sprint-3-checkout-preview, sprint-0-infraestructura (Unit of Work)
- **Estimated Time**: 8-10 horas

---

#### `sprint-4-fsm-pedidos` (US-039, US-042, US-043, US-044)
- **Funcionalidad**: Máquina de estados de pedidos (PENDIENTE → CONFIRMADO → EN_PREPARACIÓN → EN_CAMINO → ENTREGADO/CANCELADO)
- **Backend Tasks** (~22):
  - [ ] Endpoint POST /api/v1/pedidos/{id}/transicion (avanzar estado)
  - [ ] Validación de transiciones permitidas (solo secuencial)
  - [ ] Transición PENDIENTE → CONFIRMADO (automática con pago, no manual)
  - [ ] Transición CONFIRMADO → EN_PREPARACIÓN (Gestor Pedidos)
  - [ ] Transición EN_PREPARACIÓN → EN_CAMINO (Gestor Pedidos)
  - [ ] Transición EN_CAMINO → ENTREGADO (Sistema o Gestor)
  - [ ] Cancelación desde PENDIENTE (Cliente/Gestor/Admin)
  - [ ] Cancelación desde CONFIRMADO (Gestor/Admin only)
  - [ ] Cancelación desde EN_PREPARACIÓN (Admin only, con restauración de stock)
  - [ ] ENTREGADO y CANCELADO son terminales (no transiciones)
  - [ ] Al confirmar (→CONFIRMADO): decrementar stock atómicamente
  - [ ] Al cancelar desde CONFIRMADO: restaurar stock atómicamente
  - [ ] Registrar en HistorialEstadoPedido (timestamp, usuario/SISTEMA, observación)
  - [ ] Servicio de FSM con reglas de negocio centralizadas
  - [ ] Tests: valid transitions, invalid transitions, stock management, history logging
- **Frontend Tasks** (~10):
  - [ ] OrderStatusBadge componente (visualizar estado con color)
  - [ ] OrderHistoryTimeline (mostrar historial de cambios de estado)
  - [ ] CancelOrderButton (visible si estado permite cancelación)
  - [ ] Confirmación para cancelar
  - [ ] Toast notification cuando cambia estado (en tiempo real, si se integra polling/websocket)
  - [ ] Tests: FSM state transitions, history display
- **Historias Cubiertas**:
  - US-039: Transición PENDIENTE → CONFIRMADO (automática con pago)
  - US-042: Estados terminales
  - US-043: Cancelar pedido (con restauración de stock)
  - US-044: Ver historial de estados
- **Dependencias**: sprint-4-creacion-pedidos
- **Estimated Time**: 7-9 horas

---

#### `sprint-4-admin-gestion-pedidos` (US-051, US-060, US-061, US-062, US-065)
- **Funcionalidad**: Panel de Gestor de Pedidos (listar, filtrar, cambiar estado, cancelar)
- **Backend Tasks** (~14):
  - [ ] Endpoint GET /api/v1/admin/pedidos (Gestor Pedidos only, listar todos)
  - [ ] Filtros: por estado, por rango de fechas, por usuario, búsqueda
  - [ ] Paginación con sort por fecha/estado
  - [ ] Endpoint POST /api/v1/admin/pedidos/{id}/transicion (cambiar estado, validar permisos)
  - [ ] Endpoint POST /api/v1/admin/pedidos/{id}/cancelar (cancelar con razón, restaurar stock)
  - [ ] Repository con: list_with_filters, list_by_status, count_by_status
  - [ ] Tests: filtering, pagination, role-based transitions
- **Frontend Tasks** (~14):
  - [ ] AdminDashboard → OrdersSection
  - [ ] OrdersTable (ID, usuario, fecha, estado, total, acciones)
  - [ ] OrdersFilter (estado, rango fechas, búsqueda usuario)
  - [ ] OrdersStatusChart (gráfico de pedidos por estado)
  - [ ] ChangeOrderStatusModal (seleccionar nuevo estado, añadir observación)
  - [ ] CancelOrderModal (cancelar con razón)
  - [ ] useAdminOrders hook (fetch filtered orders, change status, cancel)
  - [ ] Tests: filtering UI, status change, cancel action
- **Historias Cubiertas**:
  - US-051: Listar pedidos (paginación)
  - US-060: Dashboard de Gestor Pedidos
  - US-061: Filtrar pedidos por estado
  - US-062: Cambiar estado de pedido (transiciones permitidas)
  - US-065: Cancelar pedidos
- **Dependencias**: sprint-4-fsm-pedidos
- **Estimated Time**: 6-7 horas

---

### **SPRINT 5: Pagos — Integración MercadoPago**

#### `sprint-5-mercadopago-checkout` (US-045, US-046, US-048)
- **Funcionalidad**: Integración frontend + backend con MercadoPago (preferencias, webhooks, tokens)
- **Backend Tasks** (~20):
  - [ ] Modelo Pago (pedido_id, mercadopago_payment_id, mercadopago_preference_id, estado, total, timestamp)
  - [ ] Endpoint POST /api/v1/pagos/crear-preferencia (crear orden en MP, generar external_reference)
  - [ ] Endpoint POST /api/v1/pagos/webhook (IPN de MercadoPago, procesar estado de pago)
  - [ ] Webhook handler (approved → transición PENDIENTE→CONFIRMADO + decrementar stock)
  - [ ] Webhook handler (rejected → pago queda rechazado, pedido PENDIENTE)
  - [ ] Webhook handler (pending → registro pero pedido sigue PENDIENTE)
  - [ ] Idempotency key para evitar duplicados
  - [ ] Verificación de estado real consultando API de MP (no confiar solo en webhook)
  - [ ] Servicio de pagos (crear preferencia, procesar webhook, consultar estado)
  - [ ] Repository de Pago (create, get_by_pedido, get_by_preference)
  - [ ] Tests: webhook processing, idempotency, state transitions
- **Frontend Tasks** (~16):
  - [ ] PaymentPage (mostrar MercadoPago checkout widget)
  - [ ] MercadoPagoButton (integrar SDK de MP)
  - [ ] Tokenización de tarjeta (via MercadoPago.js)
  - [ ] PaymentForm (campo de tarjeta embebido)
  - [ ] PaymentStatusModal (mostrar estado: processing, approved, rejected)
  - [ ] RetryPaymentButton (reintentar pago si fue rechazado)
  - [ ] usePayment hook (create preference, process payment, check status)
  - [ ] Tests: payment flow, error handling, retry logic
- **Historias Cubiertas**:
  - US-045: Integración MercadoPago (tokenización, preferencia)
  - US-046: Webhook de MercadoPago (cambios de estado automáticos)
  - US-048: Múltiples intentos de pago
- **Dependencias**: sprint-4-creacion-pedidos, sprint-3-checkout-preview
- **Estimated Time**: 10-12 horas

---

#### `sprint-5-pagos-admin` (US-057, US-058, US-059, US-066, US-067)
- **Funcionalidad**: Panel de admin para gestión de pagos, reembolsos, auditoría
- **Backend Tasks** (~16):
  - [ ] Endpoint GET /api/v1/admin/pagos (admin only, listar todos)
  - [ ] Filtros: por estado (approved, rejected, pending), por rango fechas
  - [ ] Endpoint GET /api/v1/admin/pagos/{id}
  - [ ] Endpoint POST /api/v1/admin/pagos/{id}/reembolsar (crear reembolso en MP)
  - [ ] Servicio de reembolsos (llamar API de MP, registrar en BD)
  - [ ] Repository con: list_by_status, list_by_date_range, count_by_status
  - [ ] Auditoría: logs de reembolsos y cambios
  - [ ] Tests: reembolso workflow, filtering
- **Frontend Tasks** (~12):
  - [ ] AdminDashboard → PaymentsSection
  - [ ] PaymentsTable (ID, pedido, usuario, monto, estado, fecha)
  - [ ] PaymentsFilter (estado, rango fechas)
  - [ ] PaymentDetailModal (detalles completos, historial de intentos)
  - [ ] RefundButton + RefundModal (crear reembolso)
  - [ ] useAdminPayments hook (fetch filtered payments, create refund)
  - [ ] Tests: payments table, refund action
- **Historias Cubiertas**:
  - US-057: Ver historial de pagos (admin)
  - US-058: Filtrar pagos por estado
  - US-059: Ver detalles de pago
  - US-066: Realizar reembolsos
  - US-067: Auditoría de transacciones
- **Dependencias**: sprint-5-mercadopago-checkout
- **Estimated Time**: 6-7 horas

---

### **SPRINT 6: Admin Dashboard & Métricas**

#### `sprint-6-admin-dashboard` (US-070, US-071, US-072)
- **Funcionalidad**: Dashboard principal del admin con resumen de KPIs y acceso a funciones
- **Backend Tasks** (~14):
  - [ ] Endpoint GET /api/v1/admin/stats (KPIs: total ventas, pedidos hoy, usuarios activos, stock bajo)
  - [ ] Endpoint GET /api/v1/admin/stats/revenue (ingresos por período: día, semana, mes)
  - [ ] Endpoint GET /api/v1/admin/stats/orders (pedidos por estado, en tiempo real)
  - [ ] Endpoint GET /api/v1/admin/stats/products (productos con bajo stock, más vendidos)
  - [ ] Queries eficientes (índices, aggregations)
  - [ ] Caché de estadísticas (actualizar cada 5 minutos)
  - [ ] Tests: stats accuracy, performance
- **Frontend Tasks** (~16):
  - [ ] AdminDashboard layout (sidebar con navegación a secciones)
  - [ ] StatsCards (mostrar KPIs en tarjetas)
  - [ ] RevenueChart (recharts: gráfico de ingresos por período)
  - [ ] OrdersChart (recharts: gráfico de pedidos por estado, pie chart)
  - [ ] LowStockAlert (mostrar productos con stock bajo)
  - [ ] TopProductsList (productos más vendidos)
  - [ ] useAdminStats hook (fetch stats with polling/SWR)
  - [ ] Tests: chart rendering, stats display
- **Historias Cubiertas**:
  - US-070: Dashboard de admin (KPIs, gráficos)
  - US-071: Métricas de ventas
  - US-072: Alertas de inventario bajo
- **Dependencias**: sprint-4-creacion-pedidos, sprint-5-mercadopago-checkout
- **Estimated Time**: 7-9 horas

---

#### `sprint-6-admin-configuracion` (US-069, US-075)
- **Funcionalidad**: Panel de configuración del sistema (formas de pago, estados de pedido, parámetros globales)
- **Backend Tasks** (~12):
  - [ ] Endpoint GET /api/v1/admin/config (obtener configuración global)
  - [ ] Endpoint PUT /api/v1/admin/config (actualizar configuración, admin only)
  - [ ] Endpoint GET /api/v1/admin/formas-pago (listar)
  - [ ] Endpoint PUT /api/v1/admin/formas-pago/{id} (habilitar/deshabilitar)
  - [ ] Configuración de: envío (tarifa plana vs por zona), MercadoPago keys, rate limiting
  - [ ] Caché de configuración (invalidar al actualizar)
  - [ ] Tests: config updates, permission validation
- **Frontend Tasks** (~10):
  - [ ] AdminDashboard → ConfigurationSection
  - [ ] ConfigForm (formas de pago, envío, API keys)
  - [ ] PaymentMethodsConfig (habilitar/deshabilitar)
  - [ ] ShippingConfig (tarifa de envío)
  - [ ] useAdminConfig hook (fetch, update)
  - [ ] Tests: config updates
- **Historias Cubiertas**:
  - US-069: Configuración global del sistema
  - US-075: Segregación de responsabilidades (ver en security sprint)
- **Dependencias**: sprint-0-infraestructura
- **Estimated Time**: 4-5 horas

---

### **SPRINT 7: Integraciones & Polish**

#### `sprint-7-notificaciones-email` (US-056, US-069)
- **Funcionalidad**: Envío de emails (confirmación de registro, cambio de estado de pedido, reembolsos)
- **Backend Tasks** (~14):
  - [ ] Servicio de email (SMTP, usar Resend o SendGrid)
  - [ ] Template de email (confirmación de registro)
  - [ ] Template de email (cambio de estado de pedido)
  - [ ] Template de email (confirmación de reembolso)
  - [ ] Cola de emails (celery o async task, para no bloquear requests)
  - [ ] Retry logic para fallos transitorios
  - [ ] Logs de emails enviados
  - [ ] Tests: email sending, templates
- **Frontend Tasks** (~6):
  - [ ] Notificación visual cuando se envía email
  - [ ] Enlace "reenviar confirmación de email" en configuración
  - [ ] Tests: email notifications
- **Historias Cubiertas**:
  - US-056: Confirmación de registro por email
  - US-069: Notificaciones (estado de pedido)
- **Dependencias**: sprint-1-autenticacion, sprint-4-creacion-pedidos
- **Estimated Time**: 5-6 horas

---

#### `sprint-7-historial-cambios-auditar` (US-064, US-067, US-069)
- **Funcionalidad**: Auditoría completa (quién hizo qué, cuándo), changelog de cambios
- **Backend Tasks** (~16):
  - [ ] Tabla de auditoría: usuario, acción, tabla, registro_id, cambio_anterior, cambio_nuevo, timestamp
  - [ ] Middleware/decorator que registra cambios en: usuarios, productos, pedidos, pagos
  - [ ] Endpoint GET /api/v1/admin/audit (admin only, filtrar por tabla, usuario, fecha)
  - [ ] Exportar changelog a CSV/JSON
  - [ ] Queries para reconstruir estado histórico de un registro
  - [ ] Tests: audit logging accuracy, querying
- **Frontend Tasks** (~10):
  - [ ] AdminDashboard → AuditLogSection
  - [ ] AuditTable (usuario, acción, tabla, timestamp, cambios)
  - [ ] AuditDetailModal (mostrar cambio_anterior vs cambio_nuevo)
  - [ ] ExportButton (descargar CSV/JSON)
  - [ ] useAuditLog hook (fetch filtered logs)
  - [ ] Tests: audit log display, filtering
- **Historias Cubiertas**:
  - US-064: Auditoría de cambios de usuario
  - US-067: Auditoría de transacciones
  - US-069: Logs de actividad
- **Dependencias**: sprint-1-gestion-usuarios, sprint-4-creacion-pedidos
- **Estimated Time**: 6-7 horas

---

#### `sprint-7-busqueda-avanzada-admin` (US-051, US-052, US-053, US-061, US-065)
- **Funcionalidad**: Búsqueda avanzada en admin (pedidos, usuarios, productos, pagos)
- **Backend Tasks** (~12):
  - [ ] FTS mejorada para admin (productos, pedidos, usuarios)
  - [ ] Endpoints de búsqueda: /search/productos, /search/pedidos, /search/usuarios
  - [ ] Filtros combinados: fecha, estado, usuario, monto, etc.
  - [ ] Índices optimizados para búsqueda
  - [ ] Tests: search accuracy, filter combinations
- **Frontend Tasks** (~10):
  - [ ] AdminSearchBar (búsqueda global con autocomplete)
  - [ ] SearchFiltersModal (filtros avanzados por tabla)
  - [ ] SearchResultsTable (mostrar resultados con highlight)
  - [ ] useAdminSearch hook
  - [ ] Tests: search functionality
- **Historias Cubiertas**:
  - US-051: Listado con paginación
  - US-052-053: Filtros
  - US-061: Filtrar pedidos
  - US-065: Cancelar pedidos (desde búsqueda)
- **Dependencias**: sprint-4-creacion-pedidos, sprint-1-gestion-usuarios
- **Estimated Time**: 5-6 horas

---

#### `sprint-7-optimizacion-performance` (Técnico, no es historia de usuario)
- **Funcionalidad**: Caché, índices BD, lazy loading, code splitting, CDN para imágenes
- **Backend Tasks** (~12):
  - [ ] Índices en tablas grandes (productos, pedidos, usuarios)
  - [ ] Caché de categorías (raramente cambian)
  - [ ] Caché de configuración global
  - [ ] N+1 query prevention (eager loading con includes)
  - [ ] Paginación por defecto en todos los listados
  - [ ] Tests: performance, N+1 detection
- **Frontend Tasks** (~12):
  - [ ] Code splitting por rutas (lazy load pages)
  - [ ] Image optimization (resize, format, lazy load)
  - [ ] useMemo/useCallback en componentes pesados
  - [ ] TanStack Query devtools para debugging
  - [ ] Bundle size analysis (esbuild plugin)
  - [ ] Tests: performance metrics
- **Dependencias**: Todos los sprints anteriores
- **Estimated Time**: 4-6 horas

---

#### `sprint-7-testing-e2e` (Técnico, no es historia de usuario)
- **Funcionalidad**: Tests end-to-end del flujo completo (registro → búsqueda → compra → pago)
- **Backend Tasks** (~0, cobertura de tests en cada change):
  - (Ya incluido en cada change)
- **Frontend Tasks** (~14):
  - [ ] Test E2E con Cypress/Playwright: registro
  - [ ] Test E2E: login/logout
  - [ ] Test E2E: búsqueda y filtrado
  - [ ] Test E2E: agregar al carrito
  - [ ] Test E2E: checkout
  - [ ] Test E2E: cambio de estado de pedido (con mock de webhook)
  - [ ] Test E2E: admin dashboard
  - [ ] CI/CD pipeline (GitHub Actions)
- **Dependencias**: Todos los sprints
- **Estimated Time**: 5-7 horas

---

## 📈 Matriz de Dependencias

```
SPRINT 0: sprint-0-infraestructura
         │
         ├─→ SPRINT 1: autenticacion
         │        ├─→ gestion-usuarios
         │        └─→ seguridad-avanzada
         │
         ├─→ SPRINT 2: categorias-jerarquicas
         │        ├─→ ingredientes-alergenos
         │        ├─→ catalogo-productos
         │        └─→ busqueda-filtros
         │
         ├─→ SPRINT 3: direcciones-entrega
         │        ├─→ carrito-compras
         │        └─→ checkout-preview
         │
         └─→ SPRINT 4: creacion-pedidos
                  ├─→ fsm-pedidos
                  └─→ admin-gestion-pedidos
                       │
                       └─→ SPRINT 5: mercadopago-checkout
                            └─→ pagos-admin
                                 │
                                 └─→ SPRINT 6: admin-dashboard
                                      └─→ admin-configuracion
                                           │
                                           └─→ SPRINT 7: notificaciones-email
                                                ├─→ historial-cambios
                                                ├─→ busqueda-avanzada-admin
                                                ├─→ optimizacion-performance
                                                └─→ testing-e2e
```

## ⏱️ Timeline Estimado

| Sprint | Changes | Tareas | Horas Est. | Días (5h/día) |
|--------|---------|--------|-----------|---------------|
| 0      | 1       | 112    | ✅ 42     | ✅ 8.4 (completado) |
| 1      | 3       | 58     | 15-19     | 3-4           |
| 2      | 5       | 102    | 24-30     | 5-6           |
| 3      | 3       | 58     | 15-19     | 3-4           |
| 4      | 3       | 68     | 21-26     | 4-5           |
| 5      | 2       | 52     | 16-19     | 3-4           |
| 6      | 2       | 42     | 11-14     | 2-3           |
| 7      | 5       | 84     | 25-31     | 5-6           |
| **TOTAL** | **24** | **576** | **165-208 horas** | **33-42 días de desarrollo** |

**Nota**: El equipo puede trabajar en paralelo (2-3 changes simultáneos por sprint después de sprint-0), lo que reduce el tiempo real a ~3-4 semanas si se coordina bien.

---

## 🎯 Próximas Acciones

1. ✅ **Revisar este mapa** con el equipo — validar dependencias, ajustar tamaños si es necesario
2. 📝 **Crear primer change**: `/opsx:propose sprint-1-autenticacion`
3. 🔄 **Ejecutar changes en paralelo**: sprint-1 tiene 3 changes independientes (auth, gestion-usuarios, seguridad)
4. 📊 **Rastrear progreso** en la matriz de dependencias

---

**Documento generado por análisis OPSX de Food Store**  
**Última revisión: 2026-04-28**
