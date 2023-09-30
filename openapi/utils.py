"""
summary
"""
from openapi.errors.handlers import CustomError
from functools import wraps
from openapi import db


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

def query_one_filtered(table, **kwargs):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return db.session.execute(
        db.select(table).filter_by(**kwargs)
    ).scalar_one_or_none()


# get all items from table based on filter
# args:table=model_class **kwargs=filters
def query_all_filtered(table, **kwargs):
    """_summary_

    Args:
        table (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (
        db.session.execute(db.select(table).filter_by(**kwargs))
        .scalars()
        .all()
    )


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