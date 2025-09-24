"""
Clase que implementa operaciones CRUD para la entidad Usuario.

Permite registrar, consultar, actualizar, eliminar y autenticar usuarios,
así como verificar roles y desactivar cuentas.
"""

from entities.usuario import Usuario
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone
import bcrypt


class UsuarioService:
    def __init__(self, db: Session):
        self.db = db

    def registrar_usuario(
        self,
        primer_nombre: str,
        segundo_nombre: str,
        primer_apellido: str,
        segundo_apellido: str,
        rol_usuario: str,
        email: str,
        contraseña: str,
        id_cliente: Optional[str] = None,
        id_usuario_creacion: Optional[str] = None,
    ) -> Usuario:

        contraseña_hash = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()

        nuevo_usuario = Usuario(
            id_usuario=uuid4(),
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            rol_usuario=rol_usuario,
            email=email,
            contraseña=contraseña_hash,
            es_admin=(rol_usuario.lower() == "admin"),
            id_cliente=id_cliente,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow().replace(tzinfo=timezone.utc),
            fecha_actualizacion=datetime.utcnow().replace(tzinfo=timezone.utc),
        )
        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    def listar_usuarios(self) -> List[Usuario]:
        return self.db.query(Usuario).all()

    def obtener_usuario_por_id(self, id_usuario: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter_by(id_usuario=id_usuario).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter_by(email=email).first()

    def actualizar_usuario(
        self, id_usuario: str, nuevos_datos: dict
    ) -> Optional[Usuario]:
        usuario = self.obtener_usuario_por_id(id_usuario)
        if usuario:
            for key, value in nuevos_datos.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)
            usuario.fecha_actualizacion = datetime.utcnow().replace(tzinfo=timezone.utc)
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, id_usuario: str) -> bool:
        usuario = self.obtener_usuario_por_id(id_usuario)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, id_usuario: str) -> Optional[Usuario]:
        return self.actualizar_usuario(id_usuario, {"rol_usuario": "inactivo"})

    def es_admin(self, id_usuario: str) -> bool:
        usuario = self.obtener_usuario_por_id(id_usuario)
        return usuario.es_admin if usuario else False

    def login(self, email: str, contraseña: str) -> Optional[Usuario]:
        usuario = self.obtener_usuario_por_email(email)

        try:
            if usuario and bcrypt.checkpw(
                contraseña.encode(), usuario.contraseña.encode()
            ):
                return usuario
        except ValueError:
            print("⚠️ Error: la contraseña almacenada no es un hash válido.")
        return None
