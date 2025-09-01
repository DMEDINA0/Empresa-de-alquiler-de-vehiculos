from Vehiculo import Vehiculo

class Bicicleta(Vehiculo):
    def __init__(self, nombre: str):
        super().__init__(nombre=nombre, tarifa_hora=5000)

    def calcular_costo(self, horas: int) -> int:
        return int(self.tarifa_hora * horas) 
