from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, Text
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    __table_args__ = (
        Index("ix_pedidos_usuario_creado", "usuario_id", "creado_en"),
        Index("ix_pedidos_estado_creado", "estado_id", "creado_en"),
    )

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado_id = Column(Integer, ForeignKey("estados_pedido.id"), nullable=False)
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)
    forma_pago_id = Column(Integer, ForeignKey("formas_pago.id"), nullable=True)
    total = Column(Numeric(10, 2), nullable=False)
    costo_envio = Column(Numeric(10, 2), default=0)
    direccion_snapshot = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    eliminado_en = Column(DateTime(timezone=True), nullable=True, index=True)

    usuario = relationship("Usuario", back_populates="pedidos")
    estado = relationship("EstadoPedido", back_populates="pedidos")
    direccion = relationship("DireccionEntrega")
    forma_pago = relationship("FormaPago", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")
    historial_estados = relationship("HistorialEstadoPedido", back_populates="pedido", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="pedido", cascade="all, delete-orphan")
