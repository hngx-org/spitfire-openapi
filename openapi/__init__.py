from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS
from flask import Flask, session
from flask_bcrypt import Bcrypt
from openapi.config import App_Config
from jobs.schedule_analytics import stop_run_continuously
import time

# Create an instance of Swagger

db = SQLAlchemy()

bcrypt = Bcrypt()

sess = Session()


def create_app():
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask-

    app = Flask(__name__)
    app.config["SESSION_SQLALCHEMY"] = db
    app.config.from_object(App_Config)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        print(f"using db")

    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize sessions
    sess.init_app(app)

    # Initialize Bcrypt
    bcrypt.init_app(app)

    # Importing the models here so it can create the empty tables.
    # The user table was created by default because it was already in use in
    # the routes
    from openapi.models.user import User
    from openapi.models.analytics import Analytics
    from openapi.models.payments import Payments

    from openapi.auth.routes import auth
    from openapi.errors.handlers import error
    from openapi.routes.interractions import conversation
    from openapi.routes.analytics import analytics

    app.register_blueprint(auth)
    app.register_blueprint(error)
    app.register_blueprint(conversation)
    app.register_blueprint(analytics)

    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app
