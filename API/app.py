from fastapi import FastAPI

from routes.actividades import actividades
from routes.alumno_clase import alumno_clase
from routes.clase import clases
from routes.equipamiento import equipamiento
from routes.login import login
from routes.personas import personas
from routes.roles import Roles
from routes.turnos import turnos

from config.data_insert import insert_data


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
