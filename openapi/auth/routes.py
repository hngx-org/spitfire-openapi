from flask import Blueprint, request, jsonify,session
from openapi import db, bcrypt
from openapi.models.user import User
from openapi.utils import is_logged_in

# url_prefix includes /api/auth before all endpoints in blueprint
auth = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth.route('/register', methods=['POST'])
def register():

    if request.method == "POST":
        
        try:
            data = request.get_json()
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            confirm_password = data.get("confirm_password")
            if password != confirm_password:
                return jsonify({"Error": "Password and confirm_password do not match"}), 400
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            user = User.query.filter_by(name=name).first()
            if user:
                return jsonify({"message": "Alaye person don choose that name, pick another one comrade"})

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
            )


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
    