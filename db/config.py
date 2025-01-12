import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

username = os.getenv('PSQL_USERNAME')
password = os.getenv('PSQL_PASSWORD')
host = os.getenv('PSQL_HOST')
port = os.getenv('PSQL_PORT')
database = os.getenv('PSQL_DB')

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_sessions():
    with SessionLocal as session:
        yield session
