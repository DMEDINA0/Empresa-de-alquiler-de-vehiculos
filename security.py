"""
Servicio para gestión de usuarios: registro, autenticación y listado.
"""

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Encripta una contraseña en texto plano.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su versión encriptada.
    """
    return pwd_context.verify(plain_password, hashed_password)
