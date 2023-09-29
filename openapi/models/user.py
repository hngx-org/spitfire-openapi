from openapi import db
import bcrypt
from uuid import uuid4
from datetime import datetime


def generate_uuid():
    return uuid4().hex


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.String(60),
        nullable=False,
        primary_key=True,
        unique=True,
        default=generate_uuid,
    )
    email = db.Column(db.String(320), nullable=False, unique=True)
    name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    credit = db.Column(db.Integer(), default="3", nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    def __init__(self, name, email, password):
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return "id: {}, name: {}, email: {}, credit: {}, created_at: {},\
              updated_at: {}".format(self.id, self.name, self.email,
                                     self.credit, self.created_at,
                                     self.updated_at)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Return a dictionary representation of the User object"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "credit": self.credit,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
