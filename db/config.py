import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from utils.constants import DATABASE_URL

# Load environment variables from a .env file
load_dotenv()

# Configure the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for declarative models
Base = declarative_base()


def init_db():
    """
    Initialize the database by creating all tables defined in the models.

    This function uses SQLAlchemy's `Base.metadata.create_all` to ensure that all
    tables defined in the models are created in the database. It binds the operation
    to the configured engine.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Provide a scoped session for database operations.

    This function is designed to be used as a dependency in FastAPI endpoints to
    handle database operations. It ensures proper session management by closing
    the session once the operation is completed.

    Yields:
        Session: An SQLAlchemy session for interacting with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
