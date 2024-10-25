from fastapi import APIRouter
from config.db import connection
from models.clase import model_clase
from schemas.clase import Clase

clases = APIRouter()

@clases.get("/clases")
async def get_clases():
    result = connection.execute(model_clase.select()).fetchall()
    return [dict(row._mapping) for row in result]

@clases.get("/clases/{id_clase}")
def get_clase_id(id_clase: str):
    result = connection.execute(model_clase.select().where(model_clase.c.id == id_clase)).first()
    return dict(result._mapping)

@clases.post("/clases")
def create_clase(clase: Clase):
    new_clase = {
        "ci_instructor": clase.ci_instructor,
        "id_actividad": clase.id_actividad,
        "id_turno": clase.id_turno,
        "dictada": clase.dictada
    }
    try:
        result = connection.execute(model_clase.insert().values(new_clase))
        connection.commit()
        print(result)
        return {"message": "Clase creada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@clases.put("/clases/{id_clase}")
def update_clase(id_clase: str, clase: Clase):
    new_clase = {
        "id": id_clase,
        "ci_instructor": clase.ci_instructor,
        "id_actividad": clase.id_actividad,
        "id_turno": clase.id_turno,
        "dictada": clase.dictada
    }
    try:
        connection.execute(model_clase.update().where(model_clase.c.id == id_clase).values(new_clase))
        connection.commit()
        return {"message": "Clase actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@clases.delete("/clases/{id_clase}")
def delete_clase(id_clase: str):
    try:
        connection.execute(model_clase.delete().where(model_clase.c.id == id_clase))
        connection.commit()
        return {"message": "Clase eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))