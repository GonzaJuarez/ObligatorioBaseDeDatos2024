from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from API.config.database import SessionLocal
from API.config.db import connection
from API.models.clase import model_clase
from API.schemas.clase import Clase

clases = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@clases.get("/clases")
async def get_clases(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_clase.select()).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@clases.get("/clases/{id_clase}")
def get_clase_id(id_clase: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_clase.select().where(model_clase.c.id == id_clase)).first()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@clases.post("/clases")
def create_clase(clase: Clase, db: Session = Depends(get_db)):
    new_clase = {
        "ci_instructor": clase.ci_instructor,
        "id_actividad": clase.id_actividad,
        "id_turno": clase.id_turno,
        "dictada": clase.dictada
    }
    try:
        result = db.execute(model_clase.insert().values(new_clase))
        db.commit()
        print(result)
        return {"message": "Clase creada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@clases.put("/clases/{id_clase}")
def update_clase(id_clase: str, clase: Clase, db: Session = Depends(get_db)):
    new_clase = {
        "id": id_clase,
        "ci_instructor": clase.ci_instructor,
        "id_actividad": clase.id_actividad,
        "id_turno": clase.id_turno,
        "dictada": clase.dictada
    }
    try:
        db.execute(model_clase.update().where(model_clase.c.id == id_clase).values(new_clase))
        db.commit()
        return {"message": "Clase actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@clases.delete("/clases/{id_clase}")
def delete_clase(id_clase: str, db: Session = Depends(get_db)):
    try:
        db.execute(model_clase.delete().where(model_clase.c.id == id_clase))
        db.commit()
        return {"message": "Clase eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))