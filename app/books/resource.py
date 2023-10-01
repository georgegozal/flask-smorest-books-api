from flask import jsonify, request, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Book, Genre, Author
from app.utils import get_or_404, get_or_create, get_extension
from app.extensions import db
import os


class BooksResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str, required=True)
    parser.add_argument("author", type=str, required=True)
    parser.add_argument("genre", type=str, action="append", required=True)
    # parser.add_argument("condition", type=str, required=True)
    parser.add_argument("description", type=str, required=False)
    # parser.add_argument("location", type=str, required=True)
    parser.add_argument("file_path", type=str, required=True)

    @jwt_required(optional=True)
    def get(self, genre=None):
        authorization_header = request.headers.get("Authorization")
        if authorization_header:
            current_user = get_jwt_identity()

        if genre:
            books = Book.query.join(Book.genres).filter(Genre.name == genre).all()
        else:
            books = Book.query.all()
        book_list = []

        for book in books:
            book_dict = {
                "title": book.title,
                "author": book.author.name,
                "genre": [genre.name for genre in book.genres],
                # "condition": book.condition.name,
                "description": book.description,
                # "location": book.location,
                "owner": book.owner.first_name,
            }
            # if current_user:
            #     book_dict["download_url"] = book.download_url
            book_list.append(book_dict)
        return jsonify({"books": book_list})

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = BooksResource.parser.parse_args()
        title = data.get("title")
        author = data.get("author")
        genre = data.get("genre")
        description = data.get("description")
        file_path = data.get("file_path")
        ext = get_extension(file_path)
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                # Process the file as needed, e.g., save it to a server location
                file_content = file.read()

            file_path_to_save = f"{current_app.config['UPLOAD_DIR']}/{title.replace(' ', '_')}_{author}{ext}"
            with open(file_path_to_save, "wb") as saved_file:
                saved_file.write(file_content)

        book = Book()
        get_author, create = get_or_create(db, Author, name=author)
        book.create(
            title=str(title),
            author_id=get_author.id,
            description=description,
            owner_id=current_user,
        )
        for g in genre:
            get_genre, create = get_or_create(db, Genre, name=g)
            book.genres.append(get_genre)
        book.save()

        return {"message": f"{book.title} has been added"}, 201
