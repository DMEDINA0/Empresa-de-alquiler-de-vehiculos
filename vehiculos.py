"""
Gestión de vehículos disponibles para alquiler.

Permite cargar un conjunto inicial de vehículos y listar los que están disponibles.
"""

from entities.vehiculo import Vehiculo
from entities.categoria_vehiculo import CategoriaVehiculo
from crud.vehiculo_crud import VehiculoCRUD
from uuid import uuid4, UUID
from datetime import datetime


class Vehiculos:
    def __init__(self, db):
        self.db = db
        self.crud = VehiculoCRUD(db)

    def cargar_vehiculos_iniciales(self):
        if self.db.query(Vehiculo).count() > 0:
            print("⚠️ Los vehículos ya están cargados.")
            return

        admin_id = UUID("00000000-0000-0000-0000-000000000000")

        categoria = (
            self.db.query(CategoriaVehiculo)
            .filter_by(nombre_categoria="General")
            .first()
        )
        if not categoria:
            categoria = CategoriaVehiculo(
                id_categoria=uuid4(),
                nombre_categoria="General",
                descripcion="Categoría por defecto",
                id_usuario_creacion=admin_id,
                id_usuario_edicion=None,
                fecha_creacion=datetime.utcnow(),
                fecha_actualizacion=datetime.utcnow(),
            )
            self.db.add(categoria)
            self.db.commit()

        lista = [
            {"nombre": "Auto Deportivo", "tarifa_hora": 20000},
            {"nombre": "Auto Familiar", "tarifa_hora": 18000},
            {"nombre": "Moto Scooter", "tarifa_hora": 10000},
            {"nombre": "Moto Eléctrica", "tarifa_hora": 12000},
            {"nombre": "Bicicleta Montaña", "tarifa_hora": 5000},
            {"nombre": "Bicicleta Urbana", "tarifa_hora": 4000},
        ]

        for item in lista:
            self.crud.crear_vehiculo(
                nombre=item["nombre"],
                tarifa_hora=item["tarifa_hora"],
                id_categoria=categoria.id_categoria,
                id_usuario_creacion=admin_id,
            )

        print("🚗 Vehículos cargados correctamente.")

    def listar_disponibles(self):
        disponibles = self.db.query(Vehiculo).filter_by(disponible=True).all()
        print("\n🚗 Vehículos disponibles:")
        if not disponibles:
            print("No hay vehículos disponibles.")
        for v in disponibles:
            print(f"- {v.nombre} (${v.tarifa_hora}/hora)")
