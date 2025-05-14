from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    # username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)


class UserRegisterSchema(UserSchema):
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
