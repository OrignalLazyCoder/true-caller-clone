from . import db
import hashlib
from shared.Constants import user_roles

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable = False)
    role = db.Column(db.Integer, nullable = False)

    def __init__(self, name, email, phone_number, password = None, role = user_roles['user']):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.role = role

    # Gets dict with the Doctor object and all of its associated reviews
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number
        }