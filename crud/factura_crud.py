from entities.factura import Factura
from entities.alquiler import Alquiler
from entities.vehiculo import Vehiculo
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4, UUID
from datetime import datetime

class FacturaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def generar_factura(self, alquiler_id: UUID, id_usuario_creacion: UUID) -> Factura:
        alquiler = self.db.query(Alquiler).get(alquiler_id)
        if not alquiler:
            raise ValueError("El alquiler especificado no existe.")

        vehiculo = self.db.query(Vehiculo).get(alquiler.id_vehiculo)
        if not vehiculo:
            raise ValueError("El vehículo asociado no existe.")

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

    def obtener_factura_por_id(self, id_factura: UUID) -> Optional[Factura]:
        return self.db.query(Factura).filter_by(id_factura=id_factura).first()

    def listar_facturas(self, skip: int = 0, limit: int = 100) -> List[Factura]:
        return self.db.query(Factura).offset(skip).limit(limit).all()

    def actualizar_factura(self, id_factura: UUID, nuevos_datos: dict) -> Optional[Factura]:
        factura = self.obtener_factura_por_id(id_factura)
        if factura:
            for key, value in nuevos_datos.items():
                if hasattr(factura, key):
                    setattr(factura, key, value)
            factura.fecha_actualizacion = datetime.utcnow()
            self.db.commit()
            self.db.refresh(factura)
        return factura

    def eliminar_factura(self, id_factura: UUID) -> bool:
        factura = self.obtener_factura_por_id(id_factura)
        if factura:
            self.db.delete(factura)
            self.db.commit()
            return True
        return False
