from marshmallow import Schema, fields, validate, pre_load, validates, ValidationError

# class GenreSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)

# class AuthorSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)

# class BookSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True)
#     author = fields.Nested(AuthorSchema, dump_only=True)
#     author_id = fields.Int(load_only=True, required=True)
#     genres = fields.List(fields.Nested(GenreSchema), dump_only=True)
#     genre_ids = fields.List(fields.Int(), load_only=True)
#     description = fields.Str()
#     src = fields.Str(dump_only=True)
#     owner_id = fields.Int(dump_only=True)



class PlainGenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainAuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str()
    description = fields.Str()
    owner_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    src = fields.Str()
    
    # author = fields.Nested(PlainAuthorSchema(), dump_only=True)
    genres = fields.List(fields.Nested(PlainGenreSchema()), dump_only=True)

    @pre_load
    def sanitize_data(self, data, **kwargs):
        """დამუშავება მონაცემების მიღებისას"""
        if "author" in data and data["author"]:
            data["author"] = strip_whitespace(data["author"]).lower()
        return data


class BookUpdateSchema(Schema):
    title = fields.Str()
    author = fields.Int()
    description = fields.Str()
    src = fields.Str()
    genre_ids = fields.List(fields.Int(), required=False)


class BookCreateSchema(BookSchema):
    genre_ids = fields.List(fields.Int(), required=False)

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
