from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, EmailStr


"Modelos para la gestión de usuarios"

class UsuarioBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    rol_usuario: str
    email: str
    id_cliente: Optional[UUID] = None

class UsuarioCreate(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    rol_usuario: str
    email: EmailStr
    contraseña: str
    es_admin: bool = False
    id_cliente: Optional[UUID] = None
    id_usuario_creacion: Optional[UUID] = None

class UsuarioUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    rol_usuario: Optional[str] = None
    email: Optional[str] = None
    contrasena: Optional[str] = None
    id_cliente: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    es_admin: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
        from_attributes = True
        
"Modelos para la gestión de categorías de vehículos"
    
class CategoriaBase(BaseModel):
    nombre_categoria: str
    descripcion: Optional[str] = None



class CategoriaCreate(CategoriaBase):
    id_usuario_creacion: Optional[UUID] = None



class CategoriaUpdate(BaseModel):
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class CategoriaResponse(BaseModel):
    id_categoria: UUID
    nombre_categoria: str
    descripcion: Optional[str] = None
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
    

"modelos para la gestión de alquileres"

class AlquilerBase(BaseModel):
    fecha_inicio: datetime
    horas: int
    id_cliente: UUID
    id_vehiculo: UUID
    id_usuario_creacion: UUID
    fecha_creacion: datetime

class AlquilerCreate(AlquilerBase):
    id_alquiler: Optional[UUID] = None


class AlquilerUpdate(BaseModel):
    fecha_inicio: Optional[datetime] = None
    horas: Optional[int] = None
    id_cliente: Optional[UUID] = None
    id_vehiculo: Optional[UUID] = None
    id_usuario_creacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None

class AlquilerResponse(AlquilerBase):
    id_alquiler: UUID

    class Config:
        from_attributes = True
        
"Modelos para la gestión de clientes"

class ClienteBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: date


class ClienteCreate(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    id_usuario_creacion: UUID

class ClienteUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None


class ClienteResponse(BaseModel):
    id_cliente: UUID
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: date
    id_usuario_creacion: UUID  # <---- CORRIGE AQUÍ
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True  
        from_attributes = True
        
"Modelos para la gestión de facturas"

class FacturaBase(BaseModel):
    id_alquiler: UUID


class FacturaCreate(FacturaBase):
    id_usuario_creacion: UUID


class FacturaUpdate(BaseModel):
    monto_total: Optional[float] = None


class FacturaResponse(FacturaBase):
    id_factura: UUID
    monto_total: float
    fecha_emision: datetime
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        orm_mode = True

        
"Modelos para la gestión de vehículos"

class VehiculoBase(BaseModel):
    nombre: str
    tarifa_hora: float
    disponible: bool
    id_categoria: UUID


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoUpdate(BaseModel):
    nombre: Optional[str] = None
    tarifa_hora: Optional[float] = None
    disponible: Optional[bool] = None
    id_categoria: Optional[UUID] = None


class VehiculoResponse(VehiculoBase):
    id_vehiculo: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
        
# Vehículo con su categoría
class VehiculoConCategoria(VehiculoResponse):
    categoria: Optional[CategoriaResponse]


# Categoría con todos sus vehículos
class CategoriaConVehiculos(CategoriaResponse):
    vehiculos: List[VehiculoResponse] = []


# Usuario con todos sus alquileres
class UsuarioConAlquileres(UsuarioResponse):
    alquileres: List[AlquilerResponse] = []


# Alquiler con detalles del usuario y del vehículo
class AlquilerConDetalles(AlquilerResponse):
    usuario: Optional[UsuarioResponse]
    vehiculo: Optional[VehiculoResponse]
    
"Modelos de respuesta para la API"
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int