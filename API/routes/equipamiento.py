from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from API.config.database import SessionLocal
from API.config.db import connection
from API.schemas.equipamiento import Equipamiento

equipamientos = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@equipamientos.get("/equipamiento")
def get_equipamiento(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM equipamiento"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@equipamientos.get("/equipamiento/{id_equipamiento}")
def get_equipamiento(id_equipamiento: int, db: Session = Depends(get_db)):
    if not isinstance(id_equipamiento, int):
        raise HTTPException(status_code=400, detail="El id del equipamiento debe ser un número entero.")
    try:
        result = db.execute(
            text("SELECT * FROM equipamiento WHERE id = :id_equipamiento ORDER BY id DESC LIMIT 1"),
            {"id_equipamiento": id_equipamiento}
        )
        return dict(result._mapping) if result else None
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    
@equipamientos.get("/equipamiento/actividad/{id_actividad}")
def get_equipamiento_by_actividad(id_actividad: int, db: Session = Depends(get_db)):
    if not isinstance(id_actividad, int):
        raise HTTPException(status_code=400, detail="El id de la actividad debe ser un número entero.")
    try:
        result = db.execute(
            text("SELECT * FROM equipamiento WHERE id_actividad = :id_actividad"),
            {"id_actividad": id_actividad}
        )
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@equipamientos.post("/equipamiento")
def post_equipamiento(equipamiento: Equipamiento, db: Session = Depends(get_db)):
    if not isinstance(equipamiento.id_actividad, int):
        raise HTTPException(status_code=400, detail="El id del equipamiento debe ser un número entero.")
    if not isinstance(equipamiento.descripcion, str) or len(equipamiento.descripcion) > 50:
        raise HTTPException(status_code=400, detail="La descripción debe ser una cadena de máximo 50 caracteres.")
    if not isinstance(equipamiento.costo, float):
        raise HTTPException(status_code=400, detail="El costo debe ser un número decimal (float).")
    new_equipamiento = {
        "id_actividad": equipamiento.id_actividad,
        "descripcion": equipamiento.descripcion,
        "costo": equipamiento.costo
    }
    try:
        db.execute(
            text("""
                INSERT INTO equipamiento (id_actividad, descripcion, costo) 
                VALUES (:id_actividad, :descripcion, :costo)
            """),
            new_equipamiento
        )
        db.commit()
        return {"message": "Equipamiento creado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear el equipamiento: {str(e)}")


@equipamientos.put("/equipamiento/{id}")
def put_equipamiento(id_equipamiento: int, equipamiento: Equipamiento, db: Session = Depends(get_db)):
    if not isinstance(id_equipamiento, int):
        raise HTTPException(status_code=400, detail="El id del equipamiento debe ser un número entero.")
    if not isinstance(equipamiento.id_actividad, int):
        raise HTTPException(status_code=400, detail="El id de la actividad debe ser un número entero.")
    if not isinstance(equipamiento.descripcion, str) or len(equipamiento.descripcion) > 50:
        raise HTTPException(status_code=400, detail="La descripción debe ser una cadena de máximo 50 caracteres.")
    if not isinstance(equipamiento.costo, float):
        raise HTTPException(status_code=400, detail="El costo debe ser un número decimal (float).")

    updated_equipamiento = {
        "id_equipamiento": id_equipamiento,
        "id_actividad": equipamiento.id_actividad,
        "descripcion": equipamiento.descripcion,
        "costo": equipamiento.costo
    }
    try:
        db.execute(
            text("""
                UPDATE equipamiento
                SET id_actividad = :id_actividad, 
                descripcion = :descripcion, 
                costo = :costo
                WHERE id = :id_equipamiento
            """), updated_equipamiento
        )
        db.commit()
        return {"message": "Equipamiento actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar el equipamiento: {str(e)}")


@equipamientos.delete("/equipamiento/{id}")
def delete_equipamiento(id_equipamiento: int, db: Session = Depends(get_db)):
    if not isinstance(id_equipamiento, int):
        raise HTTPException(status_code=400, detail="El id del equipamiento debe ser un número entero.")
    try:
        db.execute(
            text("DELETE FROM equipamiento WHERE id = :id_equipamiento"),
            {"id_equipamiento": id_equipamiento}
        )
        db.commit()
        return {"message": "Equipamiento eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar el equipamiento: {str(e)}")
