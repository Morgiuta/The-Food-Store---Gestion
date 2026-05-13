from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    accion = Column(String(20), nullable=False)  # CREATE, UPDATE, DELETE
    tabla = Column(String(50), nullable=False, index=True)
    registro_id = Column(Integer, nullable=True, index=True)
    valor_anterior = Column(Text, nullable=True)  # JSON
    valor_nuevo = Column(Text, nullable=True)     # JSON
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
