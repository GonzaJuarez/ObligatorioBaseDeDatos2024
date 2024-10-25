from pydantic import BaseModel
from typing import Optional

class Clase(BaseModel):
    id: Optional[int] = None
    ci_instructor: int
    id_actividad: int
    id_turno: int
    dictada: bool