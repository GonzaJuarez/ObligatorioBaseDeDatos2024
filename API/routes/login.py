from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from config.database import SessionLocal
from config.db import connection
from models.login import model_login
from schemas.login import Login

login = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@login.get("/login")
def get_login(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_login.select()).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.get("/login/{ci}")
def get_login_ci(ci: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_login.select().where(model_login.c.ci == ci)).first()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.post("/login")
def create_login(login1: Login, db: Session = Depends(get_db)):
    new_login = {
        "ci": login1.ci,
        "contraseña": login1.contraseña
    }
    try:
        result = db.execute(model_login.insert().values(new_login))
        db.commit()
        print(result)
        return {"message": "Login creado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.put("/login/{ci}")
def update_login(ci: str, login1: Login, db: Session = Depends(get_db)):
    new_login = {
        "ci": login1.ci,
        "contraseña": login1.contraseña
    }
    try:
        db.execute(model_login.update().where(model_login.c.ci == ci).values(new_login))
        db.commit()
        return {"message": "Login actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.delete("/login/{ci}")
def delete_login(ci: str, db: Session = Depends(get_db)):
    try:
        db.execute(model_login.delete().where(model_login.c.ci == ci))
        db.commit()
        return {"message": "Login eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
