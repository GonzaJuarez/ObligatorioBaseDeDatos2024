import dotenv
import os

dotenv.load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

ADMIN_CI = os.getenv("ADMIN_CI")
ADMIN_NOMBRE = os.getenv("ADMIN_NOMBRE")
ADMIN_APELLIDO = os.getenv("ADMIN_APELLIDO")
AMDIN_FECHA_NAC = os.getenv("ADMIN_FECHA_NAC")
ADMIN_CEL = os.getenv("ADMIN_CEL")
ADMIN_CORREO = os.getenv("ADMIN_CORREO")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")