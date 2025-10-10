"""
Clase que implementa operaciones CRUD para la entidad Usuario.

Permite registrar, consultar, actualizar, eliminar y autenticar usuarios,
así como verificar roles y desactivar cuentas.
"""

from entities.usuario import Usuario
from entities.cliente import Cliente
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from uuid import uuid4, UUID
from datetime import datetime, timezone
import bcrypt


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

  
    def registrar_usuario(
        self,
        primer_nombre: str,
        segundo_nombre: Optional[str],
        primer_apellido: str,
        segundo_apellido: Optional[str],
        rol_usuario: str,
        email: str,
        contraseña: str,
        id_cliente: Optional[str] = None,
        id_usuario_creacion: Optional[str] = None,
    ) -> Usuario:

        
        if self.obtener_usuario_por_email(email):
            raise ValueError(f"El email '{email}' ya existe.")

       
        if id_cliente:
            existe_cliente = self.db.query(Cliente).filter_by(id_cliente=id_cliente).first()
            if not existe_cliente:
                raise ValueError(f"El cliente con id '{id_cliente}' no existe.")

        
        contraseña_hash = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()

        
        id_usuario_creacion = id_usuario_creacion or str(uuid4())

       
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
            fecha_creacion=datetime.now(timezone.utc),
            fecha_actualizacion=datetime.now(timezone.utc),
        )

        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    def listar_usuario(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def obtener_usuario_por_id(self, id_usuario: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter_by(id_usuario=id_usuario).first()


    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter_by(email=email).first()

    
    def eliminar_usuario(self, id_usuario: str) -> bool:
        usuario = self.obtener_usuario_por_id(id_usuario)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True


    def actualizar_usuario(self, id_usuario: str, nuevos_datos: Dict[str, Optional[str]]) -> Optional[Usuario]:
        """
        Actualiza un usuario existente.
        """
        usuario = self.obtener_usuario_por_id(id_usuario)
        if not usuario:
            return None

        for key, value in nuevos_datos.items():
            if hasattr(usuario, key) and value is not None:
               
                if key in ["contraseña", "contrasena"]:
                    hashed = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
                    setattr(usuario, "contraseña", hashed)
                else:
                    setattr(usuario, key, value)

        usuario.fecha_actualizacion = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    
    def desactivar_usuario(self, id_usuario: str) -> Optional[Usuario]:
        return self.actualizar_usuario(id_usuario, {"rol_usuario": "inactivo"})

  
    def es_admin(self, id_usuario: str) -> bool:
        usuario = self.obtener_usuario_por_id(id_usuario)
        return usuario.es_admin if usuario else False

    
    def login(self, email: str, contraseña: str) -> Optional[Usuario]:
        usuario = self.obtener_usuario_por_email(email)
        if usuario and bcrypt.checkpw(contraseña.encode(), usuario.contraseña.encode()):
            return usuario
        return None

