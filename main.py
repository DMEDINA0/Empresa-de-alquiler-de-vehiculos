"""
Clase principal del sistema de alquiler de vehículos.

Gestiona la autenticación de usuarios, registro y selección de clientes,
alquiler y devolución de vehículos, generación de facturas y navegación
por el menú principal.
"""

from database.config import SessionLocal
from entities.cliente import Cliente
from entities.vehiculo import Vehiculo
from entities.alquiler import Alquiler
from entities.factura import Factura
from crud.alquiler_crud import AlquilerCRUD
from crud.factura_crud import FacturaCRUD
from crud.usuario_crud import UsuarioService
from vehiculos import Vehiculos
from uuid import uuid4
from datetime import datetime


class Main:
    def __init__(self):
        self.db = SessionLocal()
        self.usuario_service = UsuarioService(self.db)
        self.alquiler_service = AlquilerCRUD(self.db)
        self.factura_service = FacturaCRUD(self.db)
        self.vehiculos_service = Vehiculos(self.db)

    def autenticar_usuario(self):
        print("🔐 Iniciar sesión")
        email = input("Email: ")
        contraseña = input("Contraseña: ")
        usuario = self.usuario_service.login(email, contraseña)
        if not usuario:
            print("Acceso denegado. Verifica tus credenciales.")
            exit()
        return usuario

    def registrar_cliente(self, usuario):
        try:
            primer_nombre = input("Primer nombre: ")
            segundo_nombre = input("Segundo nombre: ")
            primer_apellido = input("Primer apellido: ")
            segundo_apellido = input("Segundo apellido: ")
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

            nuevo_cliente = Cliente(
                id_cliente=uuid4(),
                primer_nombre=primer_nombre,
                segundo_nombre=segundo_nombre,
                primer_apellido=primer_apellido,
                segundo_apellido=segundo_apellido,
                fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date(),
                id_usuario_creacion=usuario.id_usuario,
                fecha_creacion=datetime.utcnow(),
                fecha_actualizacion=datetime.utcnow(),
            )

            self.db.add(nuevo_cliente)
            self.db.commit()
            self.db.refresh(nuevo_cliente)

            print(f"👤 Cliente registrado: {nuevo_cliente.primer_nombre}")
            return nuevo_cliente
        except Exception as e:
            self.db.rollback()
            print(f"Error al registrar cliente: {e}")
            return None

    def seleccionar_cliente(self, usuario):
        clientes = self.db.query(Cliente).all()

        print("\nSeleccione un cliente existente:")
        for i, c in enumerate(clientes, start=1):
            print(f"{i}. {c.primer_nombre} {c.primer_apellido} (ID: {c.id_cliente})")
        print("0. Registrar nuevo cliente")

        try:
            opcion = int(input("Opción: "))
            if opcion == 0:
                return self.registrar_cliente(usuario)
            elif 1 <= opcion <= len(clientes):
                return clientes[opcion - 1]
            else:
                print("Opción inválida.")
                return self.seleccionar_cliente(usuario)
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")
            return self.seleccionar_cliente(usuario)

    def mostrar_clientes(self):
        clientes = self.db.query(Cliente).all()
        print("\nLista de Clientes:")
        if not clientes:
            print("No hay clientes registrados.")
        for cliente in clientes:
            print(
                f"ID: {cliente.id_cliente} | Nombre: {cliente.primer_nombre} {cliente.primer_apellido}"
            )

    def mostrar_vehiculos(self):
        self.vehiculos_service.listar_disponibles()

    def cargar_vehiculos(self):
        self.vehiculos_service.cargar_vehiculos_iniciales()

    def alquilar_vehiculo(self, cliente):
        if self.alquiler_service.obtener_alquiler_activo(cliente.id_cliente):
            print(
                "⚠️ Ya tienes un vehículo alquilado. Devuélvelo antes de alquilar otro."
            )
            return

        disponibles = self.db.query(Vehiculo).filter_by(disponible=True).all()
        if not disponibles:
            print("No hay vehículos disponibles.")
            return

        print("\nSeleccione un vehículo:")
        for i, v in enumerate(disponibles, start=1):
            print(f"{i}. {v.nombre} (${v.tarifa_hora}/hora)")

        try:
            opcion = int(input("Opción: ")) - 1
            if opcion < 0 or opcion >= len(disponibles):
                print("Opción inválida.")
                return
            horas = int(input("¿Cuántas horas desea alquilarlo?: "))
            vehiculo = disponibles[opcion]
            alquiler = self.alquiler_service.crear_alquiler(
                cliente.id_cliente,
                vehiculo.id_vehiculo,
                horas,
                cliente.id_usuario_creacion,
            )
            self.factura_service.generar_factura(
                alquiler.id_alquiler, cliente.id_usuario_creacion
            )
        except Exception as e:
            print(f"Error en el alquiler: {e}")
            self.db.rollback()

    def devolver_vehiculo(self, cliente):
        alquiler = self.alquiler_service.obtener_alquiler_activo(cliente.id_cliente)
        if not alquiler:
            print("No tienes un vehículo alquilado.")
            return
        self.alquiler_service.devolver_vehiculo(alquiler.id_alquiler)

    def mostrar_facturas(self, cliente):
        facturas = (
            self.db.query(Factura)
            .join(Alquiler)
            .filter(Alquiler.id_cliente == cliente.id_cliente)
            .all()
        )

        print("\n📄 Facturas del cliente:")
        if not facturas:
            print("No hay facturas registradas.")
            return

        for f in facturas:
            print(
                f"- Fecha: {f.fecha_emision.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Monto: ${f.monto_total:,} | ID Alquiler: {f.id_alquiler}"
            )

    def menu(self):
        print("====== Bienvenido a la Empresa de Alquiler de Vehículos ======\n")
        usuario = self.autenticar_usuario()
        cliente = self.seleccionar_cliente(usuario)

        if not cliente:
            print("❌ No se pudo continuar sin cliente. Cerrando sesión.")
            return

        while True:
            print("\n====== Menú Principal ======")
            print("1. Mostrar vehículos disponibles")
            print("2. Mostrar clientes")
            print("3. Alquilar vehículo")
            print("4. Devolver vehículo")
            print("5. Cargar vehículos iniciales")
            print("6. Salir")
            print("7. Ver facturas")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.mostrar_vehiculos()
            elif opcion == "2":
                self.mostrar_clientes()
            elif opcion == "3":
                self.alquilar_vehiculo(cliente)
            elif opcion == "4":
                self.devolver_vehiculo(cliente)
            elif opcion == "5":
                self.cargar_vehiculos()
            elif opcion == "6":
                print("Gracias por usar el sistema de alquiler.")
                break
            elif opcion == "7":
                self.mostrar_facturas(cliente)
            else:
                print("Opción no válida.")


if __name__ == "__main__":
    app = Main()
    app.menu()
