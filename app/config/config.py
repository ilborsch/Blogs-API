import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
PGADMIN_EMAIL = os.environ.get("PGADMIN_EMAIL")
PGADMIN_PASSWORD = os.environ.get("PGADMIN_PASSWORD")
DATABASE_URL = os.environ.get("DATABASE_URL")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
