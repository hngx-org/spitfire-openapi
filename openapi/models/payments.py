from openapi import db
from openapi.models.base_model import BaseModel


class Payments(BaseModel):
    __tablename__ = "payments"

    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric(6, 2), nullable=False)

    def __repr__(self):
        return "id: {}, user_id: {}, amount: {}, created_at: {},\
              updated_at: {}".format(
            self.id,
            self.user_id,
            self.amount,
            self.created_at,
            self.updated_at,
        )

    def format(self):
        """Return a dictionary representation of the Payment object"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
