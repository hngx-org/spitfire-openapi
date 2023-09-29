from flask import Blueprint, request, jsonify
from openapi import db, bcrypt
from openapi.models.user import User

# url_prefix includes /api/auth before all endpoints in blueprint
auth = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth.route('/register', methods=['POST'])
def register():

    # if request.method == "POST":
    #     try:
    #         data = request.get_json()
    #         name = data.get("name")
    #         email = data.get("email")
    #         password = data.get("password")

    #         # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    #         new_user = User(name,email,password)
    #         db.session.add(new_user)
    #         db.session.commit()

    #         return jsonify(
    #             {
    #                 "status": "success",
    #                 "message": "User Created Succesfully",
    #                 "data": new_user.format(),
    #             }
    #         )
    #     except Exception as error:
    #         print(f"{type(error).__name__}: {error}")
    #         return (
    #             jsonify(
    #                 {
    #                     "status": "failed",
    #                     "message": "Error: User not created",
    #                 }
    #             ),
    #             400,
    #         )

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(name,email,password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {
            "status": "success",
            "message": "User Created Succesfully",
            "data": new_user.format(),
        }
    )

