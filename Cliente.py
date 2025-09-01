from typing import Optional
from pydantic import BaseModel, Field
from Vehiculo import Vehiculo


class Cliente(BaseModel):
    id_cliente: int = Field(..., gt=0, description="ID único del cliente")
    nombre: str = Field(..., min_length=2, description="Nombre del cliente")
    vehiculo_alquilado: Optional[Vehiculo] = None
