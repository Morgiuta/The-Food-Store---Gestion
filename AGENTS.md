# AGENTS.md

## Propósito de este archivo

Este archivo define cómo deben trabajar los agentes dentro del proyecto **The Food Store — Gestión**. Su función es orientar a cualquier agente de código para que respete la arquitectura existente, use los skills correctos, consulte la documentación antes de modificar archivos y maneje los MCP de forma segura.

El objetivo principal no es solo generar código, sino mantener la coherencia técnica del sistema, evitar cambios innecesarios y asegurar que cada modificación siga las reglas de negocio ya definidas en la documentación del proyecto.

---

## Descripción ampliada del proyecto

**The Food Store — Gestión** es un sistema de gestión y e-commerce para la venta de productos alimenticios. El sistema está pensado para cubrir tanto la experiencia del cliente como la operación interna de la tienda.

Desde el lado del cliente, la plataforma permite navegar un catálogo de productos, ver categorías, consultar ingredientes y alérgenos, gestionar un carrito de compras, cargar direcciones de entrega, crear pedidos y realizar pagos seguros mediante MercadoPago. El carrito se maneja del lado del frontend, persistiendo en el navegador mediante Zustand y `localStorage`, mientras que los pedidos se consolidan en el backend cuando el usuario confirma la compra.

Desde el lado administrativo, el sistema permite gestionar usuarios, roles, productos, categorías, ingredientes, stock, pedidos, pagos y métricas operativas. La administración se apoya en un modelo de roles: `ADMIN`, `STOCK`, `PEDIDOS` y `CLIENT`, con permisos diferenciados para evitar que cada perfil acceda a funcionalidades que no le corresponden.

El backend está construido con **FastAPI**, **SQLAlchemy / SQLModel**, **Pydantic**, **PostgreSQL**, **JWT**, **bcrypt**, **Alembic** y patrones como **Repository Pattern** y **Unit of Work**. La lógica de negocio debe quedar en services, el acceso a datos en repositories, los modelos en models, los schemas en schemas y los endpoints en routes. Los routers no deben contener lógica de negocio pesada ni acceder directamente a la base de datos.

El frontend está construido con **React**, **TypeScript**, **Vite**, **Tailwind CSS**, **Zustand**, **TanStack Query**, **TanStack Form**, **Axios** y componentes reutilizables. Su estructura separa `app`, `pages`, `features`, `entities` y `shared`, siguiendo una arquitectura modular orientada a mantener bajo acoplamiento entre pantallas, lógica de negocio, cliente HTTP y componentes visuales.

El proyecto usa un enfoque de **Spec-Driven Development** mediante documentación en `docs/` y cambios planificados en `openspec/`. Antes de implementar funcionalidades nuevas, el agente debe verificar si corresponde crear o actualizar una especificación de cambio.

---

## Fuentes de verdad del proyecto

Antes de modificar código, revisar estos archivos según corresponda:

1. `README.md`  
   Visión general del proyecto, stack, estructura y setup.

2. `docs/Descripcion.txt`  
   Descripción integral del sistema, actores, dominios, modelo de datos y reglas generales.

3. `docs/Integrador.txt`  
   Arquitectura técnica, patrones, integración entre capas, ERD y criterios de implementación.

4. `docs/Historias_de_usuario.txt`  
   Historias de usuario, reglas de negocio, criterios de aceptación y prioridades.

5. `docs/CHANGES.md`  
   Registro de cambios y evolución del proyecto.

6. `food-store-change-map.md`  
   Mapa de sprints, changes, dependencias y planificación funcional.

7. `openspec/`  
   Carpeta para cambios funcionales gestionados mediante OpenSpec / OPSX.

Si hay contradicción entre documentos, priorizar en este orden:

1. Reglas explícitas del usuario.
2. `docs/Historias_de_usuario.txt`.
3. `docs/Integrador.txt`.
4. `docs/Descripcion.txt`.
5. `README.md`.
6. Implementación existente.

---

## Arquitectura general

### Backend

Ruta base:

```txt
backend/
```

Tecnologías principales:

- FastAPI.
- SQLAlchemy / SQLModel.
- PostgreSQL.
- Pydantic.
- Alembic.
- JWT + bcrypt.
- MercadoPago SDK.
- Repository Pattern.
- Unit of Work.

Estructura esperada por dominio:

```txt
backend/<dominio>/
├── models/
├── repositories/
├── routes/
├── schemas/
└── services/
```

Dominios actuales:

