from sqlalchemy import Table, Column, String, ForeignKey
from API.config.database import meta

# aca cambie el esquema de la tabla login para usar correo en vez de ci y
# los campos que faltaban para poder hacer la relacion con la tabla personas
model_login = Table(
    "login", meta,
    Column("correo", String(100), ForeignKey("personas.correo"), primary_key=True),
    Column("contrasena", String(150), nullable=False)
    
)

