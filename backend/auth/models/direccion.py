from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.core.database import Base


class DireccionEntrega(Base):
    __tablename__ = "direcciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    calle = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    piso = Column(String, nullable=True)
    departamento = Column(String, nullable=True)
    ciudad = Column(String, nullable=False)
    codigo_postal = Column(String, nullable=False)
    referencia = Column(Text, nullable=True)
    es_predeterminada = Column(Boolean, default=False)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    eliminado_en = Column(DateTime(timezone=True), nullable=True, index=True)

    usuario = relationship("Usuario", back_populates="direcciones")
