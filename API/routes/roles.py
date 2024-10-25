from fastapi import APIRouter
from config.db import connection
from models.roles import model_roles
from schemas.roles import Rol

Roles = APIRouter()

@Roles.get("/roles")
def get_roles():
    result = connection.execute(model_roles.select()).fetchall()
    return [dict(row._mapping) for row in result]

@Roles.get("/roles/{rol_id}")
def get_rol(rol_id: int):
    result = connection.execute(model_roles.select().where(model_roles.c.id == rol_id)).first()
    return dict(result._mapping)

@Roles.post("/roles")
def create_rol(rol: Rol):
    new_rol = {
        "descripcion": rol.descripcion
    }
    try:
        result = connection.execute(model_roles.insert().values(new_rol))
        connection.commit()  # Explicitly commit the transaction
        print(result)
        return {"message": "Rol creada exitosamente"}
    except Exception as e:
        connection.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))

@Roles.put("/roles/{rol_id}")
def update_rol(rol_id: int, rol: Rol):
    new_rol = {
        "descripcion": rol.descripcion
    }
    try:
        connection.execute(model_roles.update().where(model_roles.c.id == rol_id).values(new_rol))
        connection.commit()
        return {"message": "Rol actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@Roles.delete("/roles/{rol_id}")
def delete_rol(rol_id: int):
    try:
        result = connection.execute(model_roles.delete().where(model_roles.c.id == rol_id))
        connection.commit()
        return {"message": "Rol eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))