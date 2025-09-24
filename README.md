# Empresa-de-alquiler-de-vehiculos

Empresa de Alquiler de Vehículos

Este proyecto es una aplicación de consola desarrollada en Python que simula el funcionamiento de una empresa de alquiler de vehículos. Utiliza principios de **Programación Orientada a Objetos (POO)**, validación de datos con **Pydantic**, y persistencia con **SQLAlchemy ORM**. La base de datos está alojada en **NEON**, un motor PostgreSQL en la nube.

---

## ¿Qué hace el código?

- Permite registrar clientes.
- Muestra vehículos disponibles para alquilar.
- Calcula el costo estimado del alquiler según el tipo de vehículo y duración.
- Asocia un vehículo alquilado a cada cliente.
- Permite devolver vehículos y liberar su estado.
- Muestra listas de clientes y vehículos con su estado actual.
- Genera facturas automáticas por cada alquiler.
- Permite consultar el historial de facturas por cliente.
- Incluye autenticación de usuarios con validación de credenciales.

---

## Clases del Proyecto

### `Vehiculo.py`
Clase base que define atributos y métodos comunes para todos los vehículos. Utiliza `Pydantic` para validar los datos.

#### Atributos:
- `nombre`: nombre del vehículo.
- `tarifa_hora`: tarifa por hora.
- `alquilado`: indica si el vehículo está alquilado.
- `hora_alquiler`: momento en que se alquiló.
- `horas_alquiler`: duración del alquiler.

#### Métodos:
- `alquilar(horas)`: marca el vehículo como alquilado, calcula el costo y muestra un resumen.
- `devolver()`: libera el vehículo y borra la información del alquiler.
- `calcular_costo(horas)`: calcula el costo total del alquiler.

### `Auto.py`, `Moto.py`, `Bicicleta.py`
Heredan de `Vehiculo`. Cada clase representa un tipo de vehículo con tarifa fija por hora.

### `Cliente.py`
Modelo de cliente validado con Pydantic:
- `id_cliente`: identificador único UUID.
- `nombre`: nombre del cliente.
- `vehiculo_alquilado`: referencia al vehículo actualmente alquilado.

### `Main.py`
Clase principal que gestiona la lógica del sistema:
- Carga inicial de vehículos.
- Registro y selección de clientes.
- Menú interactivo para alquilar, devolver y consultar información.
- Control de estado de vehículos y clientes.
- Generación de facturas.
- Visualización del historial de facturas.

---

## ¿Cómo ejecutar el proyecto?

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/empresa-alquiler-vehiculos.git
   cd empresa-alquiler-vehiculos

2. Crea y activa un entorno virtual:
   python -m venv env
   source env/bin/activate  # En Linux/macOS
   .\env\Scripts\activate    # En Windows

3. Instala las dependencias:
   pip install -r requirements.txt

4. Configura tu archivo .env en la URL de conexion a NEON:
   DATABASE_URL=postgresql+psycopg2://usuario:contraseña@neon-host/dbname

5. Ejecuta el programa:
   python main.py