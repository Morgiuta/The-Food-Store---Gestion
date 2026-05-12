from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.core.database import Base


class UsuarioRol(Base):
    __tablename__ = "usuarios_roles"

    __table_args__ = (UniqueConstraint("usuario_id", "rol_id"),)

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    usuario = relationship("Usuario", back_populates="roles")
    rol = relationship("Rol", back_populates="usuarios")
