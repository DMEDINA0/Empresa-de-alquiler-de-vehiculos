"""
Modelo que representa a un cliente del sistema de alquiler.

Incluye datos personales y relación con sus alquileres.
"""

from database.config import Base
from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    primer_nombre = Column(String, nullable=False)
    segundo_nombre = Column(String)
    primer_apellido = Column(String, nullable=False)
    segundo_apellido = Column(String)
    fecha_nacimiento = Column(Date, nullable=False)

    alquileres = relationship("Alquiler", back_populates="cliente")
