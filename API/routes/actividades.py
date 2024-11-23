from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from API.config.database import SessionLocal
from API.config.db import connection
from API.schemas.actividades import Actividades


actividades = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@actividades.get("/actividades")
def get_actividades(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM actividades"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@actividades.get("/actividades/{id_actividad}")
async def get_actividad_id(id_actividad: int, db: Session = Depends(get_db)):
    if not isinstance(id_actividad, int):
        raise HTTPException(status_code=400, detail="El id debe ser un número entero.")
    try:
        result = db.execute(
            text("SELECT * FROM actividades WHERE id = :id_actividad"),
            {"id_actividad": id_actividad}
        ).first()
        return dict(result._mapping) if result else None
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@actividades.post("/actividades")
def create_actividad(actividad: Actividades, db: Session = Depends(get_db)):
    if isinstance(actividad.descripcion, str) or len(actividad.descripcion) > 50:
        raise HTTPException(status_code=400, detail="La descripción no debe exceder 50 caracteres.")
    if not isinstance(actividad.costo, float):
        raise HTTPException(status_code=400, detail="El costo debe ser un número decimal (float).")
    new_actividad = {
        "descripcion": actividad.descripcion,
        "costo": actividad.costo
    }
    try:
        db.execute(
            text("""
                INSERT INTO actividades (descripcion, costo) 
                VALUES (:descripcion, :costo)
            """),
            new_actividad
        )
        db.commit()
        return {"message": "Actividad creada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear la actividad: {str(e)}")

@actividades.put("/actividades/{id_actividad}")
def update_actividad(id_actividad: int, actividad: Actividades, db: Session = Depends(get_db)):
    if not isinstance(id_actividad, int):
        raise HTTPException(status_code=400, detail="El id debe ser un número entero.")
    if len(actividad.descripcion) > 50:
        raise HTTPException(status_code=400, detail="La descripción no debe exceder 50 caracteres.")
    if not isinstance(actividad.costo, float):
        raise HTTPException(status_code=400, detail="El costo debe ser un número decimal (float).")
    update_actividad = {
        "id_actividad": id_actividad,
        "descripcion": actividad.descripcion,
        "costo": actividad.costo,
    }
    try:
        db.execute(
            text("""
                UPDATE actividades
                SET descripcion = :descripcion, costo = :costo
                WHERE id = :id_actividad
            """),
            update_actividad
        )
        db.commit()
        return {"message": "Actividad actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar la actividad: {str(e)}")


@actividades.delete("/actividades/{id_actividad}")
def delete_actividad(id_actividad: int, db: Session = Depends(get_db)):
    if not isinstance(id_actividad, int):
        raise HTTPException(status_code=400, detail="El id debe ser un número entero.")
    try:
        db.execute(
            text("""
                DELETE FROM actividades 
                WHERE id = :id_actividad"""),
            {"id_actividad": id_actividad}
        )
        db.commit()
        return {"message": "Actividad eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar la actividad: {str(e)}")
