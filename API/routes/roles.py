from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException
from config.database import SessionLocal
from config.db import connection
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
        result = db.execute(text("SELECT * FROM roles"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@Roles.get("/roles/{rol_id}")
def get_rol(rol_id: int, db: Session = Depends(get_db)):
    if not isinstance(rol_id, int):
        raise HTTPException(status_code=400, detail="El id del rol debe ser un número entero")
    try:
        result = db.execute(
            text("""
            SELECT * FROM roles WHERE id = :id
            """),
            {"id": rol_id}).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def get_rol_by_desc(rol_desc: str, db: Session = Depends(get_db)):
    if not isinstance(rol_desc, str):
        raise HTTPException(status_code=400, detail="La descripción del rol debe ser una cadena de texto")
    try:
        result = db.execute(
            text("""
            SELECT * FROM roles WHERE descripcion = :descripcion
            """),
            {"descripcion": rol_desc}).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@Roles.post("/roles")
def create_rol(rol: Rol, db: Session = Depends(get_db)):
    if not isinstance(rol.descripcion, str):
        raise HTTPException(status_code=400, detail="La descripción del rol debe ser una cadena de texto")
    new_rol = {
        "descripcion": rol.descripcion
    }
    try:
        result = db.execute(
            text("""
            INSERT INTO roles (descripcion) VALUES (:descripcion)
            """), new_rol)
        db.commit()
        print(result)
        return {"message": "Rol creada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@Roles.put("/roles/{rol_id}")
def update_rol(rol_id: int, rol: Rol, db: Session = Depends(get_db)):
    if not isinstance(rol_id, int):
        raise HTTPException(status_code=400, detail="El id del rol debe ser un número entero")
    updated_rol = {
        "id": rol_id,
        "descripcion": rol.descripcion
    }
    try:
        db.execute(
            text("""
            UPDATE roles SET descripcion = :descripcion WHERE id = :id
            """), updated_rol
        )
        db.commit()
        return {"message": "Rol actualizada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@Roles.delete("/roles/{rol_id}")
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    if not isinstance(rol_id, int):
        raise HTTPException(status_code=400, detail="El id del rol debe ser un número entero")
    try:
        db.execute(
            text("""
            DELETE FROM roles WHERE id = :id
            """), {"id": rol_id}
        )
        db.commit()
        return {"message": "Rol eliminada exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))