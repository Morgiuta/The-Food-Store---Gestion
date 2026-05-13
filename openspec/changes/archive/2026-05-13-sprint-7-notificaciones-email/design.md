## Context

Ya existe:
- `ConfiguracionRepository` con `get_by_clave` y `upsert` (para configurar emails desde admin)
- Sistema de configuración global en admin
- Eventos: registro de usuario, cambio de estado de pedido, reembolso

## Goals / Non-Goals

**Goals:**
- EmailService con envío asíncrono via SMTP
- Templates HTML: registro, cambio de estado, reembolso
- Cola de emails (procesar en background con asyncio.create_task)
- Reintentos para fallos transitorios (3 intentos)
- Logging de emails enviados
- Variables de entorno SMTP

**Non-Goals:**
- Proveedor específico (SendGrid, Resend, etc.) — usar SMTP estándar
- Notificaciones push/WhatsApp — solo email
- Dashboard de emails enviados — solo logs

## Decisions

### 1. SMTP estándar sobre SDK específico
**Decisión**: Usar `smtplib` y `email` de la stdlib de Python. Configurable via variables de entorno.

**Rationale**: No agrega dependencias externas. Compatible con cualquier proveedor SMTP (SendGrid, Mailgun, Gmail, etc.).

### 2. Templates HTML en archivos separados
**Decisión**: Templates HTML en `backend/email/templates/`. Usar formato string simple con `{placeholders}`.

**Rationale**: Sin dependencia de motor de templates. Fácil de modificar. Se reemplaza por Jinja2 si es necesario después.

### 3. Envío asíncrono con background task
**Decisión**: Usar `asyncio.create_task` para no bloquear la respuesta HTTP. El email se envía en background.

**Rationale**: No se necesita cola externa (Celery/RabbitMQ) para el volumen esperado.

## Templates

```
backend/email/templates/
├── confirmacion-registro.html    ← "¡Bienvenido a Food Store!"
├── cambio-estado-pedido.html     ← "Tu pedido #{id} ahora está {estado}"
└── confirmacion-reembolso.html   ← "Reembolso procesado por ${monto}"
```

## API / Integraciones

No se crean endpoints nuevos. El `EmailService` se integra con:

- `auth/routes/auth.py` → después de registro exitoso
- `pedido_fsm_service.py` → después de cambio de estado
- `admin_pago_service.py` → después de reembolso

## Risks / Mitigations

| Risk | Mitigation |
|------|------------|
| SMTP no configurado | EmailService detecta y loguea warning, no falla |
| Email tarda mucho | Background task, respuesta HTTP no bloquea |
| Fallo de envío | Retry 3 veces con backoff de 1s, loguea error |
