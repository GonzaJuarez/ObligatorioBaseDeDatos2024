from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from API.config.database import SessionLocal
from API.config.db import connection
from API.models.alumno_clase import model_alumno_clase
from API.schemas.alumno_clase import Alumno_clase

alumno_clase = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@alumno_clase.get("/alumno_clase")
def get_alumno_clase(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_alumno_clase.select()).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@alumno_clase.get("/alumno_clase/{ci_alumno}")
def get_alumno_clase_ci(ci_alumno: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_alumno_clase.select().where(model_alumno_clase.c.ci_alumno == ci_alumno)).first()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@alumno_clase.post("/alumno_clase")
def create_alumno_clase(alumno_clase1: Alumno_clase, db: Session = Depends(get_db)):
    new_alumno_clase = {
        "id_clase": alumno_clase1.id_clase,
        "ci_alumno": alumno_clase1.ci_alumno,
        "id_equipamiento": alumno_clase1.id_equipamiento
    }
    try:
        result = db.execute(model_alumno_clase.insert().values(new_alumno_clase))
        db.commit()
        print(result)
        return {"message": "Alumno_clase creado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@alumno_clase.put("/alumno_clase/{ci_alumno}")
def update_alumno_clase(ci_alumno: int, alumno_clase1: Alumno_clase, db: Session = Depends(get_db)):
    new_alumno_clase = {
        "id_clase": alumno_clase1.id_clase,
        "ci_alumno": alumno_clase1.ci_alumno,
        "id_equipamiento": alumno_clase1.id_equipamiento
    }
    try:
        db.execute(model_alumno_clase.update().where(model_alumno_clase.c.ci_alumno == ci_alumno).values(new_alumno_clase))
        db.commit()
        return {"message": "Alumno_clase actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@alumno_clase.delete("/alumno_clase/{ci_alumno}")
def delete_alumno_clase(ci_alumno: int, db: Session = Depends(get_db)):
    try:
        db.execute(model_alumno_clase.delete().where(model_alumno_clase.c.ci_alumno == ci_alumno))
        db.commit()
        return {"message": "Alumno_clase eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))