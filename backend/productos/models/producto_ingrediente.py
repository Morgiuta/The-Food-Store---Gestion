from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.core.database import Base


class ProductoIngrediente(Base):
    __tablename__ = "productos_ingredientes"

    __table_args__ = (UniqueConstraint("producto_id", "ingrediente_id"),)

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    es_removible = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    producto = relationship("Producto", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="productos")
