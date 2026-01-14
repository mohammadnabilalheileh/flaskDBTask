from app.extensions import db
from app.models import Book, Library
from .book_logic import transfer_book_logic

def create_book(data):
    if not data:
        return None, "No data provided"

    required_fields = ["title", "author", "library_id"]
    for field in required_fields:
        if field not in data:
            return None, f"'{field}' is required"

    library = Library.query.get(data["library_id"])
    if not library:
        return None, "Library does not exist"

    book = Book(
        title=data["title"],
        author=data["author"],
        library_id=data["library_id"]
    )

    db.session.add(book)
    db.session.commit()

    return book, None


def update_book(book_id, data):
    if not data:
        return None, "No data provided"

    book = Book.query.get(book_id)
    if not book:
        return None, "Book not found"

    if "title" in data:
        book.title = data["title"]
    if "author" in data:
        book.author = data["author"]
    if "library_id" in data:
        book.library_id = data["library_id"]

    db.session.commit()
    return book, None


def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return False, "Book not found"

    db.session.delete(book)
    db.session.commit()
    return True, None

def transfer_book(book_id, data):
    if not data:
        return None, "Request body is required"

    from_library_id = data.get("from_library_id")
    to_library_id = data.get("to_library_id")

    book = Book.query.get(book_id)
    target_library = Library.query.get(to_library_id)

    if not target_library:
        return None, "Target library not found"

    error = transfer_book_logic(book, from_library_id, to_library_id)
    if error:
        return None, error

    db.session.commit()
    return book, None
