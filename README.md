# Food Store — Sistema de Gestión de e-commerce

Sistema de e-commerce de productos alimenticios con gestión de pedidos, pagos y administración. Desarrollado con **Spec-Driven Development (SDD)** usando OPSX y Claude Code.

---

## Documentación del Sistema

Antes de escribir una línea de código, leé los tres documentos en `docs/`:

| Archivo | Contenido |
|---------|-----------|
| `docs/Descripcion.txt` | Visión general, actores del sistema y stack tecnológico |
| `docs/Integrador.txt` | Arquitectura en capas, ERD, API REST y patrones de diseño |
| `docs/Historias_de_usuario.txt` | US-000 a US-076 con criterios de aceptación y reglas de negocio |

Estos documentos son la fuente de verdad del sistema. El agente los lee antes de cada propuesta.

---

## Stack Tecnológico

**Backend**
- Framework: FastAPI
- ORM: SQLAlchemy + SQLModel
- Base de Datos: PostgreSQL 15+
- Autenticación: JWT + bcrypt
- Pagos: MercadoPago SDK
- Validación: Pydantic
- Rate Limiting: slowapi
- Migraciones: Alembic

**Frontend**
- Framework: React 18+ con TypeScript
- Build Tool: Vite
- State Management: Zustand
- Data Fetching: TanStack Query (React Query)
- Forms: TanStack Form
- Styling: Tailwind CSS
- HTTP Client: Axios
- Gráficos: Recharts
- UI Components: Radix UI / Headless UI

**DevOps & Infrastructure**
- Containerización: Docker + Docker Compose
- Base de Datos: PostgreSQL 15
- Admin DB: pgAdmin
- Orquestación: Docker Compose (desarrollo)

---

## Estructura del Proyecto

```
The-Food-Store---Gestion/
├── backend/                          # Backend FastAPI
│   ├── auth/                        # Autenticación y autorización
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── repositories/
│   ├── usuarios/                    # Gestión de usuarios
│   ├── productos/                   # Catálogo de productos
│   ├── categorias/                  # Categorías de productos
│   ├── ingredientes/                # Ingredientes y alérgenos
│   ├── pedidos/                     # Gestión de pedidos
│   ├── pagos/                       # Integración con MercadoPago
│   ├── admin/                       # Panel de administración
│   ├── .env.example                 # Variables de entorno (template)
│   ├── requirements.txt             # Dependencias Python
│   └── main.py                      # Punto de entrada
│
├── frontend/                         # Frontend React + TypeScript
│   ├── app/                         # Capa de aplicación
│   │   ├── layouts/                # Layouts globales
│   │   ├── providers/              # Providers (React Query, Zustand, etc)
│   │   └── store/                  # Store global
│   ├── pages/                       # Páginas (rutas)
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── productos/
│   │   └── admin/
│   ├── features/                    # Features (módulos de negocio)
│   │   ├── auth/
│   │   ├── usuarios/
│   │   ├── productos/
│   │   ├── cart/
│   │   └── pedidos/
│   ├── entities/                    # Entidades de dominio
│   │   ├── user/
│   │   ├── producto/
│   │   ├── category/
│   │   ├── ingrediente/
│   │   └── pedido/
│   ├── shared/                      # Código compartido
│   │   ├── ui/                     # Componentes reutilizables
│   │   ├── lib/                    # Utilidades y helpers
│   │   ├── types/                  # Tipos TypeScript globales
│   │   ├── api/                    # Cliente HTTP
│   │   ├── constants/              # Constantes globales
│   │   └── hooks/                  # Custom hooks
│   ├── .env.example
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                             # Documentación del sistema
│   ├── Descripcion.txt              # Descripción general
│   ├── Integrador.txt               # Arquitectura e integración
│   └── Historias_de_usuario.txt     # User stories
│
├── openspec/                         # Artefactos OPSX (generado por openspec init)
│   ├── changes/
│   ├── specs/
│   ├── config.yml
│   └── ...
│
├── docker-compose.yml                # Servicios (PostgreSQL + pgAdmin)
├── .gitignore
├── README.md
└── AGENTS.md                         # Instrucciones para agentes
```

---

## Setup del Entorno de Desarrollo

### Requisitos Previos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (o Docker)
- Git
- OpenSpec CLI: `npm install -g @fission-ai/openspec`

### 1. Clonar e Inicializar

```bash
git clone <url-del-repo>
cd The-Food-Store---Gestion
git checkout -b feature/setup-infraestructura
```

