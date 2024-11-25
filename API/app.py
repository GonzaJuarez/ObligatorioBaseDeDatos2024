from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.actividades import actividades
from routes.alumno_clase import alumno_clases
from routes.clase import clases
from routes.equipamiento import equipamientos
from routes.login import login
from routes.personas import personas
from routes.roles import Roles
from routes.turnos import turnos
from routes.reportes import reportes

from config.data_insert import insert_data

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

