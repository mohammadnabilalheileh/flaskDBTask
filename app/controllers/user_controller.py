from app.extensions import db
from app.models import User, Library


def create_user(data):
    if not data or "username" not in data:
        return None, "Username is required"

    if User.query.filter_by(username=data["username"]).first():
        return None, "Username already exists"

    user = User(username=data["username"])
    db.session.add(user)
    db.session.flush() 

    library = Library(name=f"{user.username}'s Library", user_id=user.id)
    db.session.add(library)

    db.session.commit()
    return user, None


def update_user(user, data):
    if not data or "username" not in data:
        return None, "Username is required"

    user.username = data["username"]
    db.session.commit()
    return user, None


def delete_user(user):
    db.session.delete(user)
    db.session.commit()

def get_user_books_count(user):
    if not user.library:
        return 0

    return len(user.library.books)
