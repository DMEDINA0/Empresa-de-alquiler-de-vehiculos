from database.config import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class CategoriaVehiculo(Base):
    __tablename__ = "categoria_vehiculo"

    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    nombre_categoria = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)  # ✅ Explicitamente nullable

    vehiculos = relationship(
        "Vehiculo", back_populates="categoria"
    )  # ✅ Relación inversa esperada en Vehiculo

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
