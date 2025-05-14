from flask import Flask, jsonify
from sqlalchemy.exc import OperationalError
from flask_smorest import Api
from app.extensions import db, migrate, jwt
from app.auth import User
# from app.auth.resource import UserResource, LoginResource
from app.books import Book, Author, Genre, Condition, BookGenres
# from app.books.resource import BooksResource
from app.configs import Config
import threading

from app.auth.resource import blp as AuthBlueprint
from app.books.resource import blp as BookBlueprint

initialized = False
initialization_lock = threading.Lock()
BLUEPRINTS = [AuthBlueprint, BookBlueprint]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api = Api(app)
    register_extensions(app)
    register_blueprints(api)

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
    # JWT კონფიგურაცია
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "ტოკენს ვადა გაუვიდა", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "ვერიფიკაცია წარუმატებელია", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "ავტორიზაციის ტოკენი არ მოიძებნა",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    return app


def register_extensions(app):
    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-JWT-Extended
    jwt.init_app(app)

    # მონაცემთა ბაზის შექმნა პირველი გაშვებისას
    # @app.before_first_request
    def create_tables():
        global initialized
        with initialization_lock:
            if not initialized:
                initialized = True
            with app.app_context():
                try:
                    db.create_all()
                except OperationalError as e:
                    # Handle the OperationalError (database already exists)
                    print(f"Database already exists: {e}")
    create_tables()


def register_blueprints(api):
    for blueprint in BLUEPRINTS:
        api.register_blueprint(blueprint)
