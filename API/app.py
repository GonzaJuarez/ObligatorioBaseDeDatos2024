from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from API.routes.actividades import actividades
from API.routes.alumno_clase import alumno_clases
from API.routes.clase import clases
from API.routes.equipamiento import equipamientos
from API.routes.login import login
from API.routes.personas import personas
from API.routes.roles import Roles
from API.routes.turnos import turnos
from API.routes.reportes import reportes

from API.config.data_insert import insert_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

insert_data()

app.include_router(actividades)
app.include_router(alumno_clases)
app.include_router(clases)
app.include_router(equipamientos)
app.include_router(login)
app.include_router(personas)
app.include_router(Roles)
app.include_router(turnos)
app.include_router(reportes)


@app.get("/")
def api():
    return {"API del Obligario final de Bases de Datos 1"}

