from openai import db

class user(db.Model):
    __tablenme__ = "user"


    id = db.Colum(db.String(60), nullable=False, primary_key=True, unique=True)
    email = db.Colum(db.String(320), nullable=False, unique=True)
    name = db.Colum(db.String(60), nullable=False, unique=True)
    password = db.Colum(db.String(20), nullable=False, primary_key=True, unique=True)

    def __init__(self, id, name, email, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password

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
