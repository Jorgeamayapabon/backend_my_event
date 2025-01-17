import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()

# Database
DB_USERNAME = os.getenv('PSQL_USERNAME')
DB_PASSWORD = os.getenv('PSQL_PASSWORD')
DB_HOST = os.getenv('PSQL_HOST')
DB_PORT = os.getenv('PSQL_PORT')
DB_NAME = os.getenv('PSQL_DB')
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# JWT
SECRET_KEY: Final[str] = os.getenv("SECRET_KEY")
ALGORITHM: Final[str] = os.getenv("ALGORITHM")
