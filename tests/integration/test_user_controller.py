from unittest.mock import MagicMock, patch
from app.controllers.user_controller import (
    create_user,
    update_user,
    delete_user,
    get_user_books_count
)

@patch("app.controllers.user_controller.db")
@patch("app.controllers.user_controller.Library")
@patch("app.controllers.user_controller.User")
def test_create_user_success(MockUser, MockLibrary, mock_db):
    MockUser.query.filter_by.return_value.first.return_value = None

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "john"

    MockUser.return_value = mock_user

    data = {"username": "john"}

    user, error = create_user(data)

    assert error is None
    MockUser.assert_called_once_with(username="john")
    mock_db.session.add.assert_any_call(mock_user)
    mock_db.session.flush.assert_called_once()
    mock_db.session.commit.assert_called_once()

def test_create_user_username_missing():
    user, error = create_user({})

    assert user is None
    assert error == "Username is required"

@patch("app.controllers.user_controller.User")
def test_create_user_username_exists(MockUser):
    MockUser.query.filter_by.return_value.first.return_value = MagicMock()

    user, error = create_user({"username": "john"})

    assert user is None
    assert error == "Username already exists"

@patch("app.controllers.user_controller.db")
def test_update_user_success(mock_db):
    user = MagicMock()
    data = {"username": "new_name"}

    updated_user, error = update_user(user, data)

    assert error is None
    assert user.username == "new_name"
    mock_db.session.commit.assert_called_once()

def test_update_user_username_missing():
    user = MagicMock()

    updated_user, error = update_user(user, {})

    assert updated_user is None
    assert error == "Username is required"

@patch("app.controllers.user_controller.db")
def test_delete_user(mock_db):
    user = MagicMock()

    delete_user(user)

    mock_db.session.delete.assert_called_once_with(user)
    mock_db.session.commit.assert_called_once()

def test_get_user_books_count_no_library():
    user = MagicMock()
    user.library = None

    count = get_user_books_count(user)

    assert count == 0

def test_get_user_books_count_with_books():
    user = MagicMock()
    user.library = MagicMock()
    user.library.books = [MagicMock(), MagicMock(), MagicMock()]

    count = get_user_books_count(user)

    assert count == 3
