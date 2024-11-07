from pydantic import BaseModel


class Alumno_clase(BaseModel):
    id_clase: int
    ci_alumno: int
    id_equipamiento: int
