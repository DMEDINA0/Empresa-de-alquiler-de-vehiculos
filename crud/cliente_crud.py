"""
Clase que implementa operaciones CRUD para la entidad Cliente.

Permite crear, consultar, actualizar y eliminar registros de clientes en la base de datos.
"""

from entities.cliente import Cliente
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime


class ClienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cliente(
        self,
        primer_nombre: str,
        segundo_nombre: Optional[str],
        primer_apellido: str,
        segundo_apellido: Optional[str],
        fecha_nacimiento: str,
        id_usuario_creacion: str,
    ) -> Cliente:
        nuevo_cliente = Cliente(
            id_cliente=uuid4(),
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date(),
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
            fecha_actualizacion=datetime.utcnow(),
        )
        self.db.add(nuevo_cliente)
        self.db.commit()
        self.db.refresh(nuevo_cliente)
        return nuevo_cliente

    def obtener_cliente_por_id(self, id_cliente: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter_by(id_cliente=id_cliente).first()

    def listar_clientes(self) -> List[Cliente]:
        return self.db.query(Cliente).all()

    def actualizar_cliente(
        self, id_cliente: str, nuevos_datos: dict
    ) -> Optional[Cliente]:
        cliente = self.obtener_cliente_por_id(id_cliente)
        if cliente:
            for key, value in nuevos_datos.items():
                if hasattr(cliente, key) and key not in [
                    "id_cliente",
                    "id_usuario_creacion",
                ]:
                    setattr(cliente, key, value)
            cliente.fecha_actualizacion = datetime.utcnow()
            self.db.commit()
            self.db.refresh(cliente)
        return cliente

    def eliminar_cliente(self, id_cliente: str) -> bool:
        cliente = self.obtener_cliente_por_id(id_cliente)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False
