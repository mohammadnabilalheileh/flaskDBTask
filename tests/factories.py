from unittest.mock import MagicMock

def fake_book(id=1, title="Book", author="Author", library_id=1):
    book = MagicMock()
    book.id = id
    book.title = title
    book.author = author
    book.library_id = library_id
    return book

def fake_library(id=1):
    library = MagicMock()
    library.id = id
    library.books = []
    return library

def fake_user(id=1, username="user"):
    user = MagicMock()
    user.id = id
    user.username = username
    user.library = fake_library(id)
    return user
