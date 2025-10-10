from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.factura_crud import FacturaCRUD
from database.config import get_db
from schemas import (
    RespuestaAPI,
    FacturaCreate,
    FacturaResponse,
    FacturaUpdate,
)

router = APIRouter(prefix="/facturas", tags=["facturas"])


@router.get("/", response_model=List[FacturaResponse])
async def listar_facturas(db: Session = Depends(get_db)):
    """Obtener todas las facturas."""
    try:
        factura_crud = FacturaCRUD(db)
        return factura_crud.listar_facturas()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener facturas: {str(e)}",
        )


@router.get("/{factura_id}", response_model=FacturaResponse)
async def obtener_factura_por_id(factura_id: UUID, db: Session = Depends(get_db)):
    """Obtener una factura por ID."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.obtener_factura_por_id(factura_id)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )
        return factura
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener factura: {str(e)}",
        )


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
async def generar_factura(factura_data: FacturaCreate, db: Session = Depends(get_db)):
    """Generar una nueva factura a partir de un alquiler."""
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.generar_factura(
            alquiler_id=factura_data.id_alquiler,
            id_usuario_creacion=factura_data.id_usuario_creacion,
        )
        return factura
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar factura: {str(e)}",
        )


@router.put("/{factura_id}", response_model=FacturaResponse)
async def actualizar_factura(
    factura_id: UUID, factura_data: FacturaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una factura existente."""
    try:
        factura_crud = FacturaCRUD(db)
        factura_existente = factura_crud.obtener_factura_por_id(factura_id)

        if not factura_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )

        campos_actualizacion = {
            k: v for k, v in factura_data.dict().items() if v is not None
        }

        factura_actualizada = factura_crud.actualizar_factura(
            factura_id, campos_actualizacion
        )
        return factura_actualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar factura: {str(e)}",
        )


@router.delete("/{factura_id}", response_model=RespuestaAPI)
async def eliminar_factura(factura_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una factura."""
    try:
        factura_crud = FacturaCRUD(db)
        factura_existente = factura_crud.obtener_factura_por_id(factura_id)

        if not factura_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
            )

        eliminada = factura_crud.eliminar_factura(factura_id)
        if eliminada:
            return RespuestaAPI(mensaje="Factura eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar factura",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar factura: {str(e)}",
        )
