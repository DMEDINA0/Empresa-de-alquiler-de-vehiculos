"""
Entidad que representa a un usuario del sistema.

Incluye datos personales, credenciales, rol, vínculo con cliente y auditoría.
"""

from database.config import Base
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    primer_nombre = Column(String(100), nullable=False)
    segundo_nombre = Column(String(100), nullable=False)
    primer_apellido = Column(String(100), nullable=False)
    segundo_apellido = Column(String(100), nullable=False)
    rol_usuario = Column(Text, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)

    es_admin = Column(Boolean, nullable=False, default=False)

    id_cliente = Column(
        UUID(as_uuid=True), ForeignKey("cliente.id_cliente"), nullable=True
    )
    cliente = relationship("Cliente", back_populates="usuario")

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
