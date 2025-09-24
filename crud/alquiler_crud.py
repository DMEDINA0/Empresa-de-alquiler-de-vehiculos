"""
Clase que implementa operaciones CRUD para la entidad Alquiler.

Permite crear, consultar, actualizar y eliminar registros de alquiler,
así como gestionar la devolución de vehículos y obtener alquileres activos.
"""

from entities.alquiler import Alquiler
from entities.vehiculo import Vehiculo
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime


class AlquilerCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_alquiler(
        self, cliente_id: str, vehiculo_id: str, horas: int, id_usuario_creacion: str
    ) -> Alquiler:
        nuevo_alquiler = Alquiler(
            id_alquiler=uuid4(),
            fecha_inicio=datetime.utcnow(),
            horas=horas,
            id_cliente=cliente_id,
            id_vehiculo=vehiculo_id,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
        )
        self.db.add(nuevo_alquiler)

        vehiculo = self.db.query(Vehiculo).get(vehiculo_id)
        if vehiculo:
            vehiculo.disponible = False

        self.db.commit()
        self.db.refresh(nuevo_alquiler)
        return nuevo_alquiler

    def obtener_alquiler_por_id(self, id_alquiler: str) -> Optional[Alquiler]:
        return self.db.query(Alquiler).filter_by(id_alquiler=id_alquiler).first()

    def listar_alquileres(self) -> List[Alquiler]:
        return self.db.query(Alquiler).all()

    def listar_alquileres_por_cliente(self, cliente_id: str) -> List[Alquiler]:
        return self.db.query(Alquiler).filter_by(id_cliente=cliente_id).all()

    def actualizar_alquiler(
        self, id_alquiler: str, nuevos_datos: dict
    ) -> Optional[Alquiler]:
        alquiler = self.obtener_alquiler_por_id(id_alquiler)
        if alquiler:
            for key, value in nuevos_datos.items():
                if hasattr(alquiler, key):
                    setattr(alquiler, key, value)
            alquiler.fecha_actualizacion = datetime.utcnow()
            self.db.commit()
            self.db.refresh(alquiler)
        return alquiler

    def eliminar_alquiler(self, id_alquiler: str) -> bool:
        alquiler = self.obtener_alquiler_por_id(id_alquiler)
        if alquiler:
            self.db.delete(alquiler)
            self.db.commit()
            return True
        return False

    def devolver_vehiculo(self, id_alquiler: str) -> Optional[Alquiler]:
        alquiler = self.obtener_alquiler_por_id(id_alquiler)
        if alquiler and not alquiler.fecha_fin:
            alquiler.fecha_fin = datetime.utcnow()
            alquiler.fecha_actualizacion = datetime.utcnow()

            vehiculo = self.db.query(Vehiculo).get(alquiler.id_vehiculo)
            if vehiculo:
                vehiculo.disponible = True

            self.db.commit()
            self.db.refresh(alquiler)
        return alquiler

    def obtener_alquiler_activo(self, cliente_id: str) -> Optional[Alquiler]:
        return (
            self.db.query(Alquiler)
            .filter(Alquiler.id_cliente == cliente_id, Alquiler.fecha_fin == None)
            .first()
        )
