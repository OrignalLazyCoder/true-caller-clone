from flask import jsonify
from models import db
from models.Spam import Spam
from services.ErrorHandler import bad_request
from services.UserService import find_user

def add_spam(user, request):
    if not request.get_json()['number'].isdigit():
        return bad_request('wrong arguments')
    reportedUser = find_user(request.get_json()['number'], spam=True)
    if reportedUser is not None:
        spam = Spam(user.id, request.get_json()['number'], reportedUser.id)
    else:
        spam = Spam(user.id, request.get_json()['number'], None)
    db.session.add(spam)
    db.session.commit()
    return jsonify({'spam': spam.serialize}), 201