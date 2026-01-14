from app.extensions import db
from app.models import Library, User

def create_library(data):
    if not data:
        return None, "No data provided"

    name = data.get("name")
    user_id = data.get("user_id")

    if not name or not user_id:
        return None, "name and user_id are required"

    user = User.query.get(user_id)
    if not user:
        return None, "User not found"

    if user.library:
        return None, "User already has a library"

    library = Library(
        name=name,
        user_id=user_id
    )

    db.session.add(library)
    db.session.commit()

    return library, None

def get_all_libraries():
    return Library.query.all()

def get_library_by_id(library_id):
    return Library.query.get(library_id)

def update_library(library, data):
    if "name" in data:
        library.name = data["name"]

    db.session.commit()
    return library


def delete_library(library):
    db.session.delete(library)
    db.session.commit()
