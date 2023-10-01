from datetime import datetime
from app.extensions import db
from app.models import BASE


class Book(db.Model, BASE):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    # condition_id = db.Column(db.Integer, db.ForeignKey("condition.id"), nullable=False)
    description = db.Column(db.Text)
    # location = db.Column(db.String(255), nullable=False)
    # is_available = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # condition = db.relationship("Condition", backref="books", lazy=True)
    genres = db.relationship(
        "Genre",
        secondary="book_genres",
        lazy="subquery",
        backref=db.backref("books", lazy=True),
    )


class Genre(db.Model, BASE):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    # books = db.relationship("Book", backref="genre", lazy=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class BookGenres(db.Model):
    __tablename__ = "book_genres"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))


class Author(db.Model, BASE):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    books = db.relationship("Book", backref="author", lazy=True)


class Condition(db.Model, BASE):
    __tablename__ = "condition"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
