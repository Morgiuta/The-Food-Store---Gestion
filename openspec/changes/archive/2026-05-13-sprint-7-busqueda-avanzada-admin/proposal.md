## Why

El admin ya tiene endpoints con búsqueda pero falta una barra de búsqueda global y navegación rápida entre secciones. El admin también tiene páginas (pagos, configuración, auditoría) que no aparecen en el sidebar.

## What Changes

- Barra de búsqueda global en el header del admin
- Sidebar actualizado con links faltantes (pagos, configuración, auditoría)
- Búsqueda por ID en endpoint de pedidos admin

## Impact

- Frontend: AdminSearchBar + actualización de sidebar
- Backend: search param en listar_pedidos_admin
