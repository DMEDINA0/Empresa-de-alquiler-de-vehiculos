# Empresa-de-alquiler-de-vehiculos

Este proyecto es una aplicación de consola desarrollada en Python que simula el funcionamiento de una empresa de alquiler de vehículos. Utiliza principios de **Programación Orientada a Objetos (POO)** y validación de datos con **Pydantic** para gestionar clientes, vehículos y operaciones de alquiler y devolución.

## ¿Qué hace el código?

- Permite registrar clientes.
- Muestra vehículos disponibles para alquilar.
- Calcula el costo estimado del alquiler según el tipo de vehículo y duración.
- Asocia un vehículo alquilado a cada cliente.
- Permite devolver vehículos y liberar su estado.
- Muestra listas de clientes y vehículos con su estado actual.

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

### `Auto.py`
Hereda de `Vehiculo`. Representa un automóvil con tarifa fija de `$20,000` por hora.

### `Moto.py`
Hereda de `Vehiculo`. Representa una moto con tarifa fija de `$10,000` por hora.

### `Bicicleta.py`
Hereda de `Vehiculo`. Representa una bicicleta con tarifa fija de `$5,000` por hora.

### `Cliente.py`
Modelo de cliente validado con Pydantic:
- `id_cliente`: identificador único.
- `nombre`: nombre del cliente.
- `vehiculo_alquilado`: referencia al vehículo actualmente alquilado.

### `Main.py`
Clase principal que gestiona la lógica del sistema:
- Carga inicial de vehículos.
- Registro de clientes.
- Menú interactivo para alquilar, devolver y consultar información.
- Control de estado de vehículos y clientes.


## ¿Cómo ejecutar el proyecto?

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/empresa-alquiler-vehiculos.git
   cd empresa-alquiler-vehiculos

2. Instala dependencias
- Pydantic

3. Ejecuta el programa 
- main.py

## Principios de POO aplicados
- Encapsulamiento: atributos controlados y protegidos.
- Herencia: clases Auto, Moto, Bicicleta heredan de Vehiculo.
- Polimorfismo: cada clase redefine calcular_costo() según su lógica.
- Abstracción: el usuario interactúa con una interfaz clara sin conocer la lógica interna
