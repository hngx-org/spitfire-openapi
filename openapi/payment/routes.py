from flask import Flask, Blueprint, jsonify, session,request
from openapi.models.user import User
from openapi.errors.handlers import CustomError
from openapi.utils import requires_auth

# TODO: Register this route when payment checks are in place

payments = Blueprint("payments", __name__, url_prefix="/api/payments")


@payments.route("/", methods=["POST"])
@requires_auth(session)
def create_payment(user_id):
    data = request.get_json()

    # TODO: Collect payment details and confirm from client

    user = User.query.filter_by(id=user_id).one_or_none()
    if not user:
        raise CustomError("Resource not found", 404, "User does not exist")
    user.credits += 50
    user.update()
    return (
        jsonify(
            {
                "message": "Payment successful",
                "credits": user.credits,
                "user_id": user.id,
            }
        ),
        200,
    )
