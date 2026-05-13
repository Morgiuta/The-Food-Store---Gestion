from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    __table_args__ = (
        Index("ix_pagos_pedido_creado", "pedido_id", "creado_en"),
    )

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    mp_payment_id = Column(String, nullable=True)
    mp_status = Column(String, nullable=True)
    external_reference = Column(String, nullable=True, index=True)
    idempotency_key = Column(String, nullable=True, unique=True, index=True)
    creado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    pedido = relationship("Pedido", back_populates="pagos")