### 2. Iniciar Base de Datos con Docker

```bash
docker-compose up -d

# Verificar que PostgreSQL esté corriendo
# pgAdmin disponible en: http://localhost:5050
# Usuario: admin@admin.com / admin
```

### 3. Backend - FastAPI

```bash
cd backend

# Copiar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Seed de datos (opcional)
python -m app.db.seed

# Iniciar servidor
uvicorn app.main:app --reload
```

**API disponible en**: `http://localhost:8000`  
**Documentación Swagger**: `http://localhost:8000/docs`  
**ReDoc**: `http://localhost:8000/redoc`

### 4. Frontend - React + Vite

```bash
cd frontend

# Copiar variables de entorno
cp .env.example .env
# Editar VITE_API_URL si es necesario

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

**App disponible en**: `http://localhost:5173`

---

## Variables de Entorno

### Backend (.env)

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/foodstore

# Seguridad
SECRET_KEY=tu-clave-secreta-de-64-caracteres-minimo
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# MercadoPago (TEST)
MP_ACCESS_TOKEN=TEST-tu-token-de-mercadopago
MP_PUBLIC_KEY=TEST-tu-public-key-de-mercadopago

# CORS
CORS_ORIGINS=http://localhost:5173

# Environment
ENVIRONMENT=development
DEBUG=True
```

### Frontend (.env)

```env
# API Backend
VITE_API_URL=http://localhost:8000

# MercadoPago (TEST)
VITE_MP_PUBLIC_KEY=TEST-tu-public-key-de-mercadopago

# App
VITE_APP_NAME=Food Store
```

---

## Flujo de Desarrollo con OPSX

Todo cambio al sistema sigue este ciclo:

```
/opsx:explore   →  pensar antes de comprometerse (opcional)
/opsx:propose   →  generar propuesta + diseño + tareas
/opsx:apply     →  implementar tarea por tarea
/opsx:archive   →  sincronizar specs y cerrar el change
```

### Orden de Implementación (Roadmap)

```
sprint-0-infraestructura
├── us-000-setup              ← estructura base (Phase 1: DONE)
├── us-001-auth               ← JWT + RBAC + refresh tokens
├── us-002-categorias         ← catálogo jerárquico
├── us-003-productos          ← CRUD + stock + ingredientes
├── us-004-carrito            ← estado client-side (Zustand)
├── us-005-pedidos            ← UoW + FSM + audit trail
├── us-006-pagos-mercadopago  ← checkout + webhooks IPN
├── us-007-admin              ← panel + métricas
└── us-008-direcciones        ← direcciones de entrega
```

---

## Comandos Útiles

### Backend

```bash
# Migraciones Alembic
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head
alembic downgrade -1

# Testing
pytest
pytest --cov

# Type checking
mypy app/
```

### Frontend

```bash
# Desarrollo
npm run dev

# Build
npm run build

# Testing
npm run test

# Linting
npm run lint
```

### Docker

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Limpiar volúmenes
docker-compose down -v
```

---

## Convenciones de Commits

```
feat(modulo): descripción del cambio nuevo
fix(modulo): descripción del bug corregido
refactor(modulo): descripción del refactor
test(modulo): descripción de los tests
docs(modulo): descripción del cambio en docs
chore(modulo): cambios en configuración o dependencias
```

### Ejemplo

```
feat(auth): agregar endpoint de refresh token
fix(productos): corregir cálculo de precio con descuento
refactor(pedidos): extraer lógica de validación a servicio
```

---

## Arquitectura

### Patrón Backend: Feature-First + Repository Pattern

Cada feature (auth, usuarios, productos, etc.) encapsula:
- **models/**: Modelos SQLAlchemy
- **schemas/**: Esquemas Pydantic (validación)
- **routes/**: Endpoints FastAPI
- **services/**: Lógica de negocio
- **repositories/**: Acceso a datos

### Patrón Frontend: Feature-Sliced Design (FSD)

- **app/**: Capa de aplicación (providers, store, layouts)
- **pages/**: Componentes de página / rutas
- **features/**: Módulos de negocio independientes
- **entities/**: Tipos y componentes de dominio
- **shared/**: Código compartido (UI, hooks, utilidades)

---

## Contacto & Soporte

Para reportar issues o contribuir, abrí un PR o contactá al equipo.

**Repositorio**: [GitHub URL]  
**Documentación Técnica**: `docs/`  
**Especificaciones**: `openspec/`
