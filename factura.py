from entities.factura import Factura
from entities.alquiler import Alquiler
from entities.vehiculo import Vehiculo
from database.config import SessionLocal
from uuid import uuid4
from datetime import datetime


class FacturaService:
    def __init__(self):
        self.db = SessionLocal()

    def generar_factura(self, alquiler_id):
        alquiler = self.db.query(Alquiler).filter_by(id_alquiler=alquiler_id).first()
        if not alquiler:
            print("❌ Alquiler no encontrado.")
            return None

        vehiculo = self.db.query(Vehiculo).get(alquiler.id_vehiculo)
        monto_total = vehiculo.tarifa_hora * alquiler.horas

        factura = Factura(
            id_factura=uuid4(),
            fecha_emision=datetime.utcnow(),
            monto_total=monto_total,
            id_alquiler=alquiler.id_alquiler,
        )

        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)

        print(f"🧾 Factura generada: ${monto_total}")
        return factura
