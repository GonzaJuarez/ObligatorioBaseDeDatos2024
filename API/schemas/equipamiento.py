from pydantic import BaseModel
from typing import Optional


class Equipamiento(BaseModel):
    id: Optional[int] = None
    id_actividad: int
    descripcion: str
    costo: float