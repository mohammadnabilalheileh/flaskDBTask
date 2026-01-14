from flask import Blueprint, request, jsonify
from app.models import Book
from app.controllers.book_controller import (
    create_book,
    update_book,
    delete_book,
    transfer_book
)
from app.constants.http_status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK
)

books_bp = Blueprint("books", __name__)

@books_bp.route("/books", methods=["POST"])
def create_book_route():
    book, error = create_book(request.get_json())

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "library_id": book.library_id,
        "created_at": book.created_at.isoformat()
    }), HTTP_201_CREATED

@books_bp.route("/books", methods=["GET"])
def list_books_route():
    books = Book.query.all()

    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id,
            "created_at": book.created_at.isoformat()
        }
        for book in books
    ]), HTTP_200_OK

@books_bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book_route(book_id):
    book, error = update_book(book_id, request.get_json())

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author
    }), HTTP_200_OK

@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_route(book_id):
    success, error = delete_book(book_id)

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    
    return "", HTTP_204_NO_CONTENT

@books_bp.route("/books/<int:book_id>/transfer", methods=["POST"])
def transfer_book_route(book_id):
    book, error = transfer_book(book_id, request.get_json())

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify({
        "message": "Book transferred successfully",
        "book_id": book.id,
        "new_library_id": book.library_id
    }), HTTP_200_OK
