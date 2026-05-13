from datetime import datetime, timezone

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from backend.core.database import Base


class DetallePedido(Base):
    __tablename__ = "detalles_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=True)
    nombre_snapshot = Column(String(200), nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio_snapshot = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    personalizacion = Column(ARRAY(Integer), nullable=True)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto")
