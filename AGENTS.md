# AGENTS.md — Food Store Gestión

Este archivo define cómo deben trabajar los agentes de IA dentro de este proyecto. Su objetivo es evitar improvisaciones, mantener consistencia arquitectónica y asegurar que cada cambio respete el flujo de desarrollo guiado por especificaciones.

## 1. Contexto del proyecto

Food Store Gestión es un sistema de e-commerce de productos alimenticios desarrollado con enfoque **Spec-Driven Development (SDD)**.

El sistema contempla:

- Catálogo de productos alimenticios.
- Categorías jerárquicas.
- Ingredientes y alérgenos.
- Carrito de compras.
- Pedidos con trazabilidad completa.
- Pagos integrados con MercadoPago.
- Panel administrativo.
- Gestión de usuarios, roles y permisos.
- Autenticación JWT con refresh tokens.
- Backend con arquitectura en capas.
- Frontend con Feature-Sliced Design.

## 2. Fuente de verdad del sistema

Antes de proponer, modificar o implementar cualquier funcionalidad, el agente debe leer y respetar estos documentos:

```text
docs/Descripcion.txt
docs/Integrador.txt
docs/Historias_de_usuario.txt
docs/CHANGES.md
```

Además, debe revisar los artefactos activos y archivados de OpenSpec:

```text
openspec/changes/
openspec/specs/
```

Regla principal: **no se debe implementar código basándose solamente en una interpretación libre del pedido del usuario**. Primero se debe contrastar contra la documentación del proyecto y las specs existentes.

## 3. Stack tecnológico obligatorio

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- Alembic
- PostgreSQL 15+
- Pydantic v2
- python-jose
- bcrypt / passlib
- slowapi
- MercadoPago SDK

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- Zustand
- TanStack Query
- TanStack Form
- Recharts

No reemplazar tecnologías principales sin una propuesta formal en OpenSpec.

## 4. Flujo obligatorio de trabajo

El proyecto usa OPSX/OpenSpec. Todo cambio relevante debe seguir este ciclo:

```text
/opsx:explore   -> analizar, discutir, investigar, sin implementar
/opsx:propose   -> crear proposal.md, design.md, tasks.md y specs
/opsx:apply     -> implementar tareas ya definidas
/opsx:archive   -> cerrar el change y sincronizar specs
```

### Reglas del flujo

- No implementar funcionalidades nuevas sin un change activo.
- No ejecutar `/opsx:apply` si no existen artefactos aprobados.
- No mezclar dos changes en una misma implementación.
- No modificar specs archivadas directamente salvo que el flujo OpenSpec lo indique.
- Si aparece una decisión técnica nueva durante la implementación, pausar y actualizar el diseño antes de seguir.
- Las tareas deben marcarse como completadas en `tasks.md` solamente cuando realmente estén implementadas y verificadas.

## 5. Estructura esperada del backend

El backend debe seguir una estructura **feature-first**. Cada módulo funcional debe ser autocontenido.

Estructura base esperada:

```text
backend/
  app/
    main.py
    core/
      config.py
      security.py
      errors.py
      logging.py
    db/
      base.py
      session.py
      seed.py
      migrations/
    shared/
      repositories/
      unit_of_work.py
      schemas/
      utils/
    auth/
      models.py
      schemas.py
      repositories.py
      services.py
      routes.py
    usuarios/
      models.py
      schemas.py
      repositories.py
      services.py
      routes.py
    productos/
      models.py
      schemas.py
      repositories.py
      services.py
      routes.py
    categorias/
      models.py
      schemas.py
      repositories.py
      services.py
      routes.py
    ingredientes/
      models.py
      schemas.py
      repositories.py
      services.py
      routes.py
    pedidos/
      models.py
      schemas.py
      repositories.py
      services.py
      routes.py
    pagos/
      models.py
      schemas.py
      repositories.py
      services.py
      routes.py
    admin/
      schemas.py
      services.py
      routes.py
  tests/
  requirements.txt
  alembic.ini
```

