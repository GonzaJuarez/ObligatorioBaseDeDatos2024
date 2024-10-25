from fastapi import APIRouter
from config.db import connection
from models.equipamiento import model_equipamiento
from schemas.equipamiento import Equipamiento

equipamiento = APIRouter()

@equipamiento.get("/equipamiento")
async def get_equipamiento():
    result = connection.execute(model_equipamiento.select()).fetchall()
    return [dict(row._mapping) for row in result]

@equipamiento.get("/equipamiento/{id}")
async def get_equipamiento(id: int):
    result = connection.execute(model_equipamiento.select().where(model_equipamiento.c.id == id)).fetchone()
    return dict(result._mapping)

@equipamiento.post("/equipamiento")
def post_equipamiento(equipamiento1: Equipamiento):
    new_equipamiento = {
        "id_actividad": equipamiento1.id_actividad,
        "descripcion": equipamiento1.descripcion,
        "costo": equipamiento1.costo
    }
    try:
        connection.execute(model_equipamiento.insert().values(new_equipamiento))
        connection.commit()
        return {"message": "Equipamiento creado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@equipamiento.put("/equipamiento/{id}")
def put_equipamiento(id: int, equipamiento1: Equipamiento):
    new_equipamiento = {
        "id": id,
        "id_actividad": equipamiento1.id_actividad,
        "descripcion": equipamiento1.descripcion,
        "costo": equipamiento1.costo
    }
    try:
        connection.execute(model_equipamiento.update().where(model_equipamiento.c.id == id).values(new_equipamiento))
        connection.commit()
        return {"message": "Equipamiento actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@equipamiento.delete("/equipamiento/{id}")
def delete_equipamiento(id: int):
    try:
        connection.execute(model_equipamiento.delete().where(model_equipamiento.c.id == id))
        connection.commit()
        return {"message": "Equipamiento eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))