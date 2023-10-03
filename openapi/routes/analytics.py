from flask import Blueprint
from openapi.models.analytics import Analytics
from openapi.utils import get_current_analytics
from openapi import db
from datetime import date

analytics = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@analytics.route("/")
def reset_each_day():
    """create a new analytics field each day"""
    current_analytics = get_current_analytics()
    print(current_analytics)
    if not current_analytics:
        new_analytics = Analytics()
        new_analytics.insert()
        return "success"

    return "Today's Analytics already exists"
