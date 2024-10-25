from fastapi import APIRouter
from config.db import connection
from models.alumno_clase import model_alumno_clase
from schemas.alumno_clase import Alumno_clase

alumno_clase = APIRouter()

@alumno_clase.get("/alumno_clase")
def get_alumno_clase():
    result = connection.execute(model_alumno_clase.select()).fetchall()
    return [dict(row._mapping) for row in result]

@alumno_clase.get("/alumno_clase/{ci_alumno}")
def get_alumno_clase_ci(ci_alumno: int):
    result = connection.execute(model_alumno_clase.select().where(model_alumno_clase.c.ci_alumno == ci_alumno)).first()
    return dict(result._mapping)

@alumno_clase.post("/alumno_clase")
def create_alumno_clase(alumno_clase1: Alumno_clase):
    new_alumno_clase = {
        "id_clase": alumno_clase1.id_clase,
        "ci_alumno": alumno_clase1.ci_alumno,
        "id_equipamiento": alumno_clase1.id_equipamiento
    }
    try:
        result = connection.execute(model_alumno_clase.insert().values(new_alumno_clase))
        connection.commit()
        print(result)
        return {"message": "Alumno_clase creado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@alumno_clase.put("/alumno_clase/{ci_alumno}")
def update_alumno_clase(ci_alumno: int, alumno_clase1: Alumno_clase):
    new_alumno_clase = {
        "id_clase": alumno_clase1.id_clase,
        "ci_alumno": alumno_clase1.ci_alumno,
        "id_equipamiento": alumno_clase1.id_equipamiento
    }
    try:
        connection.execute(model_alumno_clase.update().where(model_alumno_clase.c.ci_alumno == ci_alumno).values(new_alumno_clase))
        connection.commit()
        return {"message": "Alumno_clase actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@alumno_clase.delete("/alumno_clase/{ci_alumno}")
def delete_alumno_clase(ci_alumno: int):
    try:
        connection.execute(model_alumno_clase.delete().where(model_alumno_clase.c.ci_alumno == ci_alumno))
        connection.commit()
        return {"message": "Alumno_clase eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))