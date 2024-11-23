from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from API.config.database import SessionLocal
from API.config .db import connection


reportes = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@reportes.get("/activiades_mas_ganancias")
def get_actividades_mas_ganancias(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("""
        SELECT 
            a.descripcion AS actividad,
            (SUM(e.costo) + a.costo * COUNT(ac.id_alumno)) AS ingresos
        FROM actividades a
        LEFT JOIN clase c ON a.id = c.id_actividad
        LEFT JOIN alumno_clase ac ON c.id = ac.id_clase
        LEFT JOIN equipamiento e ON ac.id_equipo = e.id
        GROUP BY a.id
        ORDER BY ingresos DESC;
        """)).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@reportes.get("/actividades_mas_alumnos")
def get_actividades_mas_alumnos(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("""
        SELECT 
            a.descripcion AS actividad,
            COUNT(DISTINCT ac.id_alumno) AS cantidad_alumnos
        FROM actividades a
        LEFT JOIN clase c ON a.id = c.id_actividad
        LEFT JOIN alumno_clase ac ON c.id = ac.id_clase
        GROUP BY a.id
        ORDER BY cantidad_alumnos DESC;
        """)).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))


@reportes.get("/turnos_mas_dictados")
def get_turnos_mas_dictados(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("""
        SELECT 
            t.hora_inicio AS inicio_turno,
            t.hora_fin AS fin_turno,
            COUNT(c.id) AS total_clases
        FROM turnos t
        LEFT JOIN clase c ON t.id = c.id_turno
        GROUP BY t.id
        ORDER BY total_clases DESC;
        """)).fetchone()
        return dict(result._mapping)
    except Exception as e:
        connection.rollback()
        return HTTPException(status_code=400, detail=str(e))




