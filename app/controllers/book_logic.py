def transfer_book_logic(book, from_library_id, to_library_id):
    if not book:
        return "Book not found"

    if from_library_id == to_library_id:
        return "Source and target libraries must be different"

    if book.library_id != from_library_id:
        return "Book does not belong to the source library"

    book.library_id = to_library_id
    return None
