from flask import Flask
from sqlalchemy.exc import OperationalError
from flask_restful import Api
from app.extensions import db, migrate, jwt
from app.auth import User
from app.auth.resource import UserResource, LoginResource
from app.books import Book, Author, Genre, Condition, BookGenres
from app.books.resource import BooksResource
from app.configs import Config
import threading

initialized = False
initialization_lock = threading.Lock()


def create_app():
    app = Flask(__name__)

    global initialized
    with initialization_lock:
        if not initialized:
            app.config.from_object(Config)
            register_extensions(app)
            register_api(app)
            initialized = True

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Book": Book,
            "Author": Author,
            "Genre": Genre,
            "Condition": Condition,
            "config": Config,
        }

    return app


def register_extensions(app):
    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-JWT-Extended
    jwt.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except OperationalError as e:
            # Handle the OperationalError (database already exists)
            print(f"Database already exists: {e}")


def register_api(app):
    api = Api(app)
    api.add_resource(UserResource, "/auth/register")
    api.add_resource(LoginResource, "/auth/login")
    api.add_resource(
        BooksResource,
        "/api/books",
        "/api/books/<id>",
        "/api/books/genre/<genre>",
        "/api/books/author/<author>",
    )
