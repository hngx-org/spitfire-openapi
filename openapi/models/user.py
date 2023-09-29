from openapi import db
import bcrypt
from uuid import uuid4

def generate_uuid():

    return uuid4().hex
class User(db.Model):
    __tablename__ = "users"


    id = db.Column(db.String(60), nullable=False, primary_key=True, unique=True, default=generate_uuid)
    email = db.Column(db.String(320), nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, id, name, email, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password

    def set_password(self, password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = hashed_password.decode('utf-8')

    def __repr__(self):
        return "Id: {}, name: {}, Email: {}".format(
            self.id, self.name, self.email
        )

    def format(self):
        """Return a dictionary representation of the User object"""
        return {
            "id":self.id,
            "name": self.name,
            "email": self.email,
        }
