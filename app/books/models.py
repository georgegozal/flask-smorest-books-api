from datetime import datetime
from app.extensions import db
from app.models import BASE


class Book(db.Model, BASE):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    src = db.Column(db.String(255), nullable=False)

    def add_book_url(self, ext):
        self.src = f"{self.owner_id}_{self.id}_{self.title.replace(' ', '_')}_{self.author.name.replace(' ', '_')}{ext}"
        self.save()

    genres = db.relationship(
        "Genre",
        secondary="book_genres",
        lazy="subquery",
        backref=db.backref("books", lazy=True),
    )

    def __repr__(self) -> str:
        return f"{self.title} by {self.author.name}"


class Genre(db.Model, BASE):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
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

    def __repr__(self) -> str:
        return self.name


class Condition(db.Model, BASE):
    __tablename__ = "condition"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
