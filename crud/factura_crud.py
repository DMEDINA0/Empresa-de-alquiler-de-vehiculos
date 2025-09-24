"""
Clase que implementa operaciones CRUD para la entidad Factura.

Permite generar, consultar, actualizar y eliminar facturas asociadas a alquileres de vehículos.
"""

from entities.factura import Factura
from entities.alquiler import Alquiler
from entities.vehiculo import Vehiculo
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime


class FacturaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def generar_factura(self, alquiler_id: str, id_usuario_creacion: str) -> Factura:
        alquiler = self.db.query(Alquiler).get(alquiler_id)
        vehiculo = self.db.query(Vehiculo).get(alquiler.id_vehiculo)
        monto_total = alquiler.horas * vehiculo.tarifa_hora

        nueva_factura = Factura(
            id_factura=uuid4(),
            fecha_emision=datetime.utcnow(),
            monto_total=monto_total,
            id_alquiler=alquiler_id,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
        )
        self.db.add(nueva_factura)
        self.db.commit()
        self.db.refresh(nueva_factura)
        return nueva_factura

    def obtener_factura_por_id(self, id_factura: str) -> Optional[Factura]:
        return self.db.query(Factura).filter_by(id_factura=id_factura).first()

    def listar_facturas(self) -> List[Factura]:
        return self.db.query(Factura).all()

    def listar_facturas_por_alquiler(self, alquiler_id: str) -> List[Factura]:
        return self.db.query(Factura).filter_by(id_alquiler=alquiler_id).all()

    def actualizar_factura(
        self, id_factura: str, nuevos_datos: dict
    ) -> Optional[Factura]:
        factura = self.obtener_factura_por_id(id_factura)
        if factura:
            for key, value in nuevos_datos.items():
                if hasattr(factura, key):
                    setattr(factura, key, value)
            factura.fecha_actualizacion = datetime.utcnow()
            self.db.commit()
            self.db.refresh(factura)
        return factura

    def eliminar_factura(self, id_factura: str) -> bool:
        factura = self.obtener_factura_por_id(id_factura)
        if factura:
            self.db.delete(factura)
            self.db.commit()
            return True
        return False
