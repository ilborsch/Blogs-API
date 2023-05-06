from dotenv import load_dotenv
import os

path_to_dotenv: str = os.path.dirname(os.path.abspath(__file__)) + "\\.env"
load_dotenv(dotenv_path=path_to_dotenv)

SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")
REDIS_HOST = os.environ.get("REDIS_HOST")
SECRET_JWT_KEY = os.environ.get("SECRET_JWT_KEY")
