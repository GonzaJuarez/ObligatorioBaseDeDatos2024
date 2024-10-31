from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import dotenv
import os

dotenv.load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
meta = MetaData()

# Crea la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
