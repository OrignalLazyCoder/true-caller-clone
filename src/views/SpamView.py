from flask import jsonify, request, abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from services.ErrorHandler import bad_request
from services.SpamService import add_spam
from shared.Constants import error_messages
from shared.Authentication import (generate_token, token_required)


spam_api = Blueprint('spam', __name__)

#Get list of spams

#Register new spam number
@spam_api.route('/add', methods=['POST'])
@token_required
def create(user):
    """
        This function allows user to login
        input = { "number" : number - string }
        output = {'spam' : spam details} 
    """
    if not request.is_json or 'number' not in request.get_json():
        return bad_request('Missing required data.')
    try:
        return add_spam(user, request)
    except:
        return bad_request(error_messages['cannot_report'])
