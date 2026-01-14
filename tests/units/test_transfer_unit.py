from unittest.mock import MagicMock
from app.controllers.book_logic import transfer_book_logic


def test_transfer_book_logic_only():
    book = MagicMock()
    book.library_id = 1

    error = transfer_book_logic(book, 1, 2)

    assert error is None
    assert book.library_id == 2