### Reglas de backend

- Las rutas no deben contener lógica de negocio compleja.
- Las rutas llaman a servicios.
- Los servicios coordinan reglas de negocio.
- Los servicios usan Unit of Work para operaciones transaccionales.
- Los repositorios encapsulan acceso a datos.
- Los modelos SQLAlchemy no deben depender de FastAPI.
- Los schemas Pydantic definen entrada y salida de API.
- Las respuestas de error deben ser centralizadas y consistentes.
- Las operaciones sensibles deben verificar JWT y roles.
- Las operaciones multi-entidad deben ser atómicas mediante UoW.

Flujo obligatorio:

```text
Route -> Service -> UnitOfWork -> Repository -> Model -> Database
```

## 6. Repository Pattern y Unit of Work

El proyecto usa Repository Pattern y Unit of Work como patrones obligatorios.

### Repository

Debe encargarse de:

- Crear registros.
- Buscar por ID.
- Listar con filtros y paginación.
- Actualizar registros.
- Aplicar soft delete cuando corresponda.

No debe contener reglas de negocio.

### Unit of Work

Debe encargarse de:

- Abrir una sesión transaccional.
- Exponer repositorios.
- Confirmar cambios con `commit()`.
- Revertir cambios con `rollback()`.
- Garantizar atomicidad en operaciones compuestas.

Ejemplo conceptual:

```python
async with UnitOfWork() as uow:
    pedido = await uow.pedidos.create(data)
    await uow.detalles_pedido.create_many(detalles)
    await uow.commit()
```

## 7. Autenticación y autorización

El sistema debe usar:

- JWT access token.
- Refresh token con rotación.
- Expiración de access token configurable.
- Expiración de refresh token configurable.
- Revocación de refresh token en logout.
- RBAC basado en roles.

Roles principales:

```text
ADMIN
STOCK
PEDIDOS
CLIENT
```

Reglas:

- No hardcodear permisos directamente dentro de las rutas si pueden centralizarse.
- Usar dependencias como `get_current_user` y `require_role(...)`.
- No permitir eliminar o desactivar el último usuario ADMIN.
- No devolver hashes de contraseña ni información sensible.

## 8. Estructura esperada del frontend

El frontend debe seguir **Feature-Sliced Design (FSD)**.

Estructura base esperada:

```text
frontend/
  src/
    app/
      providers/
      router/
      styles/
    pages/
      login/
      home/
      catalogo/
      producto-detalle/
      carrito/
      checkout/
      pedidos/
      admin/
      not-found/
    features/
      auth/
      cart/
      checkout/
      product-search/
      product-filters/
      order-tracking/
      admin-dashboard/
    entities/
      usuario/
      producto/
      categoria/
      ingrediente/
      pedido/
      pago/
    shared/
      api/
      config/
      constants/
      hooks/
      lib/
      types/
      ui/
  package.json
  vite.config.ts
```

### Reglas de frontend

- `shared/` no debe depender de `features/`, `entities/` ni `pages/`.
- `entities/` representa conceptos del dominio.
- `features/` contiene comportamientos reutilizables.
- `pages/` compone entidades y features.
- `app/` contiene providers globales, router y configuración raíz.
- Las llamadas HTTP deben centralizarse en `shared/api` o servicios por entidad/feature.
- No duplicar URLs de endpoints en componentes.
- No usar Zustand para estado del servidor. Para eso se usa TanStack Query.
- Zustand se usa para estado del cliente: sesión, carrito, UI local, proceso de pago.

## 9. Estado frontend

### Zustand

Usar para:

- Sesión local.
- Carrito.
- Modales.
- Notificaciones UI.
- Estado temporal del checkout.

No suscribirse al store completo si no hace falta.

Correcto:

```ts
const items = useCartStore((state) => state.items);
```

Incorrecto:

```ts
const cartStore = useCartStore();
```

