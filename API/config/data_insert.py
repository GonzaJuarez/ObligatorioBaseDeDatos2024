from config.db import connection, meta, engine

from models.actividades import model_actividad
from models.alumno_clase import model_alumno_clase
from models.clase import model_clase
from models.equipamiento import model_equipamiento
from models.login import model_login
from models.personas import model_persona
from models.roles import model_roles
from models.turnos import model_turno

from config.hashing import Hasher

from env import ADMIN_CI, ADMIN_NOMBRE, ADMIN_APELLIDO, AMDIN_FECHA_NAC, ADMIN_CEL, ADMIN_CORREO, ADMIN_PASSWORD

def insert_data():
    with engine.begin() as connection:
        if connection.execute(model_roles.select().where(model_roles.c.descripcion == "Administrador")).first() is None:
            connection.execute(model_roles.insert().values({"descripcion": "Administrador"}))

        if connection.execute(model_roles.select().where(model_roles.c.descripcion == "Instructor")).first() is None:
            connection.execute(model_roles.insert().values({"descripcion": "Instructor"}))

        if connection.execute(model_roles.select().where(model_roles.c.descripcion == "Alumno")).first() is None:
            connection.execute(model_roles.insert().values({"descripcion": "Alumno"}))

        if connection.execute(model_persona.select().where(model_persona.c.ci == ADMIN_CI)).first() is None:
            admin_role_id = connection.execute(
                model_roles.select().where(model_roles.c.descripcion == "Administrador")
            ).first().id
            connection.execute(
                model_persona.insert().values({
                    "ci": ADMIN_CI,
                    "id_rol": admin_role_id,
                    "nombre": ADMIN_NOMBRE,
                    "apellido": ADMIN_APELLIDO,
                    "fecha_nacimiento": AMDIN_FECHA_NAC,
                    "cel": ADMIN_CEL,
                    "correo": ADMIN_CORREO
                })
            )

        if connection.execute(model_login.select().where(model_login.c.ci == ADMIN_CI)).first() is None:
            connection.execute(model_login.insert().values({"ci": ADMIN_CI, "contraseña": Hasher.get_password_hash(ADMIN_PASSWORD)}))

        if connection.execute(model_actividad.select().where(model_actividad.c.descripcion == "Snowboard")).first() is None:
            connection.execute(model_actividad.insert().values({"descripcion": "Snowboard", "costo": 200}))

        if connection.execute(model_actividad.select().where(model_actividad.c.descripcion == "Sky")).first() is None:
            connection.execute(model_actividad.insert().values({"descripcion": "Sky", "costo": 150}))

        if connection.execute(model_actividad.select().where(model_actividad.c.descripcion == "Moto de Nieve")).first() is None:
            connection.execute(model_actividad.insert().values({"descripcion": "Moto de Nieve", "costo": 100}))
        connection.commit()