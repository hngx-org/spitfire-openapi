"""Payment route handlers"""
from flask import Blueprint, jsonify, session, request
from openapi.models.user import User
from openapi.models.payments import Payments
from openapi.errors.handlers import CustomError
from openapi.schemas  import CreatePaymentSchema
from openapi.utils import requires_auth, get_current_analytics

# TODO: Register this route when payment checks are in place  
# DONE

payments = Blueprint("payments", __name__, url_prefix="/api/payments")


@payments.route("/", methods=["POST"])
@requires_auth(session)
def create_payment(user_id):
    """create payment"""
    data = request.get_json()
    # TODO: Collect payment details and confirm from client


    data = CreatePaymentSchema(**data)

    user = User.query.filter_by(id=user_id).one_or_none()
    if not user:
        raise CustomError("Resource not found", 404, "User does not exist")
    # adding a default amount for subscription in dollars
    payment = Payments(user_id=user.id, amount="3.00")
    payment.insert()
    daily_analytics = get_current_analytics()
    daily_analytics.subscribers += 1
    daily_analytics.update()
    user.credits += 10
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
