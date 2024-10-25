from pydantic import BaseModel

class Personas(BaseModel):
    ci: str
    id_rol: str
    nombre: str
    apellido: str
    fecha_nacimiento: str
    cel: str
    correo: str
