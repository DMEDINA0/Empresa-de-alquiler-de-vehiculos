"""
Carga inicial y visualización de vehículos
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

        # ✅ UUID válido con guiones
        admin_id = UUID("00000000-0000-0000-0000-000000000000")

        # Crear categoría por defecto
        categoria = CategoriaVehiculo(
            id_categoria=uuid4(),
            nombre_categoria="General",
            descripcion="Categoría por defecto",
            id_usuario_creacion=admin_id,
            id_usuario_edicion=None,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
        )
        self.db.add(categoria)
        self.db.commit()

        # No necesitas refresh si ya tienes el objeto en memoria
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
















