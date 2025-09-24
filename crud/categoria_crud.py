"""
Clase que implementa operaciones CRUD para la entidad CategoriaVehiculo.

Permite crear, consultar, actualizar y eliminar categorías de vehículos.
"""

from entities.categoria_vehiculo import CategoriaVehiculo
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime


class CategoriaVehiculoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(
        self,
        nombre_categoria: str,
        descripcion: str = "",
        id_usuario_creacion: Optional[str] = None,
    ) -> CategoriaVehiculo:
        nueva_categoria = CategoriaVehiculo(
            id_categoria=uuid4(),
            nombre_categoria=nombre_categoria,
            descripcion=descripcion,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
            fecha_actualizacion=datetime.utcnow(),
        )
        self.db.add(nueva_categoria)
        self.db.commit()
        self.db.refresh(nueva_categoria)
        return nueva_categoria

    def obtener_categoria_por_id(
        self, id_categoria: str
    ) -> Optional[CategoriaVehiculo]:
        return (
            self.db.query(CategoriaVehiculo)
            .filter_by(id_categoria=id_categoria)
            .first()
        )

    def listar_categorias(self) -> List[CategoriaVehiculo]:
        return self.db.query(CategoriaVehiculo).all()

    def actualizar_categoria(
        self, id_categoria: str, nuevos_datos: dict
    ) -> Optional[CategoriaVehiculo]:
        categoria = self.obtener_categoria_por_id(id_categoria)
        if categoria:
            for key, value in nuevos_datos.items():
                if hasattr(categoria, key) and key not in [
                    "id_categoria",
                    "id_usuario_creacion",
                ]:
                    setattr(categoria, key, value)
            categoria.fecha_actualizacion = datetime.utcnow()
            self.db.commit()
            self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, id_categoria: str) -> bool:
        categoria = self.obtener_categoria_por_id(id_categoria)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False
