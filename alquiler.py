from entities.alquiler import Alquiler
from entities.vehiculo import Vehiculo
from uuid import uuid4
from datetime import datetime


class AlquilerService:
    def __init__(self, db):
        self.db = db

    def crear_alquiler(self, cliente_id, vehiculo_id, horas, id_usuario_creacion):
        vehiculo = (
            self.db.query(Vehiculo)
            .filter_by(id_vehiculo=vehiculo_id, disponible=True)
            .first()
        )
        if not vehiculo:
            print("❌ Vehículo no disponible.")
            return None

        alquiler = Alquiler(
            id_alquiler=uuid4(),
            fecha_inicio=datetime.utcnow(),
            horas=horas,
            id_cliente=cliente_id,
            id_vehiculo=vehiculo_id,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
            fecha_actualizacion=datetime.utcnow(),
        )

        vehiculo.disponible = False

        self.db.add(alquiler)
        self.db.commit()
        self.db.refresh(alquiler)

        print(f"✅ Alquiler creado. Vehículo: {vehiculo.nombre}, Horas: {horas}")
        return alquiler

    def devolver_vehiculo(self, alquiler_id):
        alquiler = self.db.query(Alquiler).filter_by(id_alquiler=alquiler_id).first()
        if not alquiler:
            print("❌ Alquiler no encontrado.")
            return

        alquiler.fecha_fin = datetime.utcnow()
        alquiler.fecha_actualizacion = datetime.utcnow()

        vehiculo = self.db.query(Vehiculo).get(alquiler.id_vehiculo)
        vehiculo.disponible = True

        self.db.commit()
        print(f"🔄 Vehículo {vehiculo.nombre} devuelto correctamente.")

    def obtener_alquiler_activo(self, cliente_id):
        return (
            self.db.query(Alquiler)
            .filter_by(id_cliente=cliente_id, fecha_fin=None)
            .first()
        )
