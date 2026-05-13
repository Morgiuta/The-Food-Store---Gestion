## Why

El proyecto no tiene tests end-to-end automatizados. Configurar Playwright permite verificar el flujo completo (registro → login → catálogo → carrito → checkout) de forma automatizada.

## What Changes

- Playwright config en frontend/
- Test E2E básico de health check
- Script npm test:e2e

## Impact

- Frontend: playwright.config.ts, tests/e2e/ directorio
