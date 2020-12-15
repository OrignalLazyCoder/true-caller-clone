from flask import jsonify, request, abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import db
import hashlib
from models.Users import Users
from models.GlobalDB import GlobalDB
from shared.Authentication import (generate_token, token_required)
from utility.Security import hash_string
from services.ErrorHandler import bad_request
from services.UserService import add_user, login_user, search_user
from shared.Constants import error_messages


user_api = Blueprint('users', __name__)


#Add new user
@user_api.route('/add', methods=['POST'])
def create_user():
    """
        This function allows user to create their account 
        input =  { "name": user name - string,
                    "phone_number": number - string - unique,
                    "email": email address - string - optional,
                    "password": password - password }
        output = {user : user details} 
     """
    if not request.is_json or 'name' not in request.get_json() or 'phone_number' not in request.get_json() or 'password' not in request.get_json():
        return bad_request('Missing required data.')
    try:
        return add_user(request)
    except:
        return bad_request(error_messages['user_exist'])


@user_api.route('/login', methods=['POST'])
def login():
     """
        This function allows user to login
        input = { 'phone_number' : 'number - string' , 'password' : 'password - string' }
        output = {'token' : 'JWT token'} 
     """
     if not request.is_json or 'phone_number' not in request.get_json() or  'password' not in request.get_json():
        return bad_request('Missing required data.')
     return login_user(request)

#Search a user using phone_number or name
@user_api.route('/search/<param>', methods=['GET'])
@token_required
def search(user, param):
    """
        This function allows user to search a user or row in Global database 
        input =  search string
        output = {'token' : [user or list of similar rows in Global database]}
        errors = param string is too short | no user found 
     """
    if len(param) <= 2:
         return bad_request(error_messages['too_short'])
    return search_user(param.lower(), user)

