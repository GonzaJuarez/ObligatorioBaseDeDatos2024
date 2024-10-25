from fastapi import APIRouter
from config.db import connection
from models.login import model_login
from schemas.login import Login

login = APIRouter()

@login.get("/login")
def get_login():
    result = connection.execute(model_login.select()).fetchall()
    return [dict(row._mapping) for row in result]

@login.get("/login/{ci}")
def get_login_ci(ci: str):
    result = connection.execute(model_login.select().where(model_login.c.ci == ci)).first()
    return dict(result._mapping)

@login.post("/login")
def create_login(login1: Login):
    new_login = {
        "ci": login1.ci,
        "contraseña": login1.contraseña
    }
    try:
        result = connection.execute(model_login.insert().values(new_login))
        connection.commit()
        print(result)
        return {"message": "Login creado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@login.put("/login/{ci}")
def update_login(ci: str, login1: Login):
    new_login = {
        "ci": login1.ci,
        "contraseña": login1.contraseña
    }
    try:
        connection.execute(model_login.update().where(model_login.c.ci == ci).values(new_login))
        connection.commit()
        return {"message": "Login actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@login.delete("/login/{ci}")
def delete_login(ci: str):
    try:
        result = connection.execute(model_login.delete().where(model_login.c.ci == ci))
        connection.commit()
        return {"message": "Login eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
