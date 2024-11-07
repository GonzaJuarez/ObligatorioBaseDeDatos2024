from sqlalchemy import Table, Column, Integer, ForeignKey
from API.config.database import meta


model_alumno_clase = Table("alumno_clase", meta,
                 Column ("id_clase", Integer, ForeignKey("clase.id"),primary_key=True),
                 Column("ci_alumno", Integer, ForeignKey("personas.ci"), primary_key=True),
                 Column("id_equipamiento", Integer, ForeignKey("equipamiento.id")))

