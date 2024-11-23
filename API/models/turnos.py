from sqlalchemy import Table, Column, Integer, Time
from API.config.database import meta

model_turno = Table("turnos", meta,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("hora_inicio", Time, nullable=False),
                    Column("hora_fin", Time, nullable=False))
