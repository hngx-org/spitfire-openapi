from flask import Blueprint, request, jsonify, session
from openapi import db, bcrypt
from openapi.models.user import User
from openapi.errors.handlers import CustomError
from openapi.utils import requires_auth

# url_prefix includes /api/auth before all endpoints in blueprint
auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.route("/register", methods=["POST"])
def register():
    """
    This view function facilitates registration of a new user.

    This endpoint allows users to register by providing their name, email, password, and password confirmation.

    Args:
        None (Uses data from the JSON request body).

    Returns:
        JSON response:
        - If successful: A JSON response with status 201 (Created) and user data.
        - If there's a password confirmation mismatch: A JSON response with status 400 (Bad Request) and an error message.
        - If the email already exists: A JSON response with status 400 (Bad Request) and an error message.
        - If an error occurs during registration: A JSON response with status 400 (Bad Request) and an error message.
    """

    data = request.get_json() if request.get_json() != None else request.form
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Check if password and password confirmation match
    if password != confirm_password:
        raise CustomError("Bad Request", 400, "Passwords do not match!")

    try:
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            return (
                jsonify({"error": "Forbbiden", "message": "Email already exists!"}),
                403,
            )

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(name, email, hashed_password)
        new_user.insert()

        session["user"] = {"id": new_user.id}

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "User Created Succesfully",
                    "data": new_user.format(),
                }
            ),
            201,
        )

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        return (
            jsonify(
                {
                    "status": "failed",
                    "message": "Internal Error: User not created",
                }
            ),
            500,
        )


@auth.route("/login", methods=["POST"])
def login_user():
    """
    This function facilitates login of an existing user.

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
        raise CustomError("Bad Request", 400, "Missing required fields")

    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).one_or_none()
    if not user:
        raise CustomError(
            "Resource not Found", 404, "User with this email does not exist"
        )
    if not bcrypt.check_password_hash(user.password, password):
        raise CustomError("Unauthorized", 401, "Incorrect password")
    session["user"] = {"id": user.id}
    return (jsonify({"message": "success", "data": user.format()}), 200)


# pylint: disable=broad-exception-caught
@auth.route("/@me")
# lets get the user id of the currently loggedin user using requires_auth wrapper
@requires_auth(session)
def see_sess(user_id):
    """
    get the details of current logged in user
    """
    try:
        user = User.query.filter_by(id=user_id).one_or_none()
        return (
            jsonify({"message": "success", "data": user.format()}),
            200,
        )
    except Exception:
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "It's not you it's us",
                }
            ),
            500,
        )


@auth.route("/logout")
def logout_user():
    """
    This view function logs out the currently authenticated user.

    This endpoint allows a user to log out, effectively clearing their session and
    ending their authenticated session on the server.

    Returns:
        JSON response:
        - If the user is successfully logged out: A JSON response with status 200 (OK)
          and a success message.

    """
    session.pop("user", None)
    return jsonify({"message": "success"}), 204
