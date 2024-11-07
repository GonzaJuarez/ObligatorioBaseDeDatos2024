from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from API.env import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE

engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
meta = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
