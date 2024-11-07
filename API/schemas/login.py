from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    ci: str
    contraseña: str