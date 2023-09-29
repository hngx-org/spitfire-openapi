"""
summary
"""
from openapi.errors.handlers import CustomError


def is_logged_in(session):
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

    return user.get("id")
