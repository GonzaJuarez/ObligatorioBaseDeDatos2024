from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from API.config.database import SessionLocal
from sqlalchemy import text
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuraciones de JWT
SECRET_KEY = "mi_clave_secreta_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuraciones de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/confirm")

# Router de FastAPI para las rutas de login
login = APIRouter()

# Modelo de Pydantic para la solicitud de login
class Login(BaseModel):
    correo: str
    contrasena: str

# Funciones para manejar contrasenas
class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

# Crear el token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint para registrar un nuevo usuario
@login.post("/login/register")
def register_login(login_data: Login, db: Session = Depends(get_db)):
    try:
        # Verificar si el usuario ya existe
        result = db.execute(
            text("SELECT * FROM login WHERE correo = :correo"),
            {"correo": login_data.correo}
        ).fetchone()

        if result:
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        # Crear un nuevo usuario
        db.execute(
            text("INSERT INTO login (correo, contrasena) VALUES (:correo, :contrasena)"),
            {"correo": login_data.correo, "contrasena": Hasher.hash_password(login_data.contrasena)}
        )
        db.commit()

        return {"message": "Usuario registrado exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint para confirmar el login y generar un token JWT
@login.post("/login/confirm")
def confirm_login(login_data: Login, db: Session = Depends(get_db)):
    try:
        # Consultar la base de datos para verificar el correo
        result = db.execute(
            text("SELECT * FROM login WHERE correo = :correo"),
            {"correo": login_data.correo}
        ).fetchone()
        
        if result is None:
            raise HTTPException(status_code=400, detail="Usuario no encontrado")

        # Verificar la contrasena
        if not Hasher.verify_password(login_data.contrasena, result.contrasena):
            raise HTTPException(status_code=400, detail="contrasena incorrecta")

        # Obtener información adicional del rol del usuario
        persona_result = db.execute(
            text("SELECT id_rol FROM personas WHERE correo = :correo"),
            {"correo": login_data.correo}
        ).fetchone()
        
        if persona_result is None:
            raise HTTPException(status_code=400, detail="No se encontró la información de la persona")

        id_rol = persona_result.id_rol

        # Generar el token JWT incluyendo el rol del usuario
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(result.correo), "rol": id_rol},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Dependencia para obtener el usuario actual basado en el token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        rol: int = payload.get("rol")
        if correo is None or rol is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"correo": correo, "rol": rol}

# Dependencia para verificar el rol del usuario
def verify_role(required_roles: list, current_user: dict = Depends(get_current_user)):
    if current_user["rol"] not in required_roles:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este recurso")
    return current_user

# Endpoint protegido que utiliza el usuario actual
@login.get("/datos_personales")
def datos_personales(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Consultar la base de datos para obtener los datos de la persona
    result = db.execute(
        text("SELECT * FROM personas WHERE correo = :correo"),
        {"correo": current_user["correo"]}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Retornar los datos de la persona
    return {
        "correo": result.correo,
        "nombre": result.nombre,
        "apellido": result.apellido,
        "cel": result.cel,
        "rol": current_user["rol"]
    }

# Endpoint protegido para instructores/administradores
@login.get("/datos_instructores")
def datos_instructores(current_user: dict = Depends(lambda: verify_role([1, 2], get_current_user())), db: Session = Depends(get_db)):
    # Consultar datos específicos para instructores o administradores
    return {"message": "Bienvenido, tienes acceso como administrador"}

# Endpoint protegido solo para alumnos
@login.get("/datos_alumnos")
def datos_alumnos(current_user: dict = Depends(lambda: verify_role([3], get_current_user())), db: Session = Depends(get_db)):
    # Consultar datos específicos para alumnos
    return {"message": "Bienvenido, tienes acceso como alumno"}
