from sqlalchemy import Table, Column, Integer, Date
from API.config.database import meta


model_turno = Table("turnos", meta,
                 Column ("id", Integer, primary_key=True, autoincrement=True),
                 Column("hora_inicio", Date, nullable=False),
                 Column("hora_fin", Date, nullable=False))

