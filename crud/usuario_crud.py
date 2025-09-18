"""
Servicio para operaciones CRUD sobre la entidad Usuario
"""

from entities.usuario import Usuario
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
from datetime import datetime


class UsuarioService:
    def __init__(self, db: Session):
        """Inicializa el servicio con la sesión de base de datos"""
        self.db = db

    def registrar_usuario(
        self,
        primer_nombre: str,
        segundo_nombre: str,
        primer_apellido: str,
        segundo_apellido: str,
        rol_usuario: str,
        id_cliente: Optional[str] = None,
        id_usuario_creacion: Optional[str] = None,
    ) -> Usuario:
        """Registrar un nuevo usuario"""
        nuevo_usuario = Usuario(
            id_usuario=uuid4(),
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            rol_usuario=rol_usuario,
            id_cliente=id_cliente,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
        )
        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    def listar_usuarios(self) -> List[Usuario]:
        """Listar todos los usuarios"""
        return self.db.query(Usuario).all()

    def obtener_usuario_por_id(self, id_usuario: str) -> Optional[Usuario]:
        """Obtener un usuario por su ID"""
        return self.db.query(Usuario).filter_by(id_usuario=id_usuario).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Obtener un usuario por su correo electrónico"""
        return self.db.query(Usuario).filter_by(email=email).first()

    def actualizar_usuario(
        self, id_usuario: str, nuevos_datos: dict
    ) -> Optional[Usuario]:
        """Actualizar los datos de un usuario"""
        usuario = self.obtener_usuario_por_id(id_usuario)
        if usuario:
            for key, value in nuevos_datos.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)
            usuario.fecha_actualizacion = datetime.utcnow()
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, id_usuario: str) -> bool:
        """Eliminar un usuario permanentemente"""
        usuario = self.obtener_usuario_por_id(id_usuario)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, id_usuario: str) -> Optional[Usuario]:
        """Desactivar un usuario (soft delete)"""
        return self.actualizar_usuario(id_usuario, {"rol_usuario": "inactivo"})

    def es_admin(self, id_usuario: str) -> bool:
        """Verificar si un usuario tiene rol de administrador"""
        usuario = self.obtener_usuario_por_id(id_usuario)
        return usuario.rol_usuario.lower() == "admin" if usuario else False

    def login(self, email: str, contraseña: str) -> Optional[Usuario]:
        """Autenticar usuario por email y contraseña"""
        usuario = self.db.query(Usuario).filter_by(email=email, contraseña=contraseña).first()
        if usuario:
            return usuario
        return None