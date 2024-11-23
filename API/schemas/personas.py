from pydantic import BaseModel


class Personas(BaseModel):
    ci: int
    id_rol: int
    nombre: str
    apellido: str
    fecha_nacimiento: str
    cel: int
    correo: str
