from unittest.mock import MagicMock, patch
from app.controllers.book_controller import (
    create_book,
    update_book,
    delete_book,
    transfer_book
)

@patch("app.controllers.book_controller.db")
@patch("app.controllers.book_controller.Library")
@patch("app.controllers.book_controller.Book")
def test_create_book_success(MockBook, MockLibrary, mock_db):
    MockLibrary.query.get.return_value = MagicMock()

    data = {
        "title": "1984",
        "author": "Orwell",
        "library_id": 1
    }

    book, error = create_book(data)

    assert error is None
    MockBook.assert_called_once_with(
        title="1984",
        author="Orwell",
        library_id=1
    )
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()

@patch("app.controllers.book_controller.Library")
def test_create_book_library_not_found(MockLibrary):
    MockLibrary.query.get.return_value = None

    data = {
        "title": "1984",
        "author": "Orwell",
        "library_id": 99
    }

    book, error = create_book(data)

    assert book is None
    assert error == "Library does not exist"

@patch("app.controllers.book_controller.db")
@patch("app.controllers.book_controller.Book")
def test_update_book_success(MockBook, mock_db):
    book = MagicMock()
    MockBook.query.get.return_value = book

    data = {"title": "New Title"}

    updated_book, error = update_book(1, data)

    assert error is None
    assert book.title == "New Title"
    mock_db.session.commit.assert_called_once()

@patch("app.controllers.book_controller.Book")
def test_update_book_not_found(MockBook):
    MockBook.query.get.return_value = None

    book, error = update_book(1, {"title": "X"})

    assert book is None
    assert error == "Book not found"

@patch("app.controllers.book_controller.db")
@patch("app.controllers.book_controller.Book")
def test_delete_book_success(MockBook, mock_db):
    book = MagicMock()
    MockBook.query.get.return_value = book

    result, error = delete_book(1)

    assert result is True
    assert error is None
    mock_db.session.delete.assert_called_once_with(book)
    mock_db.session.commit.assert_called_once()

@patch("app.controllers.book_controller.Book")
def test_delete_book_not_found(MockBook):
    MockBook.query.get.return_value = None

    result, error = delete_book(1)

    assert result is False
    assert error == "Book not found"

@patch("app.controllers.book_controller.db")
@patch("app.controllers.book_controller.Library")
@patch("app.controllers.book_controller.Book")
@patch("app.controllers.book_controller.transfer_book_logic")
def test_transfer_book_success(
    mock_logic,
    MockBook,
    MockLibrary,
    mock_db
):
    book = MagicMock()
    book.library_id = 1

    MockBook.query.get.return_value = book
    MockLibrary.query.get.return_value = MagicMock()
    mock_logic.return_value = None

    data = {
        "from_library_id": 1,
        "to_library_id": 2
    }

    transferred_book, error = transfer_book(1, data)

    assert error is None
    mock_logic.assert_called_once()
    mock_db.session.commit.assert_called_once()
