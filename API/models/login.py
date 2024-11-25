from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.database import meta

model_login = Table("login", meta,
                    Column("ci", Integer, ForeignKey("personas.ci"), primary_key=True),
                    Column("contraseña", String(150), nullable=False))
