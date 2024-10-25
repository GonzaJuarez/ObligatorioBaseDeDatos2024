from pydantic import BaseModel
from typing import Optional

class Turno(BaseModel):
    id: Optional[int] = None
    hora_inicio: str
    hora_fin: str