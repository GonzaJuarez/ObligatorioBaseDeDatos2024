from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from API.config.database import SessionLocal
from API.config.db import connection
from API.models.personas import model_persona
from API.schemas.personas import Personas

personas = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@personas.get("/personas")
def get_personas(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_persona.select()).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@personas.get("/personas/{persona_ci}")
def get_persona(persona_ci: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_persona.select().where(model_persona.c.ci == persona_ci)).first()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@personas.post("/personas")
def create_persona(persona: Personas, db: Session = Depends(get_db)):
    new_pesrona = {
        "ci": persona.ci,
        "id_rol": persona.id_rol,
        "nombre": persona.nombre,
        "apellido": persona.apellido,
        "fecha_nacimiento": persona.fecha_nacimiento,
        "cel": persona.cel,
        "correo": persona.correo
    }
    try:
        db.execute(model_persona.insert().values(new_pesrona))
        db.commit()
        return {"message": "Persona creada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@personas.put("/personas/{persona_ci}")
def update_persona(persona_ci: int, persona1: Personas, db: Session = Depends(get_db)):
    new_pesrona = {
        "ci": persona1.ci,
        "id_rol": persona1.id_rol,
        "nombre": persona1.nombre,
        "apellido": persona1.apellido,
        "fecha_nacimiento": persona1.fecha_nacimiento,
        "cel": persona1.cel,
        "correo": persona1.correo
    }
    try:
        db.execute(model_persona.update().values(new_pesrona).where(model_persona.c.ci == persona_ci))
        db.commit()
        return {"message": "Persona actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@personas.delete("/personas/{persona_ci}")
def delete_persona(persona_ci: int, db: Session = Depends(get_db)):
    try:
        db.execute(model_persona.delete().where(model_persona.c.ci == persona_ci))
        db.commit()
        return {"message": "Persona eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))