from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from config.database import SessionLocal
from config.db import connection
from config.hashing import Hasher
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
        result = db.execute(text(" SELECT * FROM login"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.get("/login/{ci}")
def get_login_ci(ci: int, db: Session = Depends(get_db)):
    if not isinstance(ci, int):
        raise HTTPException(status_code=400, detail="El ci debe ser un número entero")
    try:
        result = db.execute(
            text("""
                SELECT * FROM login WHERE ci = :ci ORDER BY ci DESC LIMIT 1
            """),
            {"ci": ci}).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.post("/login")
def create_login(login1: Login, db: Session = Depends(get_db)):
    if not isinstance(login1.ci, int):
        raise HTTPException(status_code=400, detail="El ci debe ser un número entero")
    if not isinstance(login1.contraseña, str):
        raise HTTPException(status_code=400, detail="La contraseña debe ser una cadena de texto")
    new_login = {
        "ci": login1.ci,
        "contraseña": Hasher.get_password_hash(login1.contraseña)
    }
    try:
        db.execute(
            text("""
                INSERT INTO login (ci, contraseña)
                VALUES (:ci, :contraseña)
            """),
            new_login
        )
        db.commit()
        return {"message": "Login creado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.put("/login/{ci}")
def update_login(ci: int, login1: Login, db: Session = Depends(get_db)):
    if not isinstance(ci, int):
        raise HTTPException(status_code=400, detail="El ci debe ser un número entero ")
    if not isinstance(login1.contraseña, str):
        raise HTTPException(status_code=400, detail="La contraseña debe ser una cadena de texto")
    updated_login = {
        "ci": ci,
        "contraseña": Hasher.get_password_hash(login1.contraseña)
    }
    try:
        db.execute(
            text("""
                UPDATE login SET ci = :ci, contraseña = :contraseña WHERE ci = :ci
            """),
            updated_login
        )
        db.commit()
        return {"message": "Login actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@login.delete("/login/{ci}")
def delete_login(ci: int, db: Session = Depends(get_db)):
    if not isinstance(ci, int):
        raise HTTPException(status_code=400, detail="El ci debe ser un número entero")
    try:
        db.execute(
            text("""
                DELETE FROM login WHERE ci = :ci
            """),
            {"ci": ci}
        )
        db.commit()
        return {"message": "Login eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@login.post("/login/confirm")
def confirm_login(login1: Login, db: Session = Depends(get_db)):
    if not isinstance(login1.ci, int):
        raise HTTPException(status_code=400, detail="El ci debe ser un número entero")
    if not isinstance(login1.contraseña, str):
        raise HTTPException(status_code=400, detail="La contraseña debe ser una cadena de texto")
    try:
        result = db.execute(
            text("""
                SELECT * FROM login WHERE ci = :ci
            """),
            {"ci": login1.ci}
        ).fetchone()
        if result is None:
            return {"message": "Usuario no encontrado"}
        if Hasher.verify_password(login1.contraseña, result.contraseña):
            return {"message": "Login exitoso"}
        return {"message": "Contraseña incorrecta"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
