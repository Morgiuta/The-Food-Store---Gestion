# Design: sprint-3-direcciones-entrega

## Architecture

### Backend

**Dominio**: `backend/direcciones/`

```
backend/direcciones/
├── models/
│   └── direccion.py          # Modelo SQLModel DireccionEntrega
├── repositories/
│   └── direccion_repository.py  # DireccionRepository
├── routes/
│   └── direcciones.py        # Endpoints CRUD
├── schemas/
│   └── direccion.py          # Pydantic schemas
└── services/
    └── direccion_service.py # Lógica de negocio
```

**Modelo DireccionEntrega**:
- `id`: UUID primary key
- `usuario_id`: FK a usuario (ownership)
- `calle`: String (requerido)
- `numero`: String (requerido)
- `piso`: String (opcional)
- `departamento`: String (opcional)
- `ciudad`: String (requerido)
- `codigo_postal`: String (requerido)
- `referencia`: String (opcional)
- `es_predeterminada`: Boolean (default False)
- `created_at`: DateTime
- `updated_at`: DateTime
- `eliminado_en`: DateTime (soft delete)

**Endpoints**:
- `POST /api/v1/direcciones` — Crear dirección
- `GET /api/v1/direcciones` — Listar direcciones del usuario actual
- `GET /api/v1/direcciones/{id}` — Obtener una dirección específica
- `PUT /api/v1/direcciones/{id}` — Editar dirección
- `DELETE /api/v1/direcciones/{id}` — Soft delete
- `POST /api/v1/direcciones/{id}/predeterminada` — Marcar como predeterminada

### Frontend

**Estructura**:
```
frontend/src/features/direcciones/
├── hooks/
│   └── use-direcciones.ts    # TanStack Query hooks
├── components/
│   ├── address-card.tsx      # Mostrar dirección
│   ├── address-form.tsx      # Formulario crear/editar
│   └── address-list.tsx      # Lista de direcciones
└── pages/
    └── direcciones-page.tsx # Página principal
```

## Data Flow

1. **Crear dirección**:
   - Frontend → POST /direcciones
   - Backend: Si es la primera dirección del usuario → marcar predeterminada
   - Retornar dirección creada

2. **Marcar predeterminada**:
   - Frontend → POST /direcciones/{id}/predeterminada
   - Backend: Transaction - quitar predeterminada de todas las del usuario → poner en esta
   - Retornar dirección actualizada

3. **Obtener lista**:
   - Backend: Filtrar por usuario_id + eliminado_en IS NULL
   - Retornar lista con la predeterminada primero

## Security

- Ownership check: verificar que `direccion.usuario_id == current_user.id`
- No revelar existencia de direcciones ajenas (devolver 404, no 403)
- Validar que el usuario solo acceda a sus propias direcciones

## Edge Cases

1. **Primera dirección** → automáticamente predeterminada
2. **Cambiar predeterminada** → la anterior pierde el flag
3. **Eliminar dirección predeterminada** → crear nueva predeterminada o dejar sin predeterminada
4. **Usuario sin direcciones** → retornar lista vacía
5. **Dirección no existente** → 404

## Testing Strategy

- Unit tests: DireccionService, DireccionRepository
- Integration tests: CRUD endpoints con auth
- Frontend: компонент tests, integration con mock