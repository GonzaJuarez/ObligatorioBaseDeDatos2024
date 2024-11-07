from API.config.database import engine, meta

from API.models.actividades import model_actividad
from API.models.alumno_clase import model_alumno_clase
from API.models.clase import model_clase
from API.models.equipamiento import model_equipamiento
from API.models.login import model_login
from API.models.personas import model_persona
from API.models.roles import model_roles
from API.models.turnos import model_turno


try:
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

meta.create_all(engine, tables=[model_roles, model_persona, model_login, model_actividad, model_turno, model_equipamiento, model_clase, model_alumno_clase])
