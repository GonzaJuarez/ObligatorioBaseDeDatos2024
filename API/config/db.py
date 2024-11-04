from config.database import engine, meta
from config.create_database import *

from models.actividades import model_actividad
from models.alumno_clase import model_alumno_clase
from models.clase import model_clase
from models.equipamiento import model_equipamiento
from models.login import model_login
from models.personas import model_persona
from models.roles import model_roles
from models.turnos import model_turno


try:
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

meta.create_all(engine, tables=[model_roles, model_persona, model_login, model_actividad, model_turno, model_equipamiento, model_clase, model_alumno_clase])
