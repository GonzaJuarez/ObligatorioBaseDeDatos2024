from fastapi import APIRouter
from config.db import connection
from models.actividades import model_actividad
from schemas.actividades import Actividades

actividades = APIRouter()

@actividades.get("/actividades")
async def get_actividades():
    result = connection.execute(model_actividad.select()).fetchall()
    return [dict(row._mapping) for row in result]

@actividades.get("/actividades/{id_actividad}")
def get_actividad_id(id_actividad: str):
    result = connection.execute(model_actividad.select().where(model_actividad.c.id == id_actividad)).first()
    return dict(result._mapping)

@actividades.post("/actividades")
def create_actividad(actividad: Actividades):
    new_actividad = {
        "descripcion": actividad.descripcion,
        "costo": actividad.costo
    }
    try:
        result = connection.execute(model_actividad.insert().values(new_actividad))
        connection.commit()
        print(result)
        return {"message": "Actividad creada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@actividades.put("/actividades/{id_actividad}")
def update_actividad(id_actividad: str, actividad: Actividades):
    new_actividad = {
        "id": id_actividad,
        "descripcion": actividad.descripcion,
        "costo": actividad.costo
    }
    try:
        connection.execute(model_actividad.update().where(model_actividad.c.id == id_actividad).values(new_actividad))
        connection.commit()
        return {"message": "Actividad actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))

@actividades.delete("/actividades/{id_actividad}")
def delete_actividad(id_actividad: str):
    try:
        connection.execute(model_actividad.delete().where(model_actividad.c.id == id_actividad))
        connection.commit()
        return {"message": "Actividad eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=str(e))
