from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.core.database import Base


class HistorialEstadoPedido(Base):
    __tablename__ = "historial_estados_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    estado_anterior_id = Column(Integer, ForeignKey("estados_pedido.id"), nullable=True)
    estado_nuevo_id = Column(Integer, ForeignKey("estados_pedido.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    observacion = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    pedido = relationship("Pedido", back_populates="historial_estados")
    estado_anterior = relationship("EstadoPedido", foreign_keys=[estado_anterior_id])
    estado_nuevo = relationship("EstadoPedido", foreign_keys=[estado_nuevo_id])
    usuario = relationship("Usuario")
