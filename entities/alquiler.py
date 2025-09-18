from database.config import Base
from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime


class Alquiler(Base):
    __tablename__ = "alquiler"

    id_alquiler = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False
    )
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime)
    horas = Column(
        Integer, nullable=False
    )  # ✅ Asegura que siempre se especifiquen las horas

    id_cliente = Column(
        UUID(as_uuid=True), ForeignKey("cliente.id_cliente"), nullable=False
    )  # ✅ Añade nullable=False
    id_vehiculo = Column(
        UUID(as_uuid=True), ForeignKey("vehiculo.id_vehiculo"), nullable=False
    )

    cliente = relationship(
        "Cliente", back_populates="alquileres"
    )  # ✅ Añade back_populates en Cliente
    vehiculo = relationship("Vehiculo", back_populates="alquileres")
    factura = relationship("Factura", back_populates="alquiler", uselist=False)

    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
