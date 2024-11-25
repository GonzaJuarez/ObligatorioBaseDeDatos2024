from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from config.database import SessionLocal
from config.db import connection
from schemas.clase import Clase


clases = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@clases.get("/clases")
def get_clases(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM clase"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@clases.get("/clases/{id_clase}")
def get_clase_id(id_clase: int, db: Session = Depends(get_db)):
    if not isinstance(id_clase, int):
        raise HTTPException(status_code=400, detail="El id_clase debe ser un número entero.")
    try:
        result = db.execute(
            text("SELECT * FROM clase WHERE id = :id_clase"),
            {"id_clase": id_clase}
        ).first()
        return dict(result._mapping) if result else None
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@clases.post("/clases")
def create_clase(clase: Clase, db: Session = Depends(get_db)):
    if not isinstance(clase.ci_instructor, int):
        raise HTTPException(status_code=400, detail="El ci_instructor debe ser un número entero.")
    if not isinstance(clase.id_actividad, int):
        raise HTTPException(status_code=400, detail="El id_actividad debe ser un número entero.")
    if not isinstance(clase.id_turno, int):
        raise HTTPException(status_code=400, detail="El id_turno debe ser un número entero.")
    if not isinstance(clase.dictada, bool):
        raise HTTPException(status_code=400, detail="El campo dictada debe ser un valor booleano.")

    new_clase = {
        "ci_instructor": clase.ci_instructor,
        "id_actividad": clase.id_actividad,
        "id_turno": clase.id_turno,
        "dictada": clase.dictada
    }
    try:
        db.execute(
            text("""
                INSERT INTO clase (ci_instructor, id_actividad, id_turno, dictada) 
                VALUES (:ci_instructor, :id_actividad, :id_turno, :dictada)
            """),
            new_clase
        )
        db.commit()
        return {"message": "Clase creada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear la clase: {str(e)}")


@clases.put("/clases/{id_clase}")
def update_clase(id_clase: int, clase: Clase, db: Session = Depends(get_db)):
    if not isinstance(id_clase, int):
        raise HTTPException(status_code=400, detail="El id_clase debe ser un número entero.")
    if not isinstance(clase.ci_instructor, int):
        raise HTTPException(status_code=400, detail="El ci_instructor debe ser un número entero.")
    if not isinstance(clase.id_actividad, int):
        raise HTTPException(status_code=400, detail="El id_actividad debe ser un número entero.")
    if not isinstance(clase.id_turno, int):
        raise HTTPException(status_code=400, detail="El id_turno debe ser un número entero.")
    if not isinstance(clase.dictada, bool):
        raise HTTPException(status_code=400, detail="El campo dictada debe ser un valor booleano.")

    updated_clase = {
        "id_clase": id_clase,
        "ci_instructor": clase.ci_instructor,
        "id_actividad": clase.id_actividad,
        "id_turno": clase.id_turno,
        "dictada": clase.dictada
    }
    try:
        db.execute(
            text("""
                UPDATE clase
                SET ci_instructor = :ci_instructor, 
                    id_actividad = :id_actividad, 
                    id_turno = :id_turno, 
                    dictada = :dictada
                WHERE id = :id_clase
            """),
            updated_clase
        )
        db.commit()
        return {"message": "Clase actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar la clase: {str(e)}")


@clases.delete("/clases/{id_clase}")
def delete_clase(id_clase: int, db: Session = Depends(get_db)):
    if not isinstance(id_clase, int):
        raise HTTPException(status_code=400, detail="El id_clase debe ser un número entero.")
    try:
        db.execute(
            text("""
                DELETE FROM clase
                WHERE id = :id_clase
            """),
            {"id_clase": id_clase}
        )
        db.commit()
        return {"message": "Clase eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar la clase: {str(e)}")
