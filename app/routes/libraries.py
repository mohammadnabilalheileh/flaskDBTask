from flask import Blueprint, request, jsonify
from app.models import Library
from app.controllers.library_controller import (
    create_library,
    update_library,
    delete_library,
    get_all_libraries,
    get_library_by_id
)
from app.constants.http_status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK
)

libraries_bp = Blueprint("libraries", __name__)

@libraries_bp.route("/libraries", methods=["POST"])
def create_library_route():
    library, error = create_library(request.get_json())

    if error:
        return jsonify({"error": error}), HTTP_400_BAD_REQUEST

    return jsonify({
        "id": library.id,
        "name": library.name
    }), HTTP_201_CREATED

@libraries_bp.route("/libraries", methods=["GET"])
def list_libraries_route():
    libraries = get_all_libraries()

    return jsonify([
        {
            "id": lib.id,
            "name": lib.name,
            "user_id": lib.user_id
        }
        for lib in libraries
    ]), HTTP_200_OK

@libraries_bp.route("/libraries/<int:library_id>", methods=["GET"])
def get_library_route(library_id):
    library = get_library_by_id(library_id)

    if not library:
        return jsonify({"error": "Library not found"}), 404

    return jsonify({
        "id": library.id,
        "name": library.name,
        "user_id": library.user_id
    }), HTTP_200_OK

@libraries_bp.route("/libraries/<int:library_id>", methods=["PUT"])
def update_library_route(library_id):
    library = Library.query.get_or_404(library_id)

    library = update_library(library, request.get_json())

    return jsonify({
        "id": library.id,
        "name": library.name
    }), HTTP_200_OK

@libraries_bp.route("/libraries/<int:library_id>", methods=["DELETE"])
def delete_library_route(library_id):
    library = Library.query.get_or_404(library_id)

    delete_library(library)

    return "", HTTP_204_NO_CONTENT

