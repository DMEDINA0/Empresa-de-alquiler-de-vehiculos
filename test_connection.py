"""
Script para probar la conexión a PostgreSQL (Neon)
"""

import sys
from uuid import uuid4
from datetime import datetime
from database.config import DATABASE_URL, engine
from sqlalchemy import text
from entities.usuario import Usuario
from entities.cliente import Cliente
from entities.vehiculo import Vehiculo
from entities.categoria_vehiculo import CategoriaVehiculo
from entities.alquiler import Alquiler
from entities.factura import Factura
import bcrypt


def test_connection():
    """Probar la conexión a la base de datos"""
    print("=== PRUEBA DE CONEXION A POSTGRESQL (NEON) ===\n")
    print(f"URL de conexion: {DATABASE_URL}\n")

    try:
        with engine.connect() as connection:
            print("[OK] Conexion exitosa a PostgreSQL!")

            result = connection.execute(text("SELECT version() as version"))
            version = result.fetchone()
            print(f"[OK] Version de PostgreSQL: {version[0]}")

            result = connection.execute(
                text(
                    "SELECT datname FROM pg_database WHERE datname = current_database()"
                )
            )
            db_exists = result.fetchone()

            if db_exists:
                print(f"[OK] Conectado a la base de datos: {db_exists[0]}")
            else:
                print("[WARNING] No se pudo verificar la base de datos actual")

            print("\nTablas disponibles:")
            result = connection.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
            )
            tables = result.fetchall()
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (No hay tablas creadas aun)")

    except Exception as e:
        print(f"[ERROR] Error de conexion: {e}")
        print("\nPosibles soluciones:")
        print("1. Verificar que la URL de conexion sea correcta")
        print("2. Verificar que la base de datos este activa en Neon")
        print("3. Verificar que las credenciales sean correctas")
        print("4. Verificar la conexion a internet")
        return False

    return True


def test_tables():
    """Probar la creacion de tablas"""
    print("\n=== PROBANDO CREACION DE TABLAS ===\n")

    try:
        from database.config import create_tables

        create_tables()
        print("[OK] Tablas creadas exitosamente")

    except Exception as e:
        print(f"[ERROR] Error creando las tablas: {e}")
        return False

    return True


def create_admin_user():
    """Crear usuario administrador por defecto"""
    print("\n=== CREANDO USUARIO ADMINISTRADOR ===\n")

    try:
        from database.config import SessionLocal

        db = SessionLocal()

        admin_exists = db.query(Usuario).filter(Usuario.es_admin == True).first()

        if admin_exists:
            print(f"[OK] Usuario administrador ya existe: {admin_exists.email}")
            db.close()
            return True

        contraseña_plana = "admin123"
        contraseña_hash = bcrypt.hashpw(
            contraseña_plana.encode(), bcrypt.gensalt()
        ).decode()

        admin_user = Usuario(
            id_usuario=uuid4(),
            primer_nombre="Admin",
            segundo_nombre="",
            primer_apellido="System",
            segundo_apellido="",
            rol_usuario="admin",
            email="admin@system.com",
            contraseña=contraseña_hash,
            es_admin=True,
            id_usuario_creacion=uuid4(),
            fecha_creacion=datetime.utcnow(),
            fecha_actualizacion=datetime.utcnow(),
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"[OK] Usuario administrador creado exitosamente")
        print(f"     ID: {admin_user.id_usuario}")
        print(f"     Email: {admin_user.email}")
        print(f"     Nombre: {admin_user.primer_nombre} {admin_user.primer_apellido}")

        db.close()
        return True

    except Exception as e:
        print(f"[ERROR] Error creando usuario administrador: {e}")
        return False


if __name__ == "__main__":
    print("Iniciando prueba de conexion...\n")

    if test_connection():
        print("\n" + "=" * 50)
        if test_tables():
            print("\n" + "=" * 50)
            create_admin_user()

        print("\n[SUCCESS] Configuracion completada!")
        print("Ahora puedes ejecutar:")
        print("  python main.py")
        print("  python ejemplo_basico.py")
    else:
        print("\n[ERROR] No se pudo establecer la conexion")
        sys.exit(1)
