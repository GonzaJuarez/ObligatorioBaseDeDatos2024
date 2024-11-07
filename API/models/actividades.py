from sqlalchemy import Table, Column, Integer, String, Float
from API.config.database import meta

model_actividad = Table("actividades", meta,
                 Column ("id", Integer, primary_key=True, autoincrement=True),
                 Column("descripcion", String(50), nullable=False),
                 Column("costo", Float, nullable=False))