### TanStack Query

Usar para:

- Productos.
- Categorías.
- Pedidos.
- Dashboard.
- Datos remotos cacheables.

## 10. Convenciones de API

La API debe versionarse bajo:

```text
/api/v1
```

Convenciones generales:

- Usar JSON como formato principal.
- Usar códigos HTTP correctos.
- Usar paginación en listados.
- Usar filtros explícitos.
- No exponer campos sensibles.
- Mantener Swagger funcional en `/docs`.
- Mantener ReDoc funcional en `/redoc`.
- Incluir health check en `/api/v1/health`.

## 11. Base de datos

Motor obligatorio:

```text
PostgreSQL 15+
```

Reglas:

- Usar migraciones con Alembic.
- No modificar la base manualmente sin migración.
- Usar timestamps de auditoría: `creado_en`, `actualizado_en`.
- Usar soft delete donde la spec lo indique: `eliminado_en`.
- Mantener constraints de unicidad e integridad referencial.
- Las relaciones muchos-a-muchos deben tener tablas intermedias explícitas.
- No borrar físicamente registros importantes si corresponde soft delete.

## 12. MercadoPago

La integración con MercadoPago debe tratarse como un módulo sensible.

Reglas:

- No hardcodear tokens.
- Usar variables de entorno.
- Separar creación de preferencia, confirmación de pago y webhook/IPN.
- Validar estados de pago antes de cambiar el estado de un pedido.
- Registrar eventos relevantes para trazabilidad.
- No confiar solamente en datos enviados por el frontend.

## 13. Variables de entorno

No commitear archivos `.env`.

Usar ejemplos:

```text
backend/.env.example
frontend/.env.example
```

