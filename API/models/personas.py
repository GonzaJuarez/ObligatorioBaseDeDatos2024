from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from config.database import meta


model_persona = Table("personas", meta,
                      Column ("ci", Integer, primary_key=True),
                      Column("id_rol", Integer, ForeignKey("roles.id") ,nullable=False),
                      Column("nombre", String(50), nullable=False),
                      Column("apellido", String(50), nullable=False),
                      Column("fecha_nacimiento", Date, nullable=False),
                      Column("cel", Integer, nullable=False),
                      Column("correo", String(50), nullable=False))


