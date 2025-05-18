import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta


# Load environment variables from .env file
load_dotenv()


class Config(object):
    # Flask-Smorest
    API_TITLE = "წიგნების მართვის API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    # Flask-JWT-Extended
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-dev-key-should-be-changed")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    PROJECT_NAME = "flask_books-api"
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    APP_ROOT = os.path.join(PROJECT_ROOT, "app")
    STATIC_FOLDER = os.path.join(APP_ROOT, "static")
    UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.join(STATIC_FOLDER, "uploads"))
    UPLOAD_EXTENSIONS = [".pdf", ".docx", ".epub", ".mobi"]
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    if FLASK_DEBUG is True or FLASK_DEBUG == "1" or FLASK_DEBUG == "True":
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(PROJECT_ROOT, "db.sqlite")
    else:
        POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
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
