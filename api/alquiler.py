from typing import List
from uuid import UUID
from crud.alquiler_crud import AlquilerCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    RespuestaAPI,
    AlquilerCreate,
    AlquilerResponse,
    AlquilerUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/alquileres", tags=["alquileres"])

@router.get("/", response_model=List[AlquilerResponse])
async def listar_alquileres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los alquileres con paginación."""
    try:
        alquiler_crud = AlquilerCRUD(db)
        alquileres = alquiler_crud.listar_alquileres()  
        return alquileres[skip: skip + limit]           
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alquileres: {str(e)}",
        )

        
@router.get("/{alquiler_id}", response_model=AlquilerResponse)
async def obtener_alquiler_por_id(alquiler_id: UUID, db: Session = Depends(get_db)):
    """Obtener un alquiler por ID."""
    try:
        alquiler_crud= AlquilerCRUD(db)
        alquiler = alquiler_crud.obtener_alquiler_por_id(alquiler_id)
        if not alquiler:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="alquiler no encontrado"
            )
        return alquiler
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener alquiler: {str(e)}",
        )
        


@router.post("/", response_model=AlquilerResponse, status_code=status.HTTP_201_CREATED)
async def crear_alquiler(alquiler_data: AlquilerCreate, db: Session = Depends(get_db)):
    try:
        alquiler_crud = AlquilerCRUD(db)
        alquiler = alquiler_crud.crear_alquiler(
            cliente_id=alquiler_data.id_cliente,
            vehiculo_id=alquiler_data.id_vehiculo,
            horas=alquiler_data.horas,
            id_usuario_creacion=alquiler_data.id_usuario_creacion,
        )
        return alquiler
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear alquiler: {str(e)}",
        )
        
@router.put("/{id_alquiler}", response_model=AlquilerResponse)
def actualizar_alquiler(
    id_alquiler: str,
    alquiler_data: AlquilerUpdate,
    db: Session = Depends(get_db)
):
    try:
        crud = AlquilerCRUD(db)
        alquiler_actualizado = crud.actualizar_alquiler(id_alquiler, alquiler_data.dict(exclude_unset=True))
        if not alquiler_actualizado:
            raise HTTPException(status_code=404, detail="Alquiler no encontrado")
        return alquiler_actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar alquiler: {e}")


@router.delete("/{alquiler_id}", response_model=RespuestaAPI)
async def eliminar_alquiler(alquiler_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un alquiler."""
    alquiler_crud = AlquilerCRUD(db)
    alquiler_existente = alquiler_crud.obtener_alquiler_por_id(alquiler_id)
    if not alquiler_existente:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")

    eliminado = alquiler_crud.eliminar_alquiler(alquiler_id)
    if eliminado:
        return RespuestaAPI(mensaje="Alquiler eliminado exitosamente", exito=True)
    else:
        raise HTTPException(status_code=500, detail="Error al eliminar alquiler")