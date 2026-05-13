## Why

El sistema no envía ningún tipo de notificación por email. Los usuarios no reciben confirmación de registro, ni notificaciones cuando cambia el estado de su pedido, ni confirmación de reembolsos. Sin emails transaccionales, la experiencia del usuario es incompleta.

## What Changes

- Servicio de email asíncrono usando SMTP (configurable)
- Template de email para confirmación de registro
- Template de email para cambio de estado de pedido
- Template de email para confirmación de reembolso
- Cola de emails en background (tarea asíncrona con asyncio)
- Logging de emails enviados
- Variables de entorno para configuración SMTP

## Capabilities

### New Capabilities
- `email-notifications`: Servicio de notificaciones por email con templates HTML, envío asíncrono, reintentos y logging.

### Modified Capabilities
- *(ninguna)*

## Impact

- **Backend**: Nuevo `EmailService` y templates HTML. Integración con servicios existentes (auth, pedidos, pagos).
- **Dependencias**: `aiofiles` para leer templates. SMTP estándar (no requiere SDK externo).
- **Variables de entorno**: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`.
