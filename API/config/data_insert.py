from config.db import connection, meta, engine
from sqlalchemy import text

from config.hashing import Hasher

from env import ADMIN_CI, ADMIN_NOMBRE, ADMIN_APELLIDO, AMDIN_FECHA_NAC, ADMIN_CEL, ADMIN_CORREO, ADMIN_PASSWORD


def insert_data():
    with (engine.begin() as connection):
        # Roles
        connection.execute(text("REPLACE INTO roles (descripcion) VALUES ('Administrador')"))
        connection.execute(text("REPLACE INTO roles (descripcion) VALUES ('Instructor')"))
        connection.execute(text("REPLACE INTO roles (descripcion) VALUES ('Alumno')"))

        # Administrador
        admin_rol_id = connection.execute(text("SELECT * FROM roles WHERE descripcion = 'Administrador'")).first()[
            0]
        admin = {
            "ci": ADMIN_CI,
            "id_rol": admin_rol_id,
            "nombre": ADMIN_NOMBRE,
            "apellido": ADMIN_APELLIDO,
            "fecha_nacimiento": AMDIN_FECHA_NAC,
            "cel": ADMIN_CEL,
            "correo": ADMIN_CORREO
        }
        connection.execute(
            text("""
                INSERT INTO personas (ci, id_rol, nombre, apellido, fecha_nacimiento, cel, correo)
                VALUES (:ci, :id_rol, :nombre, :apellido, :fecha_nacimiento, :cel, :correo)
                ON DUPLICATE KEY UPDATE
                    id_rol = VALUES(id_rol),
                    nombre = VALUES(nombre),
                    apellido = VALUES(apellido),
                    fecha_nacimiento = VALUES(fecha_nacimiento),
                    cel = VALUES(cel),
                    correo = VALUES(correo);
            """), admin)

        # Login Administrador
        connection.execute(
            text("""
                REPLACE INTO login (ci, contraseña)
                VALUES (:ci, :password)
            """), {"ci": ADMIN_CI, "password": Hasher.get_password_hash(ADMIN_PASSWORD)})

        # Actividades
        connection.execute(text("REPLACE INTO actividades (descripcion, costo) VALUES ('Snowboard', 200)"))
        connection.execute(text("REPLACE INTO actividades (descripcion, costo) VALUES ('Sky', 200)"))
        connection.execute(text("REPLACE INTO actividades (descripcion, costo) VALUES ('Moto de Nieve', 200)"))

        # Equipamientos
        actividad_snowboard_id = connection.execute(
            text("SELECT * FROM actividades WHERE descripcion = 'Snowboard'")).first()[0]
        actividad_sky_id = connection.execute(text("SELECT * FROM actividades WHERE descripcion = 'Sky'")).first()[0]
        actividad_moto_de_nieve_id = connection.execute(
            text("SELECT * FROM actividades WHERE descripcion = 'Moto de Nieve'")).first()[0]

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_snowboard_id}, 'Tabla de Snowboard', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_snowboard_id}, 'Botas de Snowboard', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_snowboard_id}, 'Casco de Snowboard', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_snowboard_id}, 'Lentes de Snowboard', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_sky_id}, 'Esquies', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_sky_id}, 'Botas de Sky', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_sky_id}, 'Casco de Sky', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_sky_id}, 'Lentes de Sky', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_moto_de_nieve_id}, 'Moto de Nieve', 100)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_moto_de_nieve_id}, 'Casco de Moto de Nieve', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_moto_de_nieve_id}, 'Lentes de Moto de Nieve', 50)
                """))

        connection.execute(
            text(f"""REPLACE INTO equipamiento (id_actividad, descripcion, costo)
                VALUES ({actividad_moto_de_nieve_id}, 'Botas de Moto de Nieve', 50)
                """))

        # Turnos
        connection.execute(text("REPLACE INTO turnos (hora_inicio, hora_fin) VALUES ('09:00:00', '10:00:00')"))
        connection.execute(text("REPLACE INTO turnos (hora_inicio, hora_fin) VALUES ('10:00:00', '11:00:00')"))
        connection.execute(text("REPLACE INTO turnos (hora_inicio, hora_fin) VALUES ('11:00:00', '12:00:00')"))



        connection.commit()
