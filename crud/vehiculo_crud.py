"""
Clase que implementa operaciones CRUD para la entidad Vehiculo.

Permite crear, consultar, actualizar, eliminar vehículos y gestionar su disponibilidad.
"""

from entities.vehiculo import Vehiculo
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime


class VehiculoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_vehiculo(
        self, nombre: str, tarifa_hora: int, id_categoria: str, id_usuario_creacion: str
    ) -> Vehiculo:
        nuevo_vehiculo = Vehiculo(
            id_vehiculo=uuid4(),
            nombre=nombre,
            tarifa_hora=tarifa_hora,
            disponible=True,
            id_categoria=id_categoria,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
        )
        self.db.add(nuevo_vehiculo)
        self.db.commit()
        self.db.refresh(nuevo_vehiculo)
        return nuevo_vehiculo

    def obtener_vehiculo_por_id(self, id_vehiculo: str) -> Optional[Vehiculo]:
        return self.db.query(Vehiculo).filter_by(id_vehiculo=id_vehiculo).first()

    def listar_vehiculos(self) -> List[Vehiculo]:
        return self.db.query(Vehiculo).all()

    def listar_vehiculos_disponibles(self) -> List[Vehiculo]:
        return self.db.query(Vehiculo).filter_by(disponible=True).all()

    def actualizar_vehiculo(
        self, id_vehiculo: str, nuevos_datos: dict
    ) -> Optional[Vehiculo]:
        vehiculo = self.obtener_vehiculo_por_id(id_vehiculo)
        if vehiculo:
            for key, value in nuevos_datos.items():
                if hasattr(vehiculo, key):
                    setattr(vehiculo, key, value)
            vehiculo.fecha_actualizacion = datetime.utcnow()
            self.db.commit()
            self.db.refresh(vehiculo)
        return vehiculo

    def eliminar_vehiculo(self, id_vehiculo: str) -> bool:
        vehiculo = self.obtener_vehiculo_por_id(id_vehiculo)
        if vehiculo:
            self.db.delete(vehiculo)
            self.db.commit()
            return True
        return False

    def cambiar_disponibilidad(
        self, id_vehiculo: str, disponible: bool
    ) -> Optional[Vehiculo]:
        return self.actualizar_vehiculo(id_vehiculo, {"disponible": disponible})
