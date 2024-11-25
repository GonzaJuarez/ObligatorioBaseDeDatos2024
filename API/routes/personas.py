from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from config.database import SessionLocal
from config .db import connection
from schemas.personas import Personas


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
        result = db.execute(text("SELECT * FROM personas"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@personas.get("/personas/{persona_ci}")
def get_persona(persona_ci: int, db: Session = Depends(get_db)):
    if not isinstance(persona_ci, int):
        return HTTPException(status_code=400, detail="El ci debe ser un número entero")
    try:
        result = db.execute(
            text("""
            SELECT * FROM personas WHERE ci = :persona_ci
            """),
            {"persona_ci": persona_ci}).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@personas.post("/personas")
def create_persona(persona: Personas, db: Session = Depends(get_db)):
    if not isinstance(persona.ci, int):
        return HTTPException(status_code=400, detail="El ci debe ser un número entero")
    if not isinstance(persona.id_rol, int):
        return HTTPException(status_code=400, detail="El id de rol debe ser un número entero")
    if not isinstance(persona.nombre, str):
        return HTTPException(status_code=400, detail="El nombre debe ser una cadena de texto")
    if not isinstance(persona.apellido, str):
        return HTTPException(status_code=400, detail="El apellido debe ser una cadena de texto")
    if not isinstance(persona.fecha_nacimiento, str):
        return HTTPException(status_code=400, detail="La fecha de nacimiento debe ser una cadena de texto")
    if not isinstance(persona.cel, int):
        return HTTPException(status_code=400, detail="El celular debe ser una cadena de texto")
    if not isinstance(persona.correo, str):
        return HTTPException(status_code=400, detail="El correo debe ser una cadena de texto")
    new_persona = {
        "ci": persona.ci,
        "id_rol": persona.id_rol,
        "nombre": persona.nombre,
        "apellido": persona.apellido,
        "fecha_nacimiento": persona.fecha_nacimiento,
        "cel": persona.cel,
        "correo": persona.correo
    }
    try:
        db.execute(
            text("""
            INSERT INTO personas (ci, id_rol, nombre, apellido, fecha_nacimiento, cel, correo)
            VALUES (:ci, :id_rol, :nombre, :apellido, :fecha_nacimiento, :cel, :correo)
            """),
            new_persona
        )
        db.commit()
        return {"message": "Persona creada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@personas.put("/personas/{persona_ci}")
def update_persona(persona_ci: int, persona: Personas, db: Session = Depends(get_db)):
    if not isinstance(persona_ci, int):
        return HTTPException(status_code=400, detail="El ci debe ser un número entero")
    if not isinstance(persona.id_rol, int):
        return HTTPException(status_code=400, detail="El id de rol debe ser un número entero")
    if not isinstance(persona.nombre, str):
        return HTTPException(status_code=400, detail="El nombre debe ser una cadena de texto")
    if not isinstance(persona.apellido, str):
        return HTTPException(status_code=400, detail="El apellido debe ser una cadena de texto")
    if not isinstance(persona.fecha_nacimiento, str):
        return HTTPException(status_code=400, detail="La fecha de nacimiento debe ser una cadena de texto")
    if not isinstance(persona.cel, int):
        return HTTPException(status_code=400, detail="El celular debe ser una cadena de texto")
    if not isinstance(persona.correo, str):
        return HTTPException(status_code=400, detail="El correo debe ser una cadena de texto")
    updated_persona = {
        "ci": persona_ci,
        "id_rol": persona.id_rol,
        "nombre": persona.nombre,
        "apellido": persona.apellido,
        "fecha_nacimiento": persona.fecha_nacimiento,
        "cel": persona.cel,
        "correo": persona.correo
    }
    try:
        db.execute(
            text("""
            UPDATE personas SET 
            id_rol = :id_rol, 
            nombre = :nombre, 
            apellido = :apellido, 
            fecha_nacimiento = :fecha_nacimiento, 
            cel = :cel, 
            correo = :correo
            WHERE ci = :ci
            """),
            updated_persona
        )
        db.commit()
        return {"message": "Persona actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@personas.delete("/personas/{persona_ci}")
def delete_persona(persona_ci: int, db: Session = Depends(get_db)):
    if not isinstance(persona_ci, int):
        return HTTPException(status_code=400, detail="El ci debe ser un número entero")
    try:
        db.execute(
            text("""
            DELETE FROM personas WHERE ci = :persona_ci
            """),
            {"persona_ci": persona_ci}
        )
        db.commit()
        return {"message": "Persona eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))