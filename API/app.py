from fastapi import FastAPI

from API.routes.actividades import actividades
from API.routes.alumno_clase import alumno_clase
from API.routes.clase import clases
from API.routes.equipamiento import equipamiento
from API.routes.login import login
from API.routes.personas import personas
from API.routes.roles import Roles
from API.routes.turnos import turnos

from API.config.data_insert import insert_data

app = FastAPI()

insert_data()

app.include_router(actividades)
app.include_router(alumno_clase)
app.include_router(clases)
app.include_router(equipamiento)
app.include_router(login)
app.include_router(personas)
app.include_router(Roles)
app.include_router(turnos)


@app.get("/")
def api():
    return {"API del Obligario final de Bases de Datos 1"}
