## Why

El sistema funciona pero hay oportunidades de optimización: agregar índices compuestos faltantes en la BD y verificar que el frontend use code splitting correctamente.

## What Changes

- Índices compuestos en tablas grandes (pedidos, productos)
- Code splitting via lazy() ya implementado en rutas
- Eager loading con selectinload ya implementado
- Se verifica que no haya N+1 queries evidentes

## Impact

- Backend: Índices en modelos SQLAlchemy
- Frontend: Verificación de lazy loading
