from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(prefix="/equipos", tags=["Equipos"])


def obtener_equipo_o_404(equipo_id: int, db: Session) -> models.Equipo:
    equipo = db.get(models.Equipo, equipo_id)
    if equipo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado"
        )
    return equipo


@router.post(
    "/", response_model=schemas.EquipoRespuesta, status_code=status.HTTP_201_CREATED
)
def crear_equipo(equipo: schemas.EquipoCrear, db: Session = Depends(get_db)):
    nuevo_equipo = models.Equipo(**equipo.model_dump())
    db.add(nuevo_equipo)
    db.commit()
    db.refresh(nuevo_equipo)
    return nuevo_equipo


@router.get("/", response_model=list[schemas.EquipoRespuesta])
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(models.Equipo).all()


@router.get("/{equipo_id}", response_model=schemas.EquipoRespuesta)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    return obtener_equipo_o_404(equipo_id, db)


@router.patch("/{equipo_id}", response_model=schemas.EquipoRespuesta)
def actualizar_equipo(
    equipo_id: int, datos: schemas.EquipoActualizar, db: Session = Depends(get_db)
):
    equipo = obtener_equipo_o_404(equipo_id, db)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(equipo, campo, valor)
    db.commit()
    db.refresh(equipo)
    return equipo


@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = obtener_equipo_o_404(equipo_id, db)
    if equipo.tickets:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El equipo tiene tickets asociados; desactívelo con PATCH (activo=false).",
        )
    db.delete(equipo)
    db.commit()