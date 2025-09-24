"""
Servicio para gestión de usuarios.

Permite registrar nuevos usuarios, validar credenciales de acceso
y listar usuarios registrados en el sistema.
"""

from entities.usuario import Usuario
from database.config import SessionLocal
from uuid import uuid4
from uuid import UUID
from datetime import datetime
from security import (
    hash_password,
    verify_password,
)


class UsuarioService:
    def __init__(self):
        self.db = SessionLocal()

    def registrar_usuario(
        self,
        primer_nombre: str,
        segundo_nombre: str,
        primer_apellido: str,
        segundo_apellido: str,
        rol_usuario: str,
        email: str,
        contraseña: str,
        id_cliente: str = None,
        id_usuario_creacion: UUID = UUID("00000000-0000-0000-0000-000000000000"),
    ) -> Usuario:
        nuevo_usuario = Usuario(
            id_usuario=uuid4(),
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            rol_usuario=rol_usuario,
            email=email,
            contraseña=hash_password(contraseña),
            id_cliente=id_cliente,
            id_usuario_creacion=id_usuario_creacion,
            fecha_creacion=datetime.utcnow(),
        )

        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)

        print(f"✅ Usuario registrado: {nuevo_usuario.primer_nombre} ({rol_usuario})")
        return nuevo_usuario

    def login(self, email: str, contraseña: str) -> Usuario | None:
        """Valida credenciales de usuario"""
        usuario = self.db.query(Usuario).filter_by(email=email).first()
        if usuario and verify_password(contraseña, usuario.contraseña):
            print(f"✅ Bienvenido {usuario.primer_nombre}")
            return usuario
        print("❌ Credenciales inválidas")
        return None

    def listar_usuarios(self):
        usuarios = self.db.query(Usuario).all()
        for u in usuarios:
            print(
                f"{u.id_usuario} | {u.primer_nombre} {u.primer_apellido} | Rol: {u.rol_usuario} | Email: {u.email}"
            )
