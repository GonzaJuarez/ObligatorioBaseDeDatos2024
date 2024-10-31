from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from config.database import SessionLocal
from config.db import connection
from models.roles import model_roles
from schemas.roles import Rol

Roles = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@Roles.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    try:
        result = db.execute(model_roles.select()).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@Roles.get("/roles/{rol_id}")
def get_rol(rol_id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(model_roles.select().where(model_roles.c.id == rol_id)).first()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@Roles.post("/roles")
def create_rol(rol: Rol, db: Session = Depends(get_db)):
    new_rol = {
        "descripcion": rol.descripcion
    }
    try:
        result = db.execute(model_roles.insert().values(new_rol))
        db.commit()  # Explicitly commit the transaction
        print(result)
        return {"message": "Rol creada exitosamente"}
    except Exception as e:
        connection.rollback()  # Rollback in case of error
        raise HTTPException(status_code=400, detail=str(e))

@Roles.put("/roles/{rol_id}")
def update_rol(rol_id: int, rol: Rol, db: Session = Depends(get_db)):
    new_rol = {
        "descripcion": rol.descripcion
    }
    try:
        db.execute(model_roles.update().where(model_roles.c.id == rol_id).values(new_rol))
        db.commit()
        return {"message": "Rol actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@Roles.delete("/roles/{rol_id}")
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    try:
        db.execute(model_roles.delete().where(model_roles.c.id == rol_id))
        db.commit()
        return {"message": "Rol eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))