```txt
backend/auth/
backend/usuarios/
backend/productos/
backend/categorias/
backend/ingredientes/
backend/pedidos/
backend/pagos/
backend/admin/
```

Rutas transversales:

```txt
backend/core/
backend/middleware/
backend/api/v1/routes/
```

Reglas para backend:

- Los routers solo coordinan request, response, dependencias y códigos HTTP.
- La lógica de negocio vive en services.
- El acceso a base de datos vive en repositories.
- Las operaciones transaccionales deben usar Unit of Work.
- No acceder directamente a la base desde routes.
- No duplicar lógica de negocio entre services.
- No almacenar contraseñas en texto plano.
- No devolver datos sensibles en respuestas.
- Mantener JWT, roles y ownership checks donde corresponda.
- Usar tipos seguros para dinero: `NUMERIC`, `Decimal` o equivalente. No usar float para precios.
- Respetar soft delete cuando la entidad lo requiera.
- Registrar cambios de estado de pedido en historial append-only.

---

### Frontend

Ruta base:

```txt
frontend/
```

Tecnologías principales:

- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- Zustand.
- TanStack Query.
- TanStack Form.
- Axios.
- Radix UI / Headless UI.
- Recharts.

Estructura principal:

```txt
frontend/
├── app/
│   ├── layouts/
│   ├── providers/
│   └── store/
├── pages/
├── features/
├── entities/
└── shared/
    ├── api/
    ├── constants/
    ├── hooks/
    ├── types/
    └── ui/
```

Reglas para frontend:

- No mezclar llamadas HTTP dentro de componentes puramente visuales.
- Centralizar llamadas HTTP en `shared/api/` o services específicos.
- Usar hooks cuando haya lógica reutilizable.
- Usar componentes de `shared/ui/` cuando sean reutilizables.
- No duplicar componentes si ya existe uno equivalente.
- Mantener tipado TypeScript estricto.
- Mantener estilos consistentes con Tailwind.
- No hardcodear URLs de API: usar variables de entorno.
- Respetar permisos de usuario también en la UI, pero no confiar solo en la UI para seguridad.

---

## Skills disponibles

Los skills son archivos de instrucciones específicas. Antes de tocar una parte del sistema, el agente debe revisar el skill correspondiente.

### Skills locales actuales

#### Backend API

Ruta:

```txt
skills/backend-api.md
```

Usar cuando el cambio afecte:

- FastAPI.
- Rutas del backend.
- Schemas Pydantic.
- Services.
- Repositories.
- Modelos SQLAlchemy / SQLModel.
- Unit of Work.
- Autenticación, autorización, JWT o roles.
- Pedidos, pagos, stock o MercadoPago.

Regla principal:

> El backend debe mantener separación entre routes, services, repositories, schemas y models. Los routers no deben contener lógica de negocio ni queries directas.

---

#### Frontend UI

Ruta:

```txt
skills/frontend-ui.md
```

Usar cuando el cambio afecte:

- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- Componentes visuales.
- Páginas.
- Features.
- Entities.
- Hooks.
- Stores Zustand.
- Cliente HTTP del frontend.

Regla principal:

> La UI debe mantenerse modular. La lógica de API no debe mezclarse dentro de componentes visuales si puede separarse en services, hooks o stores.

---

### Skills nuevos referenciados por lockfile

El archivo:

```txt
skills/skills-lock.json
```

registra skills externos fijados por hash. Estos skills pueden no estar materializados todavía como carpetas locales, pero sus rutas esperadas son:

#### Frontend Design

Ruta esperada:

```txt
skills/frontend-design/SKILL.md
```

Origen registrado:

```txt
anthropics/skills
```

Usar cuando el cambio afecte:

- Diseño visual.
- Layouts.
- UX.
- Jerarquía visual.
- Accesibilidad.
- Consistencia de componentes.
- Pantallas administrativas.
- Diseño del catálogo, carrito, checkout o dashboard.

Regla de uso:

> Si este skill está instalado localmente, leerlo antes de rediseñar pantallas o componentes. Si no está instalado, no inventar reglas internas: aplicar las reglas locales de `skills/frontend-ui.md` y mantener consistencia con el diseño existente.

---

#### Vercel React Best Practices

Ruta esperada:

```txt
skills/react-best-practices/SKILL.md
```

Origen registrado:

```txt
vercel-labs/agent-skills
```

Usar cuando el cambio afecte:

- Buenas prácticas React.
- Estructura de componentes.
- Performance.
- Hooks.
- Separación server/client si aplica.
- Manejo de estado.
- Data fetching.
- Reutilización de lógica.

