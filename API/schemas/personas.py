from pydantic import BaseModel


class Personas(BaseModel):
    ci: int
    nombre: str
    apellido: str
    fecha_nacimiento: str
    cel: int
    correo: str
    id_rol: int
