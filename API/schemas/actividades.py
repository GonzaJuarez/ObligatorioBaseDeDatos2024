from pydantic import BaseModel
from typing import Optional


class Actividades(BaseModel):
    id: Optional[int] = None
    descripcion: str
    costo: float