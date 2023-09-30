"""
summary
"""
from openapi.errors.handlers import CustomError
from functools import wraps


def requires_auth(session=None):
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


def chaaracter_validation(user_input):
    word = user_input.split()
    if len(word) <= 20:
        return user_input
    # reduced_word = " ".join(word[:20])
    raise CustomError("payload too long", 413, "the request body is too long") 