"""
Async email service using SMTP. Supports HTML templates, retries, and background sending.
"""
import asyncio
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from backend.core.config import get_settings

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 1

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class MailService:
    """Service for sending email notifications asynchronously."""

    def __init__(self):
        self._settings = get_settings()

    def _is_configured(self) -> bool:
        return bool(self._settings.SMTP_HOST and self._settings.SMTP_PORT)

    def _load_template(self, template_name: str, **kwargs) -> str:
        template_path = TEMPLATES_DIR / template_name
        if not template_path.exists():
            logger.warning("Template no encontrado: %s", template_path)
            return self._fallback_template(template_name, **kwargs)
        content = template_path.read_text(encoding="utf-8")
        return content.format(**kwargs)

    def _fallback_template(self, template_name: str, **kwargs) -> str:
        if "registro" in template_name:
            return f"<h2>Bienvenido a Food Store, {kwargs.get('nombre', '')}!</h2>"
        elif "pedido" in template_name:
            return f"<h2>Pedido #{kwargs.get('pedido_id', '')}</h2><p>Estado: {kwargs.get('estado', '')}</p>"
        elif "reembolso" in template_name:
            return f"<h2>Reembolso procesado</h2><p>Monto: ${kwargs.get('monto', '')}</p>"
        return "<p>Notificacion de Food Store</p>"

    async def enviar(self, destinatario: str, asunto: str, cuerpo_html: str) -> bool:
        if not self._is_configured():
            logger.warning("SMTP no configurado. No se envio email a %s", destinatario)
            return False

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                loop = asyncio.get_event_loop()
                success = await loop.run_in_executor(None, self._send_sync, destinatario, asunto, cuerpo_html)
                if success:
                    logger.info("Email enviado a %s (asunto: %s)", destinatario, asunto)
                    return True
            except Exception as e:
                logger.warning("Intento %d/%d fallo: %s", attempt, MAX_RETRIES, str(e))
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(RETRY_DELAY * attempt)

        logger.error("No se pudo enviar email a %s tras %d intentos", destinatario, MAX_RETRIES)
        return False

    def _send_sync(self, destinatario: str, asunto: str, cuerpo_html: str) -> bool:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"] = self._settings.EMAIL_FROM
        msg["To"] = destinatario
        msg.attach(MIMEText("Notificacion de Food Store", "plain"))
        msg.attach(MIMEText(cuerpo_html, "html"))

        with smtplib.SMTP(self._settings.SMTP_HOST, self._settings.SMTP_PORT, timeout=10) as server:
            if self._settings.SMTP_USER:
                server.login(self._settings.SMTP_USER, self._settings.SMTP_PASSWORD)
            server.sendmail(self._settings.EMAIL_FROM, [destinatario], msg.as_string())
        return True

    async def notificar_registro(self, destinatario: str, nombre: str) -> bool:
        cuerpo = self._load_template("confirmacion-registro.html", nombre=nombre, destinatario=destinatario)
        return await self.enviar(destinatario, "Bienvenido a Food Store!", cuerpo)

    async def notificar_cambio_estado(self, destinatario: str, pedido_id: int, estado: str, nombre: str) -> bool:
        cuerpo = self._load_template("cambio-estado-pedido.html", pedido_id=pedido_id, estado=estado, nombre=nombre)
        return await self.enviar(destinatario, f"Pedido #{pedido_id} - {estado}", cuerpo)

    async def notificar_reembolso(self, destinatario: str, pedido_id: int, monto: str, nombre: str) -> bool:
        cuerpo = self._load_template("confirmacion-reembolso.html", pedido_id=pedido_id, monto=monto, nombre=nombre)
        return await self.enviar(destinatario, f"Reembolso procesado - Pedido #{pedido_id}", cuerpo)
