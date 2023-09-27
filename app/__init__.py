from flask import Flask
from flask_restful import Api
from app.extensions import db
from app.auth.models import User
from app.auth.resource import UserResource, LoginResource


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    register_extensions(app)

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "User": User}

    return app


def register_extensions(app):
    # Setup Flask-SQLAlchemy
    db.init_app(app)

    with app.app_context():
        db.create_all()


def register_api(app):
    api = Api(app)
    api.add_resource(UserResource, '/register')
    api.add_resource(LoginResource, '/login')
