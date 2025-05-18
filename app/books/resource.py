from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.books.models import Book, Genre, Author
from app.books.schemas import BookSchema, BookCreateSchema, BookUpdateSchema, AuthorSchema, GenreSchema, BookUploadSchema
from app.auth.models import User
from app.utils import get_or_create
from flask import current_app as app
import os

from werkzeug.utils import secure_filename

blp = Blueprint("Books", "books", description="წიგნების ოპერაციები")


@blp.route("/books")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        """ყველა წიგნის სიის მიღება"""
        # return Book.get(filters=args)
        return Book.query.all()
    
    @jwt_required()
    @blp.arguments(BookUploadSchema, location="files")
    @blp.arguments(BookCreateSchema, location="form")
    @blp.response(201, BookSchema)
    def post(self, files, book_data):
        """ახალი წიგნის შექმნა"""
        user_email = get_jwt_identity()
        
        print("files", files, "\n", "book_data", book_data)

        # # ჟანრების დამუშავება
        genre_ids = book_data.pop("genre_ids", [])
        
        user = User.query.filter_by(email=user_email).first()

        author, _ = get_or_create(db, Author, name=book_data["author"].lower())
        # # author, _ = Author.query.get_or_create(name=author_name.lower())

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
    @blp.response(200, BookSchema)
    def get(self, book_id):
        """კონკრეტული წიგნის მიღება ID-ით"""
        book = Book.query.get_or_404(book_id)
        return book
    
    #TODO: არ ხდება ჯანრების დამატება
    @jwt_required()
    @blp.arguments(BookUpdateSchema)
    @blp.response(200, BookSchema)
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


# class BooksResource(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument("title", type=str, required=True)
#     parser.add_argument("author", type=str, required=True)
#     parser.add_argument("genre", type=str, action="append", required=True)
#     # parser.add_argument("condition", type=str, required=True)
#     parser.add_argument("description", type=str, required=False)
#     # parser.add_argument("location", type=str, required=True)
#     parser.add_argument("file_path", type=str, required=True)

#     @jwt_required(
#         optional=True,
#     )
#     def get(self, genre=None, author=None, id=None):
#         authorization_header = request.headers.get("Authorization")
#         if authorization_header:
#             current_user = get_jwt_identity()
#         else:
#             current_user = None

#         if genre:
#             books = (
#                 Book.query.join(Book.genres).filter(Genre.name == genre.lower()).all()
#             )
#         elif author:
#             author = author.replace("_", " ")
#             books = (
#                 Book.query.join(Book.author).filter(Author.name == author.lower()).all()
#             )
#         elif id:
#             books = [get_or_404(Book, id=id)]
#         else:
#             books = Book.query.all()
#         book_list = []

#         for book in books:
#             book_dict = {
#                 "id": book.id,
#                 "title": book.title,
#                 "author": book.author.name,
#                 "genre": [genre.name for genre in book.genres],
#                 # "condition": book.condition.name,
#                 "description": book.description,
#                 # "location": book.location,
#                 "owner": book.owner.first_name,
#             }
#             if current_user:
#                 download_url = os.path.join(app.config["UPLOAD_DIR"], book.src)
#                 book_dict["download_url"] = download_url
#             book_list.append(book_dict)
#         return jsonify({"books": book_list})

#     @jwt_required()
#     def post(self):
#         current_user = get_jwt_identity()
#         data = BooksResource.parser.parse_args()
#         title = data.get("title")
#         author = data.get("author")
#         genre = data.get("genre")
#         description = data.get("description")
#         file_path = data.get("file_path")
#         ext = get_extension(file_path)

#         book = Book()
#         get_author, create = get_or_create(db, Author, name=author.lower())
#         book.create(
#             title=str(title),
#             author_id=get_author.id,
#             description=description,
#             owner_id=current_user,
#             src=str(title),
#         )

#         for g in genre:
#             get_genre, create = get_or_create(db, Genre, name=g.lower())
#             book.genres.append(get_genre)
#         book.save()
#         book.add_book_url(ext)
#         # write book to file
#         if os.path.exists(file_path):
#             with open(file_path, "rb") as file:
#                 # Process the file as needed, e.g., save it to a server location
#                 file_content = file.read()

#             file_path_to_save = f"{app.config['UPLOAD_DIR']}\
#                 /{current_user}\
#                 _{book.id}\
#                 _{title.replace(' ', '_')}_{author.replace(' ', '_')}{ext}".replace(
#                 " ", ""
#             )
#             with open(file_path_to_save, "wb") as saved_file:
#                 saved_file.write(file_content)

#         return {"message": f"{book.title} has been added"}, 201

#     @jwt_required()
#     def delete(self, id):
#         current_user = get_jwt_identity()
#         book = get_or_404(Book, id=id)
#         if book.owner_id != current_user:
#             return {"message": "You are not authorized to delete this book"}, 401
#         try:
#             os.remove(os.path.join(app.config["UPLOAD_DIR"], book.src))
#             book.delete()
#         except OSError as e:
#             return {"message": e}, 404
#         return {"message": f"{book.title} has been deleted"}, 200

#     @jwt_required()
#     def put(self, id):
#         current_user = get_jwt_identity()
#         book = get_or_404(Book, id=id)
#         if book.owner_id != current_user:
#             return {"message": "You are not authorized to edit this book"}, 401
#         data = request.get_json()
#         if data.get("author"):
#             author = get_or_404(Author, id=book.author_id)
#             author.update(id=author.id, name=data.get("author").lower())
#             data["author_id"] = author.id
#             del data["author"]
#         book.update(id=id, **data)
#         return {"message": f"{book.title} has been updated"}, 200
