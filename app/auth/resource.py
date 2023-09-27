from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.auth import User


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument("first_name", type=str, required=True)
    parser.add_argument("last_name", type=str, required=True)

    def post(self):
        data = UserResource.parser.parse_args()
        user = User.query.filter_by(email=data.get("email")).first()
        if user:
            response = {"msg": "A user with this email already exists."}
            return make_response(jsonify(response), 409)
        user = User()
        user.create(**data)
        user.save()
        response = {"msg": f"{user.first_name} has been added"}
        return make_response(jsonify(response), 201)


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = LoginResource.parser.parse_args()
        user = User.query.filter_by(email=data.get("email")).first()
        if user and user.verify_password(data.get("password")):
            expires_delta = timedelta(hours=1)
            access_token = create_access_token(
                identity=user.id, expires_delta=expires_delta
            )

            return make_response(jsonify(access_token=access_token))
        else:
            return make_response(jsonify({"msg": "Bad email or password"}), 401)
