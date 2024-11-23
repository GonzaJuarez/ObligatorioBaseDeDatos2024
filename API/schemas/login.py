from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    ci: int
    contraseña: str