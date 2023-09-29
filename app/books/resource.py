from flask import make_response, jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Book, Genre, Author
from app.utils import get_or_404, get_or_create
from app.extensions import db


class BooksResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str, required=True)
    parser.add_argument("author", type=str, required=True)
    parser.add_argument("genre", type=str, action="append", required=True)
    # parser.add_argument("condition", type=str, required=True)
    parser.add_argument("description", type=str, required=False)
    # parser.add_argument("location", type=str, required=True)

    def get(self, genre=None):
        if genre:
            books = Book.query.filter_by(genre=genre, is_available=True).all()
        else:
            books = Book.query.filter_by(is_available=True).all()
        book_list = []
        for book in books:
            book_list.append(
                {
                    "title": book.title,
                    "author": book.author.name,
                    "genre": book.genre.name,
                    "condition": book.condition.name,
                    "description": book.description,
                    "location": book.location,
                    "owner": book.owner.username,
                }
            )
        return jsonify({"books": book_list})

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = BooksResource.parser.parse_args()
        title = data.get("title")
        author = data.get("author")
        genre = data.get("genre")
        description = data.get("description")

        book = Book()
        print("cu", current_user)
        print(data)
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
