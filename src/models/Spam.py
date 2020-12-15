from . import db

class Spam(db.Model):
    
    __table_args__ = (
        db.UniqueConstraint('reported_by', 'number', name='unique_data_entry'),
    )

    id = db.Column(db.Integer, primary_key=True)
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    number = db.Column(db.String(15), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, reported_by, number, users_id = None):
        self.reported_by = reported_by
        self.number = number
        self.users_id = users_id


    # Gets dict with the Review object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'reported_by': self.reported_by,
            'number': self.number,
            'users_id': self.users_id
        }