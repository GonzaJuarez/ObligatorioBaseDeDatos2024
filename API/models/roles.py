from sqlalchemy import Table, Column, Integer, String
from config.database import meta

model_roles = Table("roles", meta,
                    Column("id", Integer, primary_key=True, autoincrement=True),
                    Column("descripcion", String(50), nullable=False))
