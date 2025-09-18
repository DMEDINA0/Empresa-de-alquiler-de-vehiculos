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

    # Relación con CategoriaVehiculo
    id_categoria = Column(
        UUID(as_uuid=True),
        ForeignKey("categoria_vehiculo.id_categoria"),
        nullable=False,
    )
    categoria = relationship("CategoriaVehiculo", back_populates="vehiculos")

    # Relación con Alquiler (si existe)
    alquileres = relationship("Alquiler", back_populates="vehiculo")

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
