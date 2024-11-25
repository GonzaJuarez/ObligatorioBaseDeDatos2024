from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from config.database import SessionLocal
from config.db import connection
from schemas.alumno_clase import Alumno_clase


alumno_clases = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alumno_clases.get("/alumno_clase")
def get_alumno_clase(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM alumno_clase"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@alumno_clases.get("/alumno_clase/{ci_alumno}")
def get_alumno_clase_ci(ci_alumno: int, db: Session = Depends(get_db)):
    if not isinstance(ci_alumno, int):
        raise HTTPException(status_code=400, detail="El ci del alumno debe ser un número, sin puntos ni guiones.")
    try:
        result = db.execute(
            text("SELECT * FROM alumno_clase WHERE ci_alumno = :ci_alumno"),
            {"ci_alumno": ci_alumno}
        ).fetchone()
        return dict(result._mapping) if result else None
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@alumno_clases.post("/alumno_clase")
def create_alumno_clase(alumno_clase: Alumno_clase, db: Session = Depends(get_db)):
    if not isinstance(alumno_clase.id_clase, int):
        raise HTTPException(status_code=400, detail="El id de la clase debe ser un número.")
    if not isinstance(alumno_clase.ci_alumno, int):
        raise HTTPException(status_code=400, detail="El ci del alumno debe ser un número, sin puntos ni guiones.")
    if not isinstance(alumno_clase.id_equipamiento, int):
        raise HTTPException(status_code=400, detail="El id del equipamiento debe ser un número.")
    new_alumno_clase = {
        "id_clase": alumno_clase.id_clase,
        "ci_alumno": alumno_clase.ci_alumno,
        "id_equipamiento": alumno_clase.id_equipamiento
    }
    try:
        db.execute(
            text("""
                INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento) 
                VALUES (:id_clase, :ci_alumno, :id_equipamiento)
            """),
            new_alumno_clase
        )
        db.commit()
        return {"message": "Alumno_clase creado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear el alumno_clase: {str(e)}")


@alumno_clases.put("/alumno_clase/{ci_alumno}")
def update_alumno_clase(ci_alumno: int, alumno_clase: Alumno_clase, db: Session = Depends(get_db)):
    if not isinstance(ci_alumno, int):
        raise HTTPException(status_code=400, detail="El id e la clase debe ser un número.")
    if not isinstance(alumno_clase.ci_alumno, int):
        raise HTTPException(status_code=400, detail="El ci del alumno debe ser un número, sin puntos ni guiones.")
    if not isinstance(alumno_clase.id_equipamiento, int):
        raise HTTPException(status_code=400, detail="El id del equipamiento debe ser un número.")

    updated_alumno_clase = {
        "id_clase": alumno_clase.id_clase,
        "ci_alumno": ci_alumno,
        "id_equipamiento": alumno_clase.id_equipamiento
    }
    try:
        db.execute(
            text("""
                UPDATE alumno_clase
                SET id_clase = :id_clase, id_equipamiento = :id_equipamiento
                WHERE ci_alumno = :ci_alumno
            """),
            updated_alumno_clase
        )
        db.commit()
        return {"message": "Alumno_clase actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar el alumno_clase: {str(e)}")


@alumno_clases.delete("/alumno_clase/{ci_alumno}")
def delete_alumno_clase(ci_alumno: int, db: Session = Depends(get_db)):
    if not isinstance(ci_alumno, int):
        raise HTTPException(status_code=400, detail="El CI debe ser un número, sin puntos ni guiones.")
    try:
        db.execute(
            text("""
                DELETE FROM alumno_clase
                WHERE ci_alumno = :ci_alumno
            """),
            {"ci_alumno": ci_alumno}
        )
        db.commit()
        return {"message": "Alumno_clase eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar el alumno_clase: {str(e)}")
