from flask import Blueprint, request, jsonify, session
from openapi import bcrypt
from openapi.models.user import User

logins = Blueprint("logins", __name__, url_prefix="/api/login")


@logins.route('/login', methods=['POST'])
def login():
    """
    The view function facilitates login an existing user.

    This endpoint allows users to login by providing their email and password.

    Args:
        None (Uses data from the JSON request body).

    Returns:
        JSON response:
        - If successful:
            A JSON response with status 200 (OK) and user data.
        - If data field is inconsistent:
            A JSON response with status 400 (Bad Request) and an error message.
        - If the user does not exist base on the email credential:
            A JSON response with status 404 (Not Found) and an error message.
        - If there's a password confirmation mismatch:
            A JSON response with status 400 (Bad Request) and an error message.
    """
    data = request.get_json()
    # validate the data received
    if "email" not in data or "password" not in data:
        return jsonify(
                {
                    "status": "error",
                    "message": "Missing required fields"
                }), 400
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "User with this email does not exist"}), 404
    if bcrypt.check_password_hash(user.password, password):
        session["user"] = {"id": user.id}
        return (
                jsonify(
                    {
                        "message": "success",
                        "data": {
                            "id": user.id,
                            "email": user.email,
                            "name": user.name,
                            },
                        }), 200)
    else:
        return jsonify({"message": "Incorrect password"}), 400
