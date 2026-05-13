## Why

La especificación ERD v5 indica que `UsuarioRol` debe incluir `asignado_por_id` para registrar qué usuario/admin asignó el rol. Sin este campo, no hay trazabilidad sobre quién otorgó los permisos.

## What Changes

- Agregar campo `asignado_por_id` (FK a usuarios.id, nullable) en modelo UsuarioRol
- El campo es nullable para mantener compatibilidad con roles asignados antes de este cambio

## Impact

- Modelo: `auth/models/usuario_rol.py`
