
from typing import List
from uuid import UUID

from crud.categoria_crud import CategoriaVehiculoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import CategoriaCreate, CategoriaResponse, CategoriaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=List[CategoriaResponse])
async def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todas las categorías con paginación."""
    try:
        categoria_crud = CategoriaVehiculoCRUD(db)
        categorias = categoria_crud.listar_categorias()
        return categorias[skip: skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}",
        )


@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def obtener_categoria_por_id(categoria_id: UUID, db: Session = Depends(get_db)):
    """Obtener una categoría por ID."""
    try:
        categoria_crud = CategoriaVehiculoCRUD(db)
        categoria = categoria_crud.obtener_categoria_por_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return categoria
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}",
        )


@router.post("/", response_model=CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    try:
        crud = CategoriaVehiculoCRUD(db)
        nueva = crud.crear_categoria(categoria.dict())
        return nueva
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear categoría: {str(e)}")


@router.put("/{id_categoria}", response_model=CategoriaResponse)
async def actualizar_categoria(id_categoria: UUID, categoria_data: CategoriaUpdate, db: Session = Depends(get_db)):
    """Actualizar una categoría existente."""
    try:
        categoria_crud = CategoriaVehiculoCRUD(db)
        categoria_actualizada = categoria_crud.actualizar_categoria(
            id_categoria, categoria_data.dict(exclude_unset=True)
        )
        if not categoria_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return categoria_actualizada
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar categoría: {str(e)}",
        )


@router.delete("/{id_categoria}", response_model=RespuestaAPI)
async def eliminar_categoria(id_categoria: UUID, db: Session = Depends(get_db)):
    """Eliminar una categoría."""
    categoria_crud = CategoriaVehiculoCRUD(db)
    categoria_existente = categoria_crud.obtener_categoria_por_id(id_categoria)
    if not categoria_existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    eliminada = categoria_crud.eliminar_categoria(id_categoria)
    if eliminada:
        return RespuestaAPI(mensaje="Categoría eliminada exitosamente", exito=True)
    else:
        raise HTTPException(status_code=500, detail="Error al eliminar categoría")