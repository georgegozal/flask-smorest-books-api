from marshmallow import Schema, fields, validate, pre_load, validates, ValidationError

def strip_whitespace(value):
    """მოაშორებს whitespace-ს სტრინგებს თუ სტრინგია"""
    if isinstance(value, str):
        return value.strip()
    return value


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    # username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)

    @pre_load
    def sanitize_data(self, data, **kwargs):
        print("sanitazing data")
        """დამუშავება მონაცემების მიღებისას"""
        if "first_name" in data and data["first_name"]:
            data["first_name"] = strip_whitespace(data["first_name"])
        if "email" in data and data["email"]:
            data["email"] = strip_whitespace(data["email"])
        return data


class UserRegisterSchema(UserSchema):
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)

    # @validates("password")
    # def validate_password(self, value):
    #     """პაროლის დამატებითი ვალიდაცია"""
    #     if value.isdigit():
    #         raise ValidationError("პაროლი არ უნდა შეიცავდეს მხოლოდ ციფრებს")


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