Variables esperadas de backend:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/foodstore
SECRET_KEY=cambia-esto-por-una-clave-de-64-caracteres-minimo
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
MP_ACCESS_TOKEN=TEST-tu-access-token-de-mercadopago
MP_PUBLIC_KEY=TEST-tu-public-key-de-mercadopago
CORS_ORIGINS=http://localhost:5173
```

Variables esperadas de frontend:

```env
VITE_API_URL=http://localhost:8000
VITE_MP_PUBLIC_KEY=TEST-tu-public-key-de-mercadopago
```

## 14. Comandos habituales

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### OpenSpec / OPSX

```bash
openspec list --json
openspec status --change "nombre-del-change" --json
/opsx:explore tema-o-pregunta
/opsx:propose nombre-del-change
/opsx:apply nombre-del-change
/opsx:archive nombre-del-change
```

## 15. Testing y verificación

Antes de marcar una tarea como completa, el agente debe verificar lo que implementó.

### Backend

Verificaciones mínimas:

```bash
pytest
alembic upgrade head
uvicorn app.main:app --reload
```

Cuando corresponda, probar:

- Health check.
- Login.
- Refresh token.
- Rutas protegidas.
- Roles insuficientes.
- CRUD básico.
- Rollback del Unit of Work.

### Frontend

Verificaciones mínimas:

```bash
npm run dev
npm run build
```

Si existen scripts de lint/test:

```bash
npm run lint
npm run test
```

## 16. Convenciones de commits

Usar conventional commits:

```text
feat(scope): descripcion breve
fix(scope): descripcion breve
docs(scope): descripcion breve
style(scope): descripcion breve
refactor(scope): descripcion breve
test(scope): descripcion breve
chore(scope): descripcion breve
```

Ejemplos:

```text
feat(auth): add JWT refresh token rotation
fix(cart): prevent duplicate cart items
docs(openspec): document sprint 0 infrastructure
refactor(orders): move business rules into service layer
```

## 17. Reglas de seguridad

- No commitear secretos.
- No imprimir tokens en logs.
- No devolver contraseñas ni hashes.
- No confiar en IDs enviados desde el frontend para permisos.
- Validar ownership cuando un cliente accede a sus recursos.
- Sanitizar entradas de texto cuando corresponda.
- Aplicar rate limiting en autenticación.
- Registrar errores sin exponer detalles internos al cliente.

## 18. Manejo de errores

El backend debe usar errores centralizados y consistentes.

Preferencia:

- 400 para requests inválidos por negocio.
- 401 para usuario no autenticado.
- 403 para usuario sin permisos.
- 404 para recurso inexistente.
- 409 para conflictos.
- 422 para validación de esquema.
- 500 para errores internos no controlados.

Las respuestas deben ser predecibles para que el frontend pueda manejarlas correctamente.

## 19. Reglas para agentes al modificar código

El agente debe:

- Leer primero los documentos de `docs/` y el change activo.
- Mantener cambios pequeños y enfocados.
- Respetar la arquitectura definida.
- No mover archivos sin necesidad.
- No cambiar nombres públicos sin justificarlo en OpenSpec.
- No introducir dependencias nuevas sin motivo técnico claro.
- No mezclar refactors grandes con features.
- No inventar endpoints fuera de la especificación.
- Actualizar documentación si el cambio modifica comportamiento.
- Marcar tareas en `tasks.md` solo después de verificar.

El agente no debe:

- Implementar directamente desde una idea no especificada.
- Saltarse servicios y escribir lógica en rutas.
- Consultar la base directamente desde componentes React.
- Duplicar tipos entre frontend y backend sin necesidad.
- Cambiar el stack principal del proyecto.
- Ignorar soft delete, auditoría o RBAC.
- Commitear `.env`, `node_modules`, `.venv`, builds o logs.

## 20. Subagentes sugeridos

Cuando se use un orquestador con subagentes, se recomienda separar responsabilidades así:

### `spec-agent`

Responsable de:

- Leer `docs/`.
- Crear o revisar proposals.
- Crear o revisar specs.
- Detectar conflictos con documentación existente.

No implementa código.

### `backend-agent`

Responsable de:

- FastAPI.
- SQLAlchemy.
- Alembic.
- Repositories.
- Unit of Work.
- Auth JWT/RBAC.
- Tests backend.

Debe respetar siempre el flujo:

```text
Route -> Service -> UoW -> Repository -> Model
```

### `frontend-agent`

Responsable de:

- React.
- TypeScript.
- Vite.
- Tailwind.
- Zustand.
- TanStack Query.
- FSD.

Debe respetar las capas:

```text
app -> pages -> features -> entities -> shared
```

### `database-agent`

Responsable de:

- Modelo relacional.
- Migraciones Alembic.
- Constraints.
- Seed data.
- Soft delete.
- Auditoría.

No debe modificar reglas de negocio sin validar contra specs.

### `qa-agent`

Responsable de:

- Tests.
- Verificación de endpoints.
- Validación de permisos.
- Build frontend.
- Revisión de tareas completadas.

No debe marcar tareas como completas si no puede justificar la verificación.

## 21. Prioridad de instrucciones

Cuando haya conflicto entre instrucciones, usar este orden:

1. Pedido explícito del usuario.
2. Specs activas en `openspec/changes/`.
3. Specs archivadas en `openspec/specs/`.
4. Documentos en `docs/`.
5. Este `AGENTS.md`.
6. Convenciones generales del framework o lenguaje.

Si el conflicto afecta arquitectura, seguridad o datos, el agente debe detenerse y pedir confirmación antes de implementar.

## 22. Estado actual del repositorio

El repositorio contiene la base documental y la estructura inicial del proyecto. Las carpetas `backend/` y `frontend/` pueden estar incompletas o vacías al inicio.

Por lo tanto, los agentes deben tratar este proyecto como una implementación progresiva guiada por OpenSpec, no como un sistema ya terminado.

Antes de crear código base, revisar el change activo:

```text
openspec/changes/sprint-0-infraestructura/
```

Este change define la infraestructura inicial y debe ser la referencia principal para Sprint 0.
