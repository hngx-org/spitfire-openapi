from openapi import db
from openapi.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(320), nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    credits = db.Column(db.Integer(), default=3, nullable=False)

    def __init__(self, name, email, password):
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return "id: {}, name: {}, email: {}, credit: {}, created_at: {},\
              updated_at: {}".format(
            self.id,
            self.name,
            self.email,
            self.credits,
            self.created_at,
            self.updated_at,
        )

    def format(self):
        """Return a dictionary representation of the User object"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "credits": self.credits,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
