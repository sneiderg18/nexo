from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models import Criticidad


class EquipoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    tipo: str = Field(min_length=1, max_length=50)
    area: Optional[str] = Field(default=None, max_length=100)
    ip: Optional[str] = Field(default=None, max_length=45)
    criticidad: Criticidad = Criticidad.media


class EquipoCrear(EquipoBase):
    pass


class EquipoActualizar(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    tipo: Optional[str] = Field(default=None, min_length=1, max_length=50)
    area: Optional[str] = Field(default=None, max_length=100)
    ip: Optional[str] = Field(default=None, max_length=45)
    criticidad: Optional[Criticidad] = None
    activo: Optional[bool] = None


class EquipoRespuesta(EquipoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activo: bool
    creado_en: datetime