Regla de uso:

> Si este skill está instalado localmente, leerlo antes de hacer refactors grandes en React. Si no está instalado, seguir la arquitectura existente del proyecto y evitar reestructuraciones innecesarias.

---

## Cómo elegir skills

Antes de modificar archivos, decidir qué skill aplica:

| Tipo de cambio | Skill obligatorio |
|---|---|
| Endpoint, schema, service, repository o modelo backend | `skills/backend-api.md` |
| Autenticación, JWT, roles o permisos | `skills/backend-api.md` |
| Pedido, pago, stock, MercadoPago o FSM | `skills/backend-api.md` |
| Página, componente, hook, store o cliente HTTP frontend | `skills/frontend-ui.md` |
| Diseño visual, layout, UX o accesibilidad | `skills/frontend-ui.md` y, si existe, `skills/frontend-design/SKILL.md` |
| Refactor React importante | `skills/frontend-ui.md` y, si existe, `skills/react-best-practices/SKILL.md` |
| Cambio full-stack | Primero `skills/backend-api.md`, luego `skills/frontend-ui.md` |
| Cambio funcional grande | Revisar `openspec/` y documentación antes de codificar |

Si un cambio afecta varias capas, usar todos los skills relevantes. No elegir un solo skill si el cambio es full-stack.

---

## Manejo de MCP

La configuración de MCP está en:

```txt
opencode.json
```

Configuración actual detectada:

```json
{
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/francisco/git/UTN/grupo8/robledo/The-Food-Store---Gestioncopy/The-Food-Store---Gestion"
      ]
    },
    "postgres": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/francisco/git/UTN/grupo8/robledo/The-Food-Store---Gestioncopy/The-Food-Store---Gestion"
      ]
    }
  }
}
```

### MCP `filesystem`

Uso previsto:

- Leer archivos del proyecto.
- Buscar código existente.
- Inspeccionar documentación.
- Modificar archivos cuando el usuario lo pida.
- Verificar estructura de carpetas.

Reglas:

- Usar filesystem para inspeccionar antes de editar.
- No crear archivos fuera del proyecto.
- No modificar `.env`, secretos, claves, tokens ni credenciales.
- No tocar `.git/` salvo que el usuario lo pida explícitamente.
- No hacer cambios masivos si el usuario pidió un cambio puntual.
- Antes de crear un archivo nuevo, verificar si ya existe una ubicación equivalente.

---

### MCP `postgres`

Estado actual:

> El MCP llamado `postgres` está configurado con el mismo servidor que `filesystem`. Por lo tanto, con la configuración actual NO debe asumirse que existe acceso real a PostgreSQL mediante ese MCP.

Reglas:

- No usar `postgres` como si fuera una conexión real a base de datos mientras siga apuntando a `@modelcontextprotocol/server-filesystem`.
- Si se necesita consultar la base, primero verificar que exista un MCP PostgreSQL real configurado.
- No inventar resultados de queries.
- Si no hay MCP PostgreSQL real, trabajar con migraciones, modelos, documentación o scripts existentes.
- Para cambios de datos, preferir migraciones Alembic, seed scripts o instrucciones SQL revisables.

Configuración esperada si más adelante se agrega un MCP PostgreSQL real:

```json
{
  "mcp": {
    "postgres": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://USER:PASSWORD@HOST:PORT/DATABASE"
      ]
    }
  }
}
```

La URL de conexión nunca debe hardcodearse con credenciales reales dentro del repositorio. Usar variables de entorno o configuración local no versionada.

---

## Flujo obligatorio de trabajo

Para cualquier cambio:

1. Entender el pedido del usuario.
2. Revisar documentación relacionada en `docs/`.
3. Revisar el skill correspondiente en `skills/`.
4. Inspeccionar archivos existentes antes de crear archivos nuevos.
5. Determinar si el cambio requiere OpenSpec / OPSX.
6. Hacer el cambio mínimo necesario.
7. Mantener la arquitectura existente.
8. Verificar imports, rutas, tipos y nombres.
9. Ejecutar pruebas si existen o indicar qué pruebas deberían ejecutarse.
10. Resumir qué se cambió y por qué.

---

## Cuándo usar OpenSpec / OPSX

Usar `openspec/` cuando el cambio sea funcionalmente relevante, por ejemplo:

- Nueva funcionalidad.
- Nuevo endpoint.
- Nueva entidad o tabla.
- Cambio en reglas de negocio.
- Cambio en flujo de pedidos, pagos, stock o roles.
- Cambio que afecte historias de usuario existentes.
- Refactor grande que modifique arquitectura.

