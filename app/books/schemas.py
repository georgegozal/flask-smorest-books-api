from marshmallow import Schema, fields, validate, pre_load, validates, ValidationError, post_dump
from flask_smorest.fields import Upload
from flask import current_app as app, url_for
import os
import enum


def strip_whitespace(field):
    return field.strip().lower()


class UploaderSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()


class PlainGenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainAuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class BookUploadSchema(Schema):
    book = Upload(required=True)


class CreateBookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str()
    description = fields.Str()
    
    genres = fields.List(fields.Nested(PlainGenreSchema()), dump_only=True)


    @pre_load
    def sanitize_data(self, data, **kwargs):
        """დამუშავება მონაცემების მიღებისას"""
        data = dict(data)
        if "author" in data and data["author"]:
            data["author"] = strip_whitespace(data["author"])
        return data


class GetBookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    owner = fields.Nested(UploaderSchema())
    created_at = fields.DateTime(dump_only=True)
    src = fields.Str(dump_only=True)
    
    author = fields.Nested(PlainAuthorSchema())
    genres = fields.List(fields.Nested(PlainGenreSchema()), dump_only=True)

    @post_dump
    def transform_src_to_url(self, data, **kwargs):
        """src ველის URL-ად გარდაქმნა"""
        if "src" in data and data["src"]:
            book_id = data["id"]
            if os.path.exists(os.path.join(app.config.get("UPLOAD_DIR"), data["src"])):
                data["download_url"] = url_for("Books.BookResource", book_id=book_id, download=True, _external=True)            
            del data["src"]
        return data



class BookUpdateSchema(Schema):
    title = fields.Str()
    author = fields.Int()
    description = fields.Str()
    src = fields.Str()
    genre_ids = fields.List(fields.Int(), required=False)


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    # books = fields.List(fields.Nested(BookSchema()), dump_only=True)


class ListOrderBy(enum.Enum):
    title = "title"
    created_at = "created_at"


class ListOrder(enum.Enum):
    asc = "asc"
    desc = "desc"


class ListBookParameters(Schema):
    order_by = fields.Enum(ListOrderBy, load_default=ListOrderBy.created_at)
    order = fields.Enum(ListOrder, load_default=ListOrder.desc)
