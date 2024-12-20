from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from API.config.database import SessionLocal
from API.config.db import connection
from API.schemas.turnos import Turno

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
        result = db.execute(text("SELECT * FROM turnos")).fetchall()
        turnos = []
        for turno in result:
            turno = dict(turno._mapping)
            hora_inicio = turno["hora_inicio"]
            hora_fin = turno["hora_fin"]

            hora_inicio_seconds = hora_inicio.total_seconds()
            hora_fin_seconds = hora_fin.total_seconds()

            hora_inicio = f"{int(hora_inicio_seconds // 3600)}:{int((hora_inicio_seconds % 3600) // 60)}:{int(hora_inicio_seconds % 60)}"
            hora_fin = f"{int(hora_fin_seconds // 3600)}:{int((hora_fin_seconds % 3600) // 60)}:{int(hora_fin_seconds % 60)}"

            turno["hora_inicio"] = hora_inicio
            turno["hora_fin"] = hora_fin
            turnos.append(turno)
        return turnos
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@turnos.get("/turnos/{id_turno}")
def get_turno(id_turno: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT * FROM turnos
                WHERE id = :id
            """), {"id": id_turno}
        ).fetchone()
        turno = dict(result._mapping)
        hora_inicio = turno["hora_inicio"]
        hora_fin = turno["hora_fin"]
        hora_inicio_seconds = hora_inicio.total_seconds()
        hora_fin_seconds = hora_fin.total_seconds()
        turno[
            "hora_inicio"] = f"{int(hora_inicio_seconds // 3600)}:{int((hora_inicio_seconds % 3600) // 60)}:{int(hora_inicio_seconds % 60)}"
        turno[
            "hora_fin"] = f"{int(hora_fin_seconds // 3600)}:{int((hora_fin_seconds % 3600) // 60)}:{int(hora_fin_seconds % 60)}"
        return turno
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@turnos.post("/turnos")
def post_turno(turno: Turno, db: Session = Depends(get_db)):
    if not isinstance(turno.hora_inicio, str):
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser un string de tipo hh:mm:ss")
    if not isinstance(turno.hora_fin, str):
        raise HTTPException(status_code=400, detail="La hora de fin debe ser un string de tipo hh:mm:ss")
    new_turno = {
        "hora_inicio": turno.hora_inicio,
        "hora_fin": turno.hora_fin
    }
    try:
        db.execute(
            text("""
                INSERT INTO turnos (hora_inicio, hora_fin) 
                VALUES (:hora_inicio, :hora_fin)
            """), new_turno)
        db.commit()
        return {"message": "Turno creado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@turnos.put("/turnos/{id_turno}")
def put_turno(id_turno: int, turno: Turno, db: Session = Depends(get_db)):
    if not isinstance(id_turno, int):
        raise HTTPException(status_code=400, detail="El id del turno debe ser un entero")
    if not isinstance(turno.hora_inicio, str):
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser un string de tipo hh:mm:ss")
    if not isinstance(turno.hora_fin, str):
        raise HTTPException(status_code=400, detail="La hora de fin debe ser un string de tipo hh:mm:ss")
    new_turno = {
        "id": id_turno,
        "hora_inicio": turno.hora_inicio,
        "hora_fin": turno.hora_fin
    }
    try:
        db.execute(
            text("""
                UPDATE turnos
                SET hora_inicio = :hora_inicio, hora_fin = :hora_fin
                WHERE id = :id
            """), new_turno
        )
        db.commit()
        return {"message": "Turno actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@turnos.delete("/turnos/{id_turno}")
def delete_turno(id_turno: int, db: Session = Depends(get_db)):
    if not isinstance(id_turno, int):
        raise HTTPException(status_code=400, detail="El id del turno debe ser un entero")
    try:
        db.execute(
            text("""
                DELETE FROM turnos
                WHERE id = :id
            """), {"id": id_turno}
        )
        db.commit()
        return {"message": "Turno eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))
