from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from config.database import meta

model_equipamiento = Table("equipamiento", meta,
                           Column("id", Integer, primary_key=True, autoincrement=True),
                           Column("id_actividad", Integer, ForeignKey("actividades.id"), nullable=False),
                           Column("descripcion", String(50), nullable=False),
                           Column("costo", Float, nullable=False))
