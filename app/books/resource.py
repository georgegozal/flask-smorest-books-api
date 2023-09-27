from flask import make_response, jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Book


class AvaliableBooks(Resource):
    def get(self):
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
