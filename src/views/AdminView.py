from flask import jsonify, request, abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from services.ErrorHandler import bad_request
from shared.Authentication import (generate_token, token_required)
from shared.Constants import user_roles, error_messages
from services.DataAnalyzer import update_spam_likelihood

admin_api = Blueprint('admin', __name__)

#Get list of spams

#Register new spam number
@admin_api.route('/sync', methods=['GET'])
@token_required
def sync(user):
    """
        This function is only accessible to admin user to upadate spam likelihood in global database
    """
    if (user.role is not user_roles['admin']):
        return bad_request(error_messages['unauthorized_access'])
    try:
        update_spam_likelihood()
        return jsonify({'task':error_messages['completed']}) , 200
    except:
        return jsonify({'task':error_messages['something_went_wrong']})

