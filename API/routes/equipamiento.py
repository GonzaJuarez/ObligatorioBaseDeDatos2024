from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from config.database import SessionLocal
from config.db import connection
from models.equipamiento import model_equipamiento
from schemas.equipamiento import Equipamiento

equipamiento = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@equipamiento.get("/equipamiento")
async def get_equipamiento(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_equipamiento.select()).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@equipamiento.get("/equipamiento/{id}")
async def get_equipamiento(id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_equipamiento.select().where(model_equipamiento.c.id == id)).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@equipamiento.post("/equipamiento")
def post_equipamiento(equipamiento1: Equipamiento, db: Session = Depends(get_db)):
    new_equipamiento = {
        "id_actividad": equipamiento1.id_actividad,
        "descripcion": equipamiento1.descripcion,
        "costo": equipamiento1.costo
    }
    try:
        db.execute(model_equipamiento.insert().values(new_equipamiento))
        db.commit()
        return {"message": "Equipamiento creado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@equipamiento.put("/equipamiento/{id}")
def put_equipamiento(id: int, equipamiento1: Equipamiento, db: Session = Depends(get_db)):
    new_equipamiento = {
        "id": id,
        "id_actividad": equipamiento1.id_actividad,
        "descripcion": equipamiento1.descripcion,
        "costo": equipamiento1.costo
    }
    try:
        db.execute(model_equipamiento.update().where(model_equipamiento.c.id == id).values(new_equipamiento))
        db.commit()
        return {"message": "Equipamiento actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@equipamiento.delete("/equipamiento/{id}")
def delete_equipamiento(id: int, db: Session = Depends(get_db)):
    try:
        db.execute(model_equipamiento.delete().where(model_equipamiento.c.id == id))
        db.commit()
        return {"message": "Equipamiento eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))