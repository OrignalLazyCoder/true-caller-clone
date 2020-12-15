from . import db
from .Spam import Spam
from shared.Constants import globaldb_is_user

class GlobalDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    phone_number = db.Column(db.String(15), nullable=False)
    spam_likelihood = db.Column(db.Integer, nullable = False)
    isUser = db.Column(db.Integer, nullable = False)
    sycnedFrom = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, name, email, phone_number, spam_likelihood = 0, isUser = globaldb_is_user['synced'], syncedFrom = None):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.spam_likelihood = spam_likelihood
        self.isUser = isUser
        self.sycnedFrom = syncedFrom

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'spam_likelihood': self.spam_likelihood
        }