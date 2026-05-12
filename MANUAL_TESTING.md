# Guía de Pruebas Manuales — Food Store

Guía paso a paso para levantar el entorno y probar manualmente la aplicación.

---

## 1. Requisitos Previos

- **Docker Desktop** instalado y corriendo
- **Python 3.11+**
- **Node.js 18+**
- **Git**

---

## 2. Iniciar Base de Datos (PostgreSQL)

```bash
# Desde la raíz del proyecto
docker compose up -d

# Verificar que esté corriendo
docker compose ps
# Deberías ver: foodstore-db (healthy) y foodstore-pgadmin

# pgAdmin: http://localhost:5050
# Email: admin@foodstore.com / Password: admin
```

La base de datos `foodstore` se crea automáticamente con usuario `user` y password `password`.

---

## 3. Backend (FastAPI)

### 3.1 Instalar dependencias

```bash
cd backend

# Crear entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# O en Mac/Linux:
# python -m venv .venv
# source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3.2 Crear tablas y seed data

```bash
# Opción A: Usando Docker (recomendado, evita problemas de encoding en Windows)
docker exec -i foodstore-db psql -U user -d foodstore -f backend/seed.sql

# Nota: si no existe seed.sql, ejecutar el script Python:
cd backend
python seed.py
```

### 3.3 Iniciar servidor

```bash
cd backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Servidor disponible en:** http://localhost:8000  
**Swagger Docs:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

---

## 4. Frontend (React + Vite)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

**App disponible en:** http://localhost:5173

---

## 5. Flujo de Prueba Manual Completo

### 5.1 Probar endpoints públicos

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Obtener árbol de categorías (vacío inicialmente)
curl http://localhost:8000/api/v1/categorias

# Listar productos del catálogo (vacío inicialmente)
curl http://localhost:8000/api/v1/productos
```

### 5.2 Probar registro de cliente

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Cliente Test",
    "email": "cliente@test.com",
    "password": "password123"
  }'

# Deberías recibir: access_token, refresh_token y datos del usuario con rol CLIENT
```

Guardar el `access_token` y `refresh_token` de la respuesta.

### 5.3 Probar login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@test.com",
    "password": "password123"
  }'

# Deberías recibir el mismo formato que register
```

### 5.4 Probar refresh token

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "EL_REFRESH_TOKEN_QUE_RECIBISTE"
  }'

# Deberías recibir un nuevo par de tokens
```

### 5.5 Probar login como admin

El admin por defecto se crea con el seed:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@foodstore.com",
    "password": "Admin123!"
  }'

# Guardar el access_token (empieza con "eyJ...")
```

### 5.6 Probar gestión de usuarios (admin)

```bash
# Usar el token de admin en el header Authorization
TOKEN="eyJ..."

# Listar usuarios
curl http://localhost:8000/api/v1/admin/usuarios \
  -H "Authorization: Bearer $TOKEN"

# Ver detalle de usuario
curl http://localhost:8000/api/v1/admin/usuarios/1 \
  -H "Authorization: Bearer $TOKEN"

# Editar usuario
curl -X PUT http://localhost:8000/api/v1/admin/usuarios/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Admin Modificado"}'
```

### 5.7 Probar CRUD de categorías (admin)

```bash
# Crear categoría raíz
curl -X POST http://localhost:8000/api/v1/categorias \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Bebidas"}'

# Crear subcategoría (reemplazar ID_PADRE con el id de "Bebidas")
curl -X POST http://localhost:8000/api/v1/categorias \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Gaseosas", "padre_id": 1}'

# Ver árbol de categorías (público)
curl http://localhost:8000/api/v1/categorias
```

### 5.8 Probar CRUD de productos (admin)

```bash
# Crear producto con categoría
curl -X POST http://localhost:8000/api/v1/productos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Coca Cola 500ml",
    "precio": 150.00,
    "stock_cantidad": 100,
    "categoria_ids": [1]
  }'

# Ver catálogo público
curl http://localhost:8000/api/v1/productos

# Buscar productos
curl "http://localhost:8000/api/v1/productos/search?q=coca"

# Editar producto
curl -X PUT http://localhost:8000/api/v1/productos/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"precio": 180.00}'
```

### 5.9 Probar role-based access

```bash
# Login como cliente
TOKEN_CLIENT=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "cliente@test.com", "password": "password123"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Cliente intenta crear producto (debería dar 403)
curl -X POST http://localhost:8000/api/v1/productos \
  -H "Authorization: Bearer $TOKEN_CLIENT" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test", "precio": 10}'
# → 403 Forbidden

# Cliente ve su perfil (debería funcionar)
curl http://localhost:8000/api/v1/perfil \
  -H "Authorization: Bearer $TOKEN_CLIENT"
```

### 5.10 Probar rate limiting

```bash
# Intentar login 6 veces con credenciales inválidas
for i in $(seq 1 6); do
  echo "Intento $i:"
  curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "test@test.com", "password": "wrong"}'
  echo ""
done
# El 6to intento debería devolver 429 Too Many Requests
```

---

## 6. Probar con el Frontend (UI)

1. Abrir http://localhost:5173
2. **Sin autenticar**: Ver catálogo de productos, login, registro
3. **Registrarse**: Completar formulario → redirige al catálogo
4. **Login**: Email `admin@foodstore.com` / `Admin123!` → menú admin completo
5. **Admin**: Navegar a las secciones del panel:
   - Usuarios: listar, editar, activar/desactivar
   - Productos: crear, editar, eliminar
   - Categorías: crear árbol jerárquico
   - Ingredientes: crear con flag de alérgeno
6. **Cerrar sesión** → volver a vista pública
7. **Error 403**: Intentar acceder a `/admin` sin ser admin → redirige a página 403

---

## 7. Tests Automatizados

```bash
# Tests del backend (162 tests)
cd backend
pytest -v

# Tests del frontend (7 tests)
cd frontend
npm test

# TypeScript
cd frontend
npx tsc --noEmit
```

---

## 8. Solución de Problemas Comunes

| Problema | Solución |
|----------|----------|
| `psycopg2` error de encoding en Windows | Usar `docker exec` para consultas directas a la DB |
| Puerto 5432 ocupado | Detener otra instancia de PostgreSQL o cambiar puerto en docker-compose.yml |
| `alembic upgrade head` falla | Ejecutar las migraciones manualmente con docker exec psql |
| Frontend no conecta con backend | Verificar `VITE_API_URL` en `frontend/.env` |
| 401 en endpoints | El token expiró (30 min). Hacer refresh o login nuevamente |
| 403 en endpoints | El usuario no tiene el rol requerido. Usar admin@foodstore.com |
| pgAdmin no carga | Esperar unos segundos, a veces tarda en iniciar |