No hace falta OpenSpec para:

- Correcciones menores de estilo.
- Fixes pequeños y localizados.
- Ajustes de texto.
- Corrección de imports.
- Cambios puramente visuales sin cambio funcional.

Si hay dudas, revisar `food-store-change-map.md` y `docs/Historias_de_usuario.txt` antes de decidir.

---

## Reglas generales de código

- No romper compatibilidad con código existente.
- No cambiar nombres de archivos, carpetas, clases, funciones, endpoints o modelos sin motivo fuerte.
- No duplicar lógica.
- No mezclar responsabilidades.
- No hardcodear secretos, tokens, credenciales, URLs sensibles ni claves privadas.
- No modificar configuración global si el cambio puede resolverse localmente.
- No borrar documentación ni comentarios útiles.
- No introducir dependencias nuevas sin justificar su necesidad.
- No hacer refactors grandes dentro de una tarea pequeña.
- Mantener cambios pequeños, trazables y reversibles.

---

## Reglas de seguridad

- Nunca commitear `.env` reales.
- Nunca exponer contraseñas, tokens JWT, refresh tokens o claves de MercadoPago.
- Las contraseñas deben hashearse con bcrypt.
- El servidor nunca debe procesar datos sensibles de tarjetas.
- Validar ownership en recursos de cliente.
- Validar roles en endpoints protegidos.
- Devolver 401 cuando falta autenticación válida.
- Devolver 403 cuando el usuario autenticado no tiene permisos.
- No revelar información sensible en mensajes de error.

---

## Reglas específicas de dominio

### Usuarios y roles

- Roles fijos: `ADMIN`, `STOCK`, `PEDIDOS`, `CLIENT`.
- Un usuario puede tener múltiples roles.
- Solo `ADMIN` puede administrar roles.
- No permitir que el último admin pierda el rol `ADMIN`.

### Catálogo

- Categorías jerárquicas con `padre_id` autoreferencial.
- Evitar ciclos en categorías.
- Productos pueden tener múltiples categorías.
- Productos pueden tener múltiples ingredientes.
- Ingredientes pueden marcarse como alérgenos.
- El catálogo público solo muestra productos disponibles y no eliminados.

### Carrito

- El carrito es client-side only.
- Persistencia mediante Zustand + `localStorage`.
- No crear backend de carrito salvo cambio explícito de requerimiento.

### Pedidos

- La creación de pedido debe ser atómica.
- Validar stock dentro de la transacción.
- Usar snapshot de precio y dirección.
- Todo pedido nace en estado `PENDIENTE`.
- Los cambios de estado deben respetar la FSM.
- Registrar historial append-only para cambios de estado.

### Pagos

- MercadoPago confirma pagos mediante webhooks.
- La transición `PENDIENTE` → `CONFIRMADO` debe ser automática por pago aprobado.
- Usar idempotency key para evitar doble procesamiento.
- No procesar datos sensibles de tarjeta en el servidor.

---

## Convenciones para commits y cambios

Cuando se proponga un cambio, mantenerlo claro y limitado.

Formato sugerido:

```txt
feat(auth): agregar login con JWT y refresh token
fix(productos): corregir validación de stock negativo
docs(agents): actualizar reglas de skills y MCP
refactor(frontend): separar lógica de API del componente de productos
```

Si el cambio corresponde a una historia o issue, referenciarlo cuando exista:

```txt
feat(pedidos): implementar creación atómica de pedido #12
```

---

## Checklist antes de finalizar una tarea

Antes de dar una tarea por terminada, verificar:

- [ ] Se revisó la documentación relevante.
- [ ] Se usó el skill correcto.
- [ ] Se respetó la estructura existente.
- [ ] No se agregaron secretos ni hardcodes sensibles.
- [ ] No se duplicó lógica.
- [ ] Los nombres respetan convenciones existentes.
- [ ] Los imports y rutas son correctos.
- [ ] El cambio es mínimo y trazable.
- [ ] Se indicaron o ejecutaron pruebas relevantes.
- [ ] Se explicó brevemente qué se cambió.

---

## Regla final

Si el agente no está seguro de una regla de negocio, no debe inventarla. Debe revisar primero `docs/Historias_de_usuario.txt`, `docs/Integrador.txt`, `docs/Descripcion.txt` y los archivos existentes. Si todavía no hay definición, debe proponer una solución mínima, explícita y consistente con la arquitectura actual.
