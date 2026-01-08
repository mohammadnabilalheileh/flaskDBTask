from datetime import datetime
from .extensions import db

class Library(db.Model):
    __tablename__ = "libraries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    books = db.relationship(
        "Book",
        backref="library",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Library {self.name}>"

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)

    library_id = db.Column(
        db.Integer,
        db.ForeignKey("libraries.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Book {self.title}>"
