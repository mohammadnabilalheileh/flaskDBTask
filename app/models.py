from datetime import datetime
from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)

    library = db.relationship(
        "Library",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

class Library(db.Model):
    __tablename__ = "libraries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_libraries_user_id"),
        nullable=False,
        unique=True
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", name="uq_libraries_user_id"),
    )

    books = db.relationship(
        "Book",
        backref="library",
        lazy=True,
        cascade="all, delete-orphan"
    )

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
