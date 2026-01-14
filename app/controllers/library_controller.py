from app.models import Library
from app.extensions import db


def create_library(data):
    if not data or "name" not in data:
        return None, "Library name is required"

    library = Library(name=data["name"])
    db.session.add(library)
    db.session.commit()

    return library, None


def update_library(library, data):
    if "name" in data:
        library.name = data["name"]

    db.session.commit()
    return library


def delete_library(library):
    db.session.delete(library)
    db.session.commit()
