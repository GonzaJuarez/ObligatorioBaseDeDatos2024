from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from config.database import SessionLocal
from config.db import connection
from models.turnos import model_turno
from schemas.turnos import Turno

turnos = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@turnos.get("/turnos")
def get_turnos(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_turno.select()).fetchall()
        turnos_list = []
        for row in result:
            turno = dict(row._mapping)
            if turno["hora_inicio"] is not None:
                turno["hora_inicio"] = turno["hora_inicio"] / 3600
            if turno["hora_fin"] is not None:
                turno["hora_fin"] = turno["hora_fin"] / 3600
            turnos_list.append(turno)
        return turnos_list
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@turnos.get("/turnos/{id}")
def get_turno(id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_turno.select().where(model_turno.c.id == id)).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@turnos.post("/turnos")
def post_turno(turno: Turno, db: Session = Depends(get_db)):
    new_turno = {
        "hora_inicio": turno.hora_inicio,
        "hora_fin": turno.hora_fin
    }
    try:
        db.execute(model_turno.insert().values(new_turno))
        db.commit()
        return {"message": "Turno creado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@turnos.put("/turnos/{id_turno}")
def put_turno(id_turno: int, turno: Turno, db: Session = Depends(get_db)):
    new_turno = {
        "id": id_turno,
        "hora_inicio": turno.hora_inicio,
        "hora_fin": turno.hora_fin
    }
    try:
        db.execute(model_turno.update().where(model_turno.c.id == id).values(new_turno))
        db.commit()
        return {"message": "Turno actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))

@turnos.delete("/turnos/{id_turno}")
def delete_turno(id_turno: int, db: Session = Depends(get_db)):
    try:
        db.execute(model_turno.delete().where(model_turno.c.id == id_turno))
        db.commit()
        return {"message": "Turno eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))
