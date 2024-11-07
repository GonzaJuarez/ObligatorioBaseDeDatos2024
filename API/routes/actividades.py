from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from API.config.database import SessionLocal
from API.config.db import connection
from API.models.actividades import model_actividad
from API.schemas.actividades import Actividades


actividades = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@actividades.get("/actividades")
async def get_actividades(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_actividad.select()).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@actividades.get("/actividades/{id_actividad}")
async def get_actividad_id(id_actividad: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_actividad.select().where(model_actividad.c.id == id_actividad)).first()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@actividades.post("/actividades")
def create_actividad(actividad: Actividades, db: Session = Depends(get_db)):
    new_actividad = {
        "descripcion": actividad.descripcion,
        "costo": actividad.costo
    }
    try:
        result = db.execute(model_actividad.insert().values(new_actividad))
        db.commit()
        print(result)
        return {"message": "Actividad creada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@actividades.put("/actividades/{id_actividad}")
def update_actividad(id_actividad: str, actividad: Actividades, db: Session = Depends(get_db)):
    new_actividad = {
        "id": id_actividad,
        "descripcion": actividad.descripcion,
        "costo": actividad.costo
    }
    try:
        db.execute(model_actividad.update().where(model_actividad.c.id == id_actividad).values(new_actividad))
        db.commit()
        return {"message": "Actividad actualizada exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@actividades.delete("/actividades/{id_actividad}")
def delete_actividad(id_actividad: str, db: Session = Depends(get_db)):
    try:
        db.execute(model_actividad.delete().where(model_actividad.c.id == id_actividad))
        db.commit()
        return {"message": "Actividad eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))
