from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.auth.models import User
from app.auth.schemas import UserSchema, UserRegisterSchema, UserLoginSchema

blp = Blueprint("Auth", "auth", description="ავტორიზაციის ოპერაციები", url_prefix="/auth")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """მომხმარებლის რეგისტრაცია"""
        # if User.query.filter(User.username == user_data["username"]).first():
        #     abort(409, message="მომხმარებლის სახელი უკვე გამოყენებულია")
            
        if User.query.filter(User.email == user_data["email"]).first():
            abort(409, message="ელ-ფოსტა უკვე გამოყენებულია")
            
        user = User(
            # username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"]
        )
        user.password = user_data["password"]
        db.session.add(user)
        db.session.commit()
        
        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        """მომხმარებლის ავტორიზაცია"""
        user = User.query.filter(User.email == user_data["email"]).first()
        
        if user and user.verify_password(user_data["password"]):
            access_token = create_access_token(identity=user.email)
            return {"access_token": access_token}
            
        abort(401, message="არასწორი მომხმარებლის სახელი ან პაროლი")


@blp.route("/user")
class UserResource(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        """მიმდინარე მომხმარებლის მონაცემების წამოღება"""
        user_email = get_jwt_identity()
        # user = User.query.get_or_404(user_id)
        user = User.query.filter_by(email=user_email).first()
        return user
