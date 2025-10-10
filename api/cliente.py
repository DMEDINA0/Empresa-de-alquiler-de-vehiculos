from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.cliente_crud import ClienteCRUD
from database.config import get_db
from schemas import (
    RespuestaAPI,
    ClienteCreate,
    ClienteResponse,
    ClienteUpdate,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[ClienteResponse])
async def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los clientes con paginación."""
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.listar_clientes(skip=skip, limit=limit)
        return clientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}",
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente_por_id(cliente_id: UUID, db: Session = Depends(get_db)):
    """Obtener un cliente por ID."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.obtener_cliente_por_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cliente."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.crear_cliente(
            primer_nombre=cliente_data.primer_nombre,
            segundo_nombre=cliente_data.segundo_nombre,
            primer_apellido=cliente_data.primer_apellido,
            segundo_apellido=cliente_data.segundo_apellido,
            fecha_nacimiento=cliente_data.fecha_nacimiento,
            id_usuario_creacion=cliente_data.id_usuario_creacion,
        )
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: UUID, cliente_data: ClienteUpdate, db: Session = Depends(get_db)
):
    """Actualizar un cliente existente."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente_existente = cliente_crud.obtener_cliente_por_id(cliente_id)

        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        campos_actualizacion = {
            k: v for k, v in cliente_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return cliente_existente

        cliente_actualizado = cliente_crud.actualizar_cliente(
            cliente_id, **campos_actualizacion
        )
        return cliente_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{cliente_id}", response_model=RespuestaAPI)
async def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un cliente."""
    try:
        cliente_crud = ClienteCRUD(db)
        cliente_existente = cliente_crud.obtener_cliente_por_id(cliente_id)

        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        eliminado = cliente_crud.eliminar_cliente(cliente_id)
        if eliminado:
            return RespuestaAPI(mensaje="Cliente eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cliente",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}",
        )
