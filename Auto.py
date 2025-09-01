from Vehiculo import Vehiculo

class Auto(Vehiculo):
    def __init__(self, nombre: str):
        super().__init__(nombre=nombre, tarifa_hora=20000)

    def calcular_costo(self, horas: int) -> int:
        return self.tarifa_hora * horas