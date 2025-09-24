"""
Entidad que representa una factura generada por un alquiler.

Incluye fecha de emisión, monto total, relación con el alquiler y datos de auditoría.
"""

from database.config import Base
from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Factura(Base):
    __tablename__ = "factura"

    id_factura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    fecha_emision = Column(DateTime, nullable=False)
    monto_total = Column(Integer, nullable=False)
    id_alquiler = Column(UUID(as_uuid=True), ForeignKey("alquiler.id_alquiler"))

    alquiler = relationship("Alquiler", back_populates="factura")

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
