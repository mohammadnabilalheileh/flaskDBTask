import pytest
from unittest.mock import MagicMock, patch
from app.controllers.library_controller import create_library

@patch("app.controllers.library_controller.db")
@patch("app.controllers.library_controller.User")
@patch("app.controllers.library_controller.Library")
def test_create_library_success(MockLibrary, MockUser, mock_db):
    mock_user = MagicMock()
    mock_user.library = None
    MockUser.query.get.return_value = mock_user

    data = {
        "name": "Central Library",
        "user_id": 1
    }

    library, error = create_library(data)

    assert error is None
    MockLibrary.assert_called_once_with(name="Central Library", user_id=1)
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()

@patch("app.controllers.library_controller.User")
def test_create_library_user_not_found(MockUser):
    MockUser.query.get.return_value = None

    data = {
        "name": "Central Library",
        "user_id": 99
    }

    library, error = create_library(data)

    assert library is None
    assert error == "User not found"

@patch("app.controllers.library_controller.User")
def test_create_library_user_has_library(MockUser):
    mock_user = MagicMock()
    mock_user.library = MagicMock()
    MockUser.query.get.return_value = mock_user

    data = {
        "name": "Central Library",
        "user_id": 1
    }

    library, error = create_library(data)

    assert library is None
    assert error == "User already has a library"

@patch("app.controllers.library_controller.Library")
def test_get_all_libraries(MockLibrary):
    mock_libraries = [MagicMock(), MagicMock()]
    MockLibrary.query.all.return_value = mock_libraries

    from app.controllers.library_controller import get_all_libraries
    result = get_all_libraries()

    assert result == mock_libraries

@patch("app.controllers.library_controller.db")
def test_update_library(mock_db):
    from app.controllers.library_controller import update_library

    library = MagicMock()
    data = {"name": "Updated Library"}

    result = update_library(library, data)

    assert library.name == "Updated Library"
    mock_db.session.commit.assert_called_once()
    assert result == library

@patch("app.controllers.library_controller.db")
def test_delete_library(mock_db):
    from app.controllers.library_controller import delete_library

    library = MagicMock()

    delete_library(library)

    mock_db.session.delete.assert_called_once_with(library)
    mock_db.session.commit.assert_called_once()

