"""
Helper functions and decorators
"""
from functools import wraps
from openapi import db
from datetime import date, datetime, timedelta
from openapi.models.user import User
from openapi.models.payments import Payments
from openapi.models.analytics import Analytics
from openapi.errors.handlers import CustomError


def requires_auth(session=None):
    """Auth handler"""
    def is_logged_in_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            Ensures a user is logged in or returns error

            Parameterss:
                session(dict):
                    - flask session object

            returns
                id(str):
                    - logged in users id
            """
            user = session.get("user")

            if not user:
                raise CustomError("Unauthorized", 401, "You are not logged in")
            user_id = user.get("id")
            return f(user_id, *args, **kwargs)

        return wrapper

    return is_logged_in_wrapper


def query_one_filtered(table, **kwargs):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(db.select(table).filter_by(**kwargs)).scalar_one_or_none()


# get all items from table based on filter
# args:table=model_class **kwargs=filters
def query_all_filtered(table, **kwargs):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(db.select(table).filter_by(**kwargs)).scalars().all()


# get first one item from table no filter
def query_one(table):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(db.select(table)).scalar_one_or_none()


# get all items on table no filter
def query_all(table):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(db.select(table)).scalars().all()


def chaaracter_validation(user_input):
    word = user_input.split()
    if len(word) <= 20:
        return user_input
    # reduced_word = " ".join(word[:20])
    raise CustomError("payload too long", 413, "the request body is too long")


def get_current_analytics():
    """Get the current day's analytic entry from the database"""
    return db.session.execute(
        db.select(Analytics).filter(
            db.Cast(Analytics.created_at, db.Date())
            == date.today().strftime("%Y-%m-%d")
        )
    ).scalar_one_or_none()

def handle_check_subscription(user):
    """Confirm subcription status of user"""
    payment = db.session.execute(
        db.Select(Payments).filter_by(user_id=user.id)
                            .order_by(db.desc(Payments.created_at))
                            .scalar_one_or_none()
    )
    print(payment)
    if payment is None:
        # This means user is still on free trial and hasn't
        # made any payment at all
        return True
    if payment.created_at >= (datetime.now() - timedelta(days=30)):
        # this means user has paid in the last 30 days
        return True
    raise CustomError(
        "Subscription Required", 402, "You do not have an active subscription"
    )



def handle_check_credits(session=None):
    """Check user credit"""
    def chat_completion_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = session.get("user")
            if not user:
                raise CustomError("Unauthorized", 401, "You are not logged in")
            if handle_check_subscription() is True:
                user_id = user.get("id")
                user = User.query.get(user_id)
                if user.credits <= 0:
                    raise CustomError(
                        "Payment Required", 402, "You have exhausted your credits"
                    )

            return f(user, *args, **kwargs)

        return wrapper

    return chat_completion_wrapper
