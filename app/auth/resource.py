from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.auth.models import User
from app.auth.schemas import UserSchema, UserRegisterSchema, UserLoginSchema

blp = Blueprint("Auth", "auth", description="ავტორიზაციის ოპერაციები")


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

# class UserResource(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument(
#         "email", type=str, required=True, help="This field cannot be blank."
#     )
#     parser.add_argument(
#         "password", type=str, required=True, help="This field cannot be blank."
#     )
#     parser.add_argument("first_name", type=str, required=True)
#     parser.add_argument("last_name", type=str, required=True)

#     def post(self):
#         data = UserResource.parser.parse_args()
#         user = User.query.filter_by(email=data.get("email")).first()
#         if user:
#             response = {"msg": "A user with this email already exists."}
#             return make_response(jsonify(response), 409)
#         user = User()
#         user.create(**data)
#         user.save()
#         response = {"msg": f"{user.first_name} has been added"}
#         return make_response(jsonify(response), 201)


# class LoginResource(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument(
#         "email", type=str, required=True, help="This field cannot be blank."
#     )
#     parser.add_argument(
#         "password", type=str, required=True, help="This field cannot be blank."
#     )

#     def post(self):
#         data = LoginResource.parser.parse_args()
#         user = User.query.filter_by(email=data.get("email")).first()
#         if user and user.verify_password(data.get("password")):
#             expires_delta = timedelta(hours=1)
#             access_token = create_access_token(
#                 identity=user.id, expires_delta=expires_delta
#             )

#             return make_response(jsonify(access_token=access_token))
#         else:
#             return make_response(jsonify({"msg": "Bad email or password"}), 401)
