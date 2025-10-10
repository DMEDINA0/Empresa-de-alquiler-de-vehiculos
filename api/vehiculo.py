from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.vehiculo_crud import VehiculoCRUD
from database.config import get_db
from schemas import (
    RespuestaAPI,
    VehiculoCreate,
    VehiculoResponse,
    VehiculoUpdate,
)

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])


@router.get("/", response_model=List[VehiculoResponse])
async def listar_vehiculos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los vehículos con paginación."""
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculos = vehiculo_crud.listar_vehiculos(skip=skip, limit=limit)
        return vehiculos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener vehículos: {str(e)}",
        )



@router.get("/{vehiculo_id}", response_model=VehiculoResponse)
async def obtener_vehiculo_por_id(vehiculo_id: UUID, db: Session = Depends(get_db)):
    """Obtener un vehículo por ID."""
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo = vehiculo_crud.obtener_vehiculo_por_id(vehiculo_id)
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado"
            )
        return vehiculo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener vehículo: {str(e)}",
        )



@router.post("/", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
async def crear_vehiculo(vehiculo_data: VehiculoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo vehículo."""
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo = vehiculo_crud.crear_vehiculo(
            nombre=vehiculo_data.nombre,
            tarifa_hora=vehiculo_data.tarifa_hora,
            id_categoria=vehiculo_data.id_categoria,
            id_usuario_creacion=vehiculo_data.id_usuario_creacion,
        )
        return vehiculo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear vehículo: {str(e)}",
        )



@router.put("/{vehiculo_id}", response_model=VehiculoResponse)
async def actualizar_vehiculo(
    vehiculo_id: UUID, vehiculo_data: VehiculoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un vehículo existente."""
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo_existente = vehiculo_crud.obtener_vehiculo_por_id(vehiculo_id)

        if not vehiculo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado"
            )

        campos_actualizacion = {
            k: v for k, v in vehiculo_data.dict().items() if v is not None
        }

        vehiculo_actualizado = vehiculo_crud.actualizar_vehiculo(
            vehiculo_id, campos_actualizacion
        )

        return vehiculo_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar vehículo: {str(e)}",
        )


@router.delete("/{vehiculo_id}", response_model=RespuestaAPI)
async def eliminar_vehiculo(vehiculo_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un vehículo."""
    try:
        vehiculo_crud = VehiculoCRUD(db)
        vehiculo_existente = vehiculo_crud.obtener_vehiculo_por_id(vehiculo_id)

        if not vehiculo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado"
            )

        eliminado = vehiculo_crud.eliminar_vehiculo(vehiculo_id)
        if eliminado:
            return RespuestaAPI(mensaje="Vehículo eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar vehículo",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar vehículo: {str(e)}",
        )
