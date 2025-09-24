"""
Modelo que representa un vehículo disponible para alquiler.

Incluye información como nombre, tarifa por hora, disponibilidad,
categoría asociada y datos de auditoría.
"""

from database.config import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Vehiculo(Base):
    __tablename__ = "vehiculo"

    id_vehiculo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    nombre = Column(String(100), nullable=False)
    tarifa_hora = Column(Integer, nullable=False)
    disponible = Column(Boolean, default=True)

    id_categoria = Column(
        UUID(as_uuid=True), ForeignKey("categoria_vehiculo.id_categoria"), nullable=True
    )
    categoria = relationship("CategoriaVehiculo", back_populates="vehiculos")

    alquileres = relationship("Alquiler", back_populates="vehiculo")

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
