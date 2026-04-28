# AGENTS.md

## Propósito del proyecto

Sistema de gestión para The Food Store, con backend FastAPI y frontend React.

## Regla principal

Antes de modificar código, revisar la documentación del proyecto y respetar la arquitectura existente.

## Arquitectura general

- Backend: FastAPI, SQLAlchemy, Repository Pattern, Unit of Work.
- Frontend: React, TypeScript, Vite, estructura modular.
- Documentación: OpenSpec / OPSX para cambios funcionales.
- Seguridad: JWT y roles.
- Pagos: integración con MercadoPago.

## Flujo de trabajo obligatorio

1. Entender el cambio solicitado.
2. Revisar documentación relacionada.
3. Determinar si requiere OpenSpec.
4. Modificar solo los archivos necesarios.
5. Mantener la arquitectura existente.
6. Ejecutar o indicar pruebas relevantes.

## Skills disponibles

- Backend API: `skills/backend-api.md`
- Frontend UI: `skills/frontend-ui.md`

## Reglas generales

- No romper compatibilidad con código existente.
- No duplicar lógica de negocio.
- No mezclar responsabilidades.
- No hardcodear valores sensibles.
- No cambiar nombres de archivos, carpetas o endpoints sin motivo fuerte.
- Preferir cambios pequeños y trazables.