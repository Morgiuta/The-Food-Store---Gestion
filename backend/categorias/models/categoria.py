from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String, nullable=True)
    padre_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    eliminado_en = Column(DateTime(timezone=True), nullable=True, index=True)

    padre = relationship("Categoria", remote_side="Categoria.id", back_populates="subcategorias")
    subcategorias = relationship("Categoria", back_populates="padre", cascade="all, delete-orphan")
    productos = relationship("ProductoCategoria", back_populates="categoria", cascade="all, delete-orphan")
