# Tasks: sprint-7-notificaciones-email

## 1. Backend — Email Service

- [x] 1.1 Crear `backend/mail_service/` con `__init__.py`
- [x] 1.2 Crear `backend/mail_service/services/mail_service.py` con clase `MailService`
- [x] 1.3 Implementar `enviar(destinatario, asunto, cuerpo_html)` con SMTP + retry
- [x] 1.4 Implementar reintentos (3 intentos con backoff)
- [x] 1.5 Crear templates HTML en `backend/mail_service/templates/`:
  - `confirmacion-registro.html`
  - `cambio-estado-pedido.html`
  - `confirmacion-reembolso.html`

## 2. Integración con servicios existentes

- [ ] 2.1 Integrar email en registro (`auth/routes/auth.py`)
- [ ] 2.2 Integrar email en cambio de estado (`pedido_fsm_service.py`)
- [ ] 2.3 Integrar email en reembolso (`admin_pago_service.py`)

## 3. Configuración

- [x] 3.1 Agregar variables SMTP a `backend/core/config.py`

## 4. Verify

- [x] 4.1 Verificar tests backend pasan
