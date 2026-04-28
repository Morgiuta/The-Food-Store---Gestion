# skills/backend-api.md

## Alcance

Usar este skill cuando el cambio afecte al backend FastAPI.

## Reglas

- Respetar Repository Pattern.
- Usar Unit of Work cuando haya operaciones transaccionales.
- No acceder directamente a la base desde routers.
- Mantener validaciones en schemas o services según corresponda.
- Los routers solo deben coordinar request/response.
- La lógica de negocio debe estar en services.