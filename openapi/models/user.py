from openapi import db
import bcrypt
from uuid import uuid4
from datetime import datetime


def generate_uuid():
    return uuid4().hex



class User(db.Model):
    __tablename__ = "users"


    id = db.Column(db.String(60), nullable=False, primary_key=True, unique=True, default=generate_uuid)
    email = db.Column(db.String(320), nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    def __init__(self, name, email, password):
        self.email = email
        self.name = name
        self.password = password
        self.subscription_cost = 5
        self.credit_limit = 3
        self.subscription_start_date = datetime.now()
        self.credit_spent = 0

    def has_subscription_rights(self):
        """check if user has subscription rights this month"""
        current_month = datetime.now().month
        return self.subscription_start_date.month == current_month

    def can_use_ai_service(self, service_cost):
        """check if user is allowed to use the ai service"""
        return self.credit_spent + service_cost <= self.credit_limit

    def insert(self):
        """add a new object to the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """allow updates mto the db
        """
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        """delete an object from the database"""
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password):
        """
        Check if the provided password matches the stored hash.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


    def __repr__(self):
        return f"Id: {self.id}, name: {self.name}, Email: {self.email}, Subscribed: {self.has_subscription_rights()}"

    def format(self):
        """Return a dictionary representation of the User object"""
        return {
            "id":self.id,
            "name": self.name,
            "email": self.email,
        }
