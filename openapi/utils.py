"""
summary
"""
from openapi import db
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

def query_one_filtered(table, **kwargs):
    return db.session.execute(
        db.select(table).filter_by(**kwargs)
    ).scalar_one_or_none()

def query_all_filtered(table, **kwargs):
    return (
        db.session.execute(db.select(table).filter_by(**kwargs))
        .scalars()
        .all()
    )

def query_one(table):
    return db.session.execute(db.select(table)).scalar_one_or_none()


def query_all(table):
    return db.session.execute(db.select(table)).scalars().all()


def query_paginated(table, page):
    return db.paginate(
        db.select(table).order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )

def query_paginate_filtered(table, page, **kwargs):
    return db.paginate(
        db.select(table)
        .filter_by(**kwargs)
        .order_by(table.date_created.desc()),
        per_page=15,
        page=page,
        error_out=False,
    )
