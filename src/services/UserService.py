from models.Users import Users
from models import db
from models.GlobalDB import GlobalDB
from flask.json import jsonify
from services.ErrorHandler import bad_request, not_found
from utility.Security import hash_string
from shared.Authentication import generate_token
import re
from shared.Constants import email_regex, globaldb_is_user, error_messages
from services.DataAnalyzer import update_spam_likelihood

# Adds user entry to Users table and one entry to global database for global search
def add_user(request):
    if request.get_json()['email'] != "" and not re.search(email_regex,request.get_json()['email']) or not request.get_json()['phone_number'].isdigit():
        return bad_request('wrong arguments')
    user = Users(request.get_json()['name'].lower(), request.get_json()['email'], request.get_json()['phone_number'], hash_string(request.get_json()['password']))
    globalDB = GlobalDB(request.get_json()['name'].lower(), request.get_json()['email'], request.get_json()['phone_number'], 0, isUser = globaldb_is_user['user'])
    db.session.add(user)
    db.session.add(globalDB)
    db.session.commit()
    return jsonify({'user' : user.serialize}), 201

# check user credentials and assign jwt token
def login_user(request):
     try:
        if not request.get_json()['phone_number'].isdigit():
            return bad_request('wrong arguments')
        user = find_user(request.get_json()['phone_number'], login = True)
        if user is not None and (user.password == hash_string(request.get_json()['password'])):
            #create token
            token = generate_token(user)
            return jsonify({'token' : token}), 201
        else:
            return jsonify(not_found(error_messages['invalid_credentials'])), 404
     except Exception:
        return bad_request(error_messages['invalid_credentials'])

# search user based on search parameter - phone_number or name
def search_user(param, user = None):
    try:
        result = find_user(param, request_user = user)
        return jsonify({'users' : [globaldb.serialize for globaldb in result]})
    except:
        return not_found(error_messages['user_not_found']) 


# finds user based on multiple conditions
def find_user(param, request_user = None, spam = False, login = False):

    # when searching for spam entries, user is fetched so that it can be recorded to maintain relationship
    if spam:
        return Users.query.filter_by(phone_number = param).first()
    
    # when seaching for login, user is searched based on phone number only
    if login:
        return Users.query.filter_by(phone_number = param).first()

    result = []
    #arrange users in such a way that 
    #1. If required user is found. Send one user in a list
    #2. First those users should come who has seach string in starting
    #3. Second those should come who have similar string in between but not in starting
    #check if search string is number or not and search for exact match with phone_number or name
    if param.isdigit():
        user = GlobalDB.query.filter_by(phone_number = param).all()
    else:
        user = GlobalDB.query.filter_by(name = param).all()
    
    if len(user) > 1 and param.isdigit():
        for u in user:
            if u.isUser == globaldb_is_user['user']:
                result.extend([u])
                break
    else:
        result.extend(user)
    
    if None in result or result == [] and not spam:
        # if no exact match is found and this search is not for spam, then similar entries are searched
        if param.isdigit():
            user = GlobalDB.query.filter(GlobalDB.phone_number.like(param + "%")).all()
        else:
            user = GlobalDB.query.filter(GlobalDB.name.like(param + "%")).all()

        if user is not None:
            result.extend(user)

        # then search for users that have similar string in between
        if param.isdigit():
            user = GlobalDB.query.filter(GlobalDB.phone_number.like("_%" + param + "%")).all()            
        else:
            user = GlobalDB.query.filter(GlobalDB.name.like("_%" + param + "%")).all()

        if user is not None:
            result.extend(user)

    for res in result:
        #if details in globaldb is not of registered user then email should be hidden
        if not (request_user is not None and request_user.id == res.sycnedFrom) or res.isUser != globaldb_is_user['user']:
            res.email = ""
    return result