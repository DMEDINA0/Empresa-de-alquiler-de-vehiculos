from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Vehiculo(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del vehículo")
    tarifa_hora: int = Field(..., gt=0, description="Tarifa por hora")
    alquilado: bool = False
    hora_alquiler: Optional[datetime] = None
    horas_alquiler: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True  # permite datetime y objetos

    def alquilar(self, horas: int):
        if not self.alquilado:
            self.alquilado = True
            self.hora_alquiler = datetime.now()
            self.horas_alquiler = horas
            costo = self.calcular_costo(horas)
            print(f"\n {self.nombre} alquilado por {horas} horas.")
            print(f" Costo total: ${costo}\n")
        else:
            print(f" {self.nombre} ya está alquilado.")

    def devolver(self):
        if self.alquilado:
            self.alquilado = False
            self.hora_alquiler = None
            self.horas_alquiler = None
            print(f"{self.nombre} devuelto correctamente.")
        else:
            print(f"{self.nombre} no está alquilado.")

    def calcular_costo(self, horas: int) -> int:
        return self.tarifa_hora * horas
