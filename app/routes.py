from flask import Blueprint, request, jsonify
from .models import Library, Book
from .extensions import db

api = Blueprint("api", __name__)

@api.route("/libraries", methods=["POST"])
def create_library():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Library name is required"}), 400

    library = Library(name=data["name"])
    db.session.add(library)
    db.session.commit()

    return jsonify({
        "id": library.id,
        "name": library.name
    }), 201

@api.route("/libraries", methods=["GET"])
def list_libraries():
    libraries = Library.query.all()

    return jsonify([
        {
            "id": lib.id,
            "name": lib.name,
            "books_count": len(lib.books)
        }
        for lib in libraries
    ])

@api.route("/libraries/<int:library_id>", methods=["PUT"])
def update_library(library_id):
    library = Library.query.get_or_404(library_id)
    data = request.get_json()

    if "name" in data:
        library.name = data["name"]

    db.session.commit()

    return jsonify({
        "id": library.id,
        "name": library.name
    })

@api.route("/libraries/<int:library_id>", methods=["DELETE"])
def delete_library(library_id):
    library = Library.query.get_or_404(library_id)

    db.session.delete(library)
    db.session.commit()

    return jsonify({"message": "Library deleted"})

@api.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    required_fields = ["title", "author", "library_id"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    book = Book(
        title=data["title"],
        author=data["author"],
        library_id=data["library_id"]
    )

    db.session.add(book)
    db.session.commit()

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "library_id": book.library_id,
        "created_at": book.created_at.isoformat()
    }), 201

@api.route("/books", methods=["GET"])
def list_books():
    library_id = request.args.get("library_id", type=int)
    search = request.args.get("search")

    query = Book.query

    if library_id:
        query = query.filter(Book.library_id == library_id)

    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) |
            (Book.author.ilike(f"%{search}%"))
        )

    books = query.all()

    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id,
            "created_at": book.created_at.isoformat()
        }
        for book in books
    ])

@api.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if "title" in data:
        book.title = data["title"]
    if "author" in data:
        book.author = data["author"]
    if "library_id" in data:
        book.library_id = data["library_id"]

    db.session.commit()

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "library_id": book.library_id
    })

@api.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted"})

@api.route("/libraries/<int:library_id>/books", methods=["GET"])
def get_books_by_library(library_id):
    library = Library.query.get_or_404(library_id)

    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "created_at": book.created_at.isoformat()
        }
        for book in library.books
    ])

