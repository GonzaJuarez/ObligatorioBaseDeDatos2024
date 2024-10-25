from fastapi import APIRouter
from config.db import connection
from models.personas import model_persona
from schemas.personas import Personas

personas = APIRouter()

@personas.get("/personas")
def get_personas():
    result = connection.execute(model_persona.select()).fetchall()
    return [dict(row._mapping) for row in result]

@personas.get("/personas/{persona_ci}")
def get_persona(persona_ci: int):
    result = connection.execute(model_persona.select().where(model_persona.c.ci == persona_ci)).first()
    return dict(result._mapping)

@personas.post("/personas")
def create_persona(persona: Personas):
    new_pesrona = {
        "ci": persona.ci,
        "id_rol": persona.id_rol,
        "nombre": persona.nombre,
        "apellido": persona.apellido,
        "fecha_nacimiento": persona.fecha_nacimiento,
        "cel": persona.cel,
        "correo": persona.correo
    }
    connection.execute(model_persona.insert().values(new_pesrona))
    connection.commit()
    return {"message": "Persona creada exitosamente"}

@personas.put("/personas/{persona_ci}")
def update_persona(persona_ci: int, persona1: Personas):
    new_pesrona = {
        "ci": persona1.ci,
        "id_rol": persona1.id_rol,
        "nombre": persona1.nombre,
        "apellido": persona1.apellido,
        "fecha_nacimiento": persona1.fecha_nacimiento,
        "cel": persona1.cel,
        "correo": persona1.correo
    }
    connection.execute(model_persona.update().values(new_pesrona).where(model_persona.c.ci == persona_ci))
    connection.commit()
    return {"message": "Persona actualizada exitosamente"}

@personas.delete("/personas/{persona_ci}")
def delete_persona(persona_ci: int):
    connection.execute(model_persona.delete().where(model_persona.c.ci == persona_ci))
    connection.commit()
    return {"message": "Persona eliminada exitosamente"}