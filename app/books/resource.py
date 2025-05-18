from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.books.models import Book, Genre, Author
from app.books.schemas import  GetBookSchema, CreateBookSchema, BookUpdateSchema, AuthorSchema, GenreSchema, BookUploadSchema
from app.auth.models import User
from app.utils import get_or_create
from flask import current_app as app, request, redirect, url_for, send_from_directory
import os

from werkzeug.utils import secure_filename

blp = Blueprint("Books", "books", description="წიგნების ოპერაციები")


@blp.route("/books")
class BookList(MethodView):
    @blp.response(200, GetBookSchema(many=True))
    def get(self):
        """ყველა წიგნის სიის მიღება"""
        # return Book.get(filters=args)
        return Book.query.all()
    
    @jwt_required()
    @blp.arguments(BookUploadSchema, location="files")
    @blp.arguments(CreateBookSchema, location="form")
    @blp.response(201, GetBookSchema)
    def post(self, files, book_data):
        """ახალი წიგნის შექმნა"""
        user_email = get_jwt_identity()
        
        # TODO: ამას ჭირდება გასწორება
        # ჟანრების დამუშავება
        genre_ids = book_data.pop("genre_ids", [])
        
        user = User.query.filter_by(email=user_email).first()

        author, _ = get_or_create(db, Author, name=book_data["author"].lower())

        # Uploaded File
        uploaded_file = files["book"]
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config.get("UPLOAD_DIR"), filename)
        uploaded_file.save(file_path)

        book = Book(
            author_id=author.id,
            title=book_data["title"],
            description=book_data["description"],
            owner_id=user.id,
            src=filename
        )

        # ჟანრების დამატება
        if genre_ids:
            genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
            book.genres = genres
        
        try:
            db.session.add(book)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
            
        return book



@blp.route("/books/<int:book_id>")
class BookResource(MethodView):
    @blp.response(200, GetBookSchema)
    @blp.alt_response(200, content_type="application/octet-stream", description="წიგნის ფაილი")
    def get(self, book_id):
        """კონკრეტული წიგნის მიღება ID-ით, 
        download=true პარამეტრის შემთხვევაში ფაილის ჩამოტვირთვა"""
        
        book = Book.query.get_or_404(book_id)

        download = request.args.get("download", "false").lower() in ("true", "1", "yes")
        if download:
            if not book.src:
                abort(404, message="წიგნის ფაილი არ არსებობს")
            try:
                return send_from_directory(
                    app.config.get("UPLOAD_DIR"), book.src, as_attachment=True
                )
            except FileNotFoundError:
                abort(404, message="წიგნის ფაილი ვერ მოიძებნა დისკზე")

        return book

    #TODO: არ ხდება ჟანრების დამატება
    @jwt_required()
    @blp.arguments(BookUpdateSchema)
    @blp.response(200, GetBookSchema)
    def put(self, book_data, book_id):
        """წიგნის განახლება"""
        book = Book.query.get_or_404(book_id)
        user_email = get_jwt_identity()

        user = User.query.filter_by(email=user_email).first()

        
        if book.owner_id != user.id:
            abort(403, message="თქვენ არ გაქვთ ამ წიგნის განახლების უფლება")
        
        # ჟანრების დამუშავება
        genre_ids = book_data.pop("genre_ids", None)
        
        # წიგნის მონაცემების განახლება
        for key, value in book_data.items():
            setattr(book, key, value)
        
        # ჟანრების განახლება
        if genre_ids is not None:
            genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
            book.genres = genres
        
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
            
        return book
    
    @jwt_required()
    def delete(self, book_id):
        """წიგნის წაშლა"""
        book = Book.query.get_or_404(book_id)
        user_email = get_jwt_identity()

        user = User.query.filter_by(email=user_email).first()
        
        if book.owner_id != user.id:
            abort(403, message="თქვენ არ გაქვთ ამ წიგნის წაშლის უფლება")
            
        try:
            db.session.delete(book)
            db.session.commit()
            return {"message": "წიგნი წარმატებით წაიშალა"}
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))


@blp.route("/authors")
class AuthorList(MethodView):
    @blp.response(200, AuthorSchema(many=True))
    def get(self):
        """ყველა ავტორის სიის მიღება"""
        return Author.query.all()

    @jwt_required()
    @blp.arguments(AuthorSchema)
    @blp.response(201, AuthorSchema)
    def post(self, author_data):
        """ახალი ავტორის შექმნა"""
        author = Author(**author_data)
        
        try:
            db.session.add(author)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
            
        return author


@blp.route("/genres")
class GenreList(MethodView):
    @blp.response(200, GenreSchema(many=True))
    def get(self):
        """ყველა ჟანრის სიის მიღება"""
        return Genre.query.all()

    @jwt_required()
    @blp.arguments(GenreSchema)
    @blp.response(201, GenreSchema)
    def post(self, genre_data):
        """ახალი ჟანრის შექმნა"""
        if Genre.query.filter(Genre.name == genre_data["name"]).first():
            abort(409, message="ჟანრი უკვე არსებობს")
            
        genre = Genre(**genre_data)
        
        try:
            db.session.add(genre)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
            
        return genre
