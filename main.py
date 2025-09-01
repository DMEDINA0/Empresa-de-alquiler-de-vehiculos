from Auto import Auto
from Moto import Moto
from Bicicleta import Bicicleta
from Cliente import Cliente
from Vehiculo import Vehiculo


class Main:
    def __init__(self):
        self.vehiculos = []
        self.clientes = []
        self._cargar_vehiculos()

    # ---------- CARGA DE VEHÍCULOS ----------
    def _cargar_vehiculos(self):
        # Agregamos distintos tipos de vehículos
        self.vehiculos.append(Auto(nombre="Auto Deportivo"))
        self.vehiculos.append(Auto(nombre="Auto Familiar"))
        self.vehiculos.append(Moto(nombre="Moto Scooter"))
        self.vehiculos.append(Moto(nombre="Moto Eléctrica"))
        self.vehiculos.append(Bicicleta(nombre="Bicicleta Montaña"))
        self.vehiculos.append(Bicicleta(nombre="Bicicleta Urbana"))

    # ---------- CLIENTES ----------
    def registrar_cliente(self):
        while True:
            try:
                id_cliente = int(input("Ingrese ID del cliente: "))
                nombre = input("Ingrese nombre del cliente: ")
                cliente = Cliente(id_cliente=id_cliente, nombre=nombre)
                self.clientes.append(cliente)
                print(f"👤 Cliente registrado: {cliente.nombre}\n")
                return cliente
            except Exception as e:
                print(f"Error al registrar cliente: {e}, intente nuevamente.")

    def mostrar_clientes(self):
        print("\nLista de Clientes:")
        if not self.clientes:
            print("No hay clientes registrados.")
        for cliente in self.clientes:
            estado = f"Alquiló {cliente.vehiculo_alquilado.nombre}" if cliente.vehiculo_alquilado else "Sin alquiler activo"
            print(f"ID: {cliente.id_cliente} | Nombre: {cliente.nombre} | Estado: {estado}")

    # ---------- VEHÍCULOS ----------
    def mostrar_vehiculos(self, disponibles=True):
        print("\nLista de Vehículos:")
        for i, v in enumerate(self.vehiculos, start=1):
            if disponibles and v.alquilado:
                continue
            estado = "Alquilado " if v.alquilado else "Disponible "
            print(f"{i}. {v.nombre} | Tarifa: ${v.tarifa_hora}/hora | {estado}")

    # ---------- ALQUILER ----------
    def alquilar_vehiculo(self, cliente: Cliente):
        print("\nSeleccione un vehículo disponible:")

        disponibles = [v for v in self.vehiculos if not v.alquilado]
        if not disponibles:
            print("No hay vehículos disponibles en este momento.")
            return

        for i, v in enumerate(disponibles, start=1):
            print(f"{i}. {v.nombre} (${v.tarifa_hora}/hora)")

        try:
            opcion = int(input("Opción: ")) - 1
            if opcion < 0 or opcion >= len(disponibles):
                print("Opción inválida.")
                return
        except ValueError:
            print("Debe ingresar un número.")
            return

        vehiculo = disponibles[opcion]
        horas = int(input("¿Cuántas horas desea alquilarlo?: "))
        costo_estimado = vehiculo.calcular_costo(horas)

        print(f"\n El costo de su alquiler es: ${costo_estimado}")
        confirmar = input("¿Desea confirmar el alquiler? (s/n): ")

        if confirmar.lower() == "s":
            vehiculo.alquilar(horas)
            cliente.vehiculo_alquilado = vehiculo
            print(f"Gracias por su alquiler, {cliente.nombre}.")
        else:
            print("Alquiler cancelado.")

    # ---------- DEVOLUCIÓN ----------
    def devolver_vehiculo(self, cliente: Cliente):
        if cliente.vehiculo_alquilado:
            cliente.vehiculo_alquilado.devolver()
            cliente.vehiculo_alquilado = None
        else:
            print("Usted no tiene un vehículo alquilado.")

    # ---------- MENÚ PRINCIPAL ----------
    def menu(self):
        print("====== Bienvenido a la Empresa de Alquiler de Vehículos ======\n")

        # Registro de cliente obligatorio
        cliente = self.registrar_cliente()

        while True:
            print("\n====== Menú Principal ======")
            print("1. Alquilar vehículo")
            print("2. Devolver vehículo")
            print("3. Mostrar clientes")
            print("4. Mostrar vehículos")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.alquilar_vehiculo(cliente)
            elif opcion == "2":
                self.devolver_vehiculo(cliente)
            elif opcion == "3":
                self.mostrar_clientes()
            elif opcion == "4":
                self.mostrar_vehiculos(disponibles=False)
            elif opcion == "5":
                print("Gracias por usar el sistema de alquiler.")
                break
            else:
                print("Opción no válida.")


# ==========================
# EJECUCIÓN
# ==========================
if __name__ == "__main__":
    app = Main()
    app.menu()

