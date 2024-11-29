from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    correo: str
    contrasena: str