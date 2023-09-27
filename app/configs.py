import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config(object):
    PROJECT_NAME = "flask_books-api"
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    APP_ROOT = os.path.join(PROJECT_ROOT, "app")
    STATIC_FOLDER = os.path.join(APP_ROOT, "static")
    UPLOAD_DIR = os.environ.get(
        "UPLOAD_DIR",
        os.path.join(APP_ROOT, "/static/uploads")
    )
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    if FLASK_DEBUG is True or FLASK_DEBUG == "1" or FLASK_DEBUG == "True":
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            PROJECT_ROOT, "db.sqlite"
        )
    else:
        POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
        # print(POSTGRES_HOST)
        POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
        POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
        POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
        POSTGRES_DB = os.environ.get("POSTGRES_DB", "books")
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://\
            {POSTGRES_USER}:\
            {POSTGRES_PASSWORD}@\
            {POSTGRES_HOST}:\
            {POSTGRES_PORT}/\
            {POSTGRES_DB}".replace(
            " ", ""
        )
    SECRET_KEY = os.environ.get("SECRET_KEY") or "asd;lkajs-90 as;doaksdasd0/A"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
