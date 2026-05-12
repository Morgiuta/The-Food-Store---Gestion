from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock_cantidad = Column(Integer, default=0)
    disponible = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    eliminado_en = Column(DateTime(timezone=True), nullable=True, index=True)

    categorias = relationship("ProductoCategoria", back_populates="producto", cascade="all, delete-orphan")
    ingredientes = relationship("ProductoIngrediente", back_populates="producto", cascade="all, delete-orphan")
