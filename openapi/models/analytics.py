from openapi import db
from openapi.models.base_model import BaseModel


class Analytics(BaseModel):
    __tablename__ = "analytics"

    openai_requests = db.Column(db.Integer(), default=0, nullable=False)
    subscribers = db.Column(db.Integer(), defaault=0, nullable=False)


    def __repr__(self):
        return "id: {}, openai_requests: {}, subscribers: {}, created_at: {},\
              updated_at: {}".format(
            self.id,
            self.openai_requests,
            self.subscribers,
            self.created_at,
            self.updated_at,
        )

    def format(self):
        """Return a dictionary representation of the analytics object"""
        return {
            "id": self.id,
            "openai_requests": self.openai_requests,
            "subscribers": self.subscribers,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
