from flask import jsonify, request, Blueprint, make_response
from injector import inject
from src.api.schemas.users_schema import user_schema
from src.api.interfaces.services.user_service import UserService
from src.api.schemas.requests.request_schema import (
    create_user_schema,
    update_user_schema,
    login_user_schema
)
from flask_expects_json import expects_json
from jsonschema import ValidationError
from src.api.interfaces.exceptions.generic_api_exception import GenericApiException

users_bp = Blueprint("users", __name__, url_prefix="/users")


@inject
@users_bp.route("", methods=["POST"])
@expects_json(create_user_schema)
def create_user(user_service: UserService):
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    new_user = user_service.create_user(username, email, password)

    return jsonify(user_schema.dump(new_user)), 201

@inject
@users_bp.route("/login", methods=["POST"])
@expects_json(login_user_schema)
def login_user(user_service: UserService):
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = user_service.get_user_by_email(email)

    if not user or user.password != password :
     return make_response(
            jsonify(
                {
                    "message": "Invalid user or password",
                    "error": "Invalid input",
                },
            ),
            400,
        )
    
    return jsonify(user_schema.dump(user)), 200


@inject
@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id, user_service: UserService):
    user = user_service.get_user_by_id(user_id)

    return jsonify(user_schema.dump(user)), 200


@inject
@users_bp.route("/<user_id>", methods=["PUT"])
@expects_json(update_user_schema)
def update_user(user_id, user_service: UserService):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user_service.update_user(user_id, username, password)

    return "", 204


@users_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


@users_bp.errorhandler(404)
def not_found(error):
    return jsonify({"message": f"url {request.url} not found"}), 404


@users_bp.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(
            jsonify(
                {
                    "message": original_error.message,
                    "error": "Invalid input",
                },
            ),
            400,
        )

    return error


@users_bp.errorhandler(GenericApiException)
def generic_api_exception(e):
    return jsonify(e.to_dict()), e.status_code
