from flask import Blueprint, request, jsonify,session
from openapi import db, bcrypt
from openapi.models.user import User
from openapi.utils import is_logged_in

# url_prefix includes /api/auth before all endpoints in blueprint
auth = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth.route('/register', methods=['POST'])
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
    if request.method == "POST":
        
        try:
            data = request.get_json()
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            password_confirm = data.get("password_confirm")  # New field for password confirmation

            # Check if password and password confirmation match
            if password != password_confirm:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Password confirmation does not match!"
                    }
                ), 400
              
            confirm_password = data.get("confirm_password")
            if password != confirm_password:
                return jsonify({"Error": "Password and confirm_password do not match"}), 400
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            email_exists = User.query.filter_by(email=email).first()
            if email_exists:
                return jsonify(
                    {
                        "status": "error", 
                        "message": "Email already exists!"
                    }
                ), 400

            new_user = User(name,email,hashed_password)
            db.session.add(new_user)
            db.session.commit()

            session["user"]={"id":new_user.id}

            return jsonify(
                {
                    "status": "success",
                    "message": "User Created Succesfully",
                    "data": new_user.format(),
                }
            ),201

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
            

# pylint: disable=broad-exception-caught
@auth.route("/@me")
def see_sess():
    """
    get the details of current logged in user
    """
    # lets get the user id of the currently loggedin user using is_logged_in helper
    user_id = is_logged_in(session) 
    print(user_id)
    pass
    
