from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey
from API.config.database import meta

model_clase = Table("clase", meta,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("ci_instructor", Integer, ForeignKey("personas.ci"), nullable=False),
                    Column("id_actividad", Integer, ForeignKey("actividades.id"), nullable=False),
                    Column("id_turno", Integer, ForeignKey("turnos.id"), nullable=False),
                    Column("dictada", Boolean, nullable=False))
