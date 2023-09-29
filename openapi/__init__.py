from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from flask_bcrypt import Bcrypt
import os

# Create an instance of Swagger

db = SQLAlchemy()

bcrypt = Bcrypt()


def create_app():
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask-

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///spitfire.db')
    
    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Bcrypt
    bcrypt.init_app(app)

    from openapi.auth.routes import auth

    app.register_blueprint(auth)
    
    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app
