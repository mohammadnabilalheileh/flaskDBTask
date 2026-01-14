from flask import Blueprint, request, jsonify
from app.models import User
from app.controllers.user_controller import (
    create_user,
    update_user,
    delete_user
)
from app.constants.http_status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["POST"])
def create_user_route():
    user, error = create_user(request.get_json())

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify({
        "id": user.id,
        "username": user.username
    }), HTTP_201_CREATED

@users_bp.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "library_id": user.library.id if user.library else None
        }
        for user in users
    ]), HTTP_200_OK

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    user = User.query.get_or_404(user_id)

    user, error = update_user(user, request.get_json())

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify({
        "id": user.id,
        "username": user.username
    }), HTTP_200_OK

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    user = User.query.get_or_404(user_id)

    delete_user(user)
    return "", HTTP_204_NO_CONTENT

@users_bp.route("/users/<int:user_id>/books/count", methods=["GET"])
def get_user_books_count_route(user_id):
    user = User.query.get_or_404(user_id)

    books_count = len(user.library.books) if user.library else 0

    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "books_count": books_count
    }), HTTP_200_OK
