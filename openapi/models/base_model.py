"""Base template for the application models"""
from openapi import db
from uuid import uuid4
from datetime import datetime


def generate_uuid():
    """Generate a unique id using uuid4()"""
    return uuid4().hex


# Create a base model class that will contain common functionality
class BaseModel(db.Model):
    """BaseClass for all models"""

    __abstract__ = True

    id = db.Column(
        db.String(60),
        primary_key=True,
        unique=True,
        nullable=False,
        default=generate_uuid,
    )
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    def insert(self):
        """Insert the current object into the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update the current object in the database"""
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        """Delete the current object from the database"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Format the object's attributes as a dictionary"""
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses must implement the 'format' method")
