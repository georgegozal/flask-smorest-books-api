from flask import Flask
from flask_restful import Api
from app.extensions import db, migrate, jwt
from app.auth import User
from app.auth.resource import UserResource, LoginResource
from app.books import Book, Author, Genre, Condition, BookGenres
from app.books.resource import BooksResource
from app.configs import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_api(app)

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
        db.create_all()


def register_api(app):
    api = Api(app)
    api.add_resource(UserResource, "/auth/register")
    api.add_resource(LoginResource, "/auth/login")
    api.add_resource(BooksResource, "/api/books", "/api/books/genre/<genre>")
