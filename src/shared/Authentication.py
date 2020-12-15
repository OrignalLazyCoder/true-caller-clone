import jwt
from datetime import datetime, timedelta
from flask import jsonify, request, abort, Blueprint
from models.Users import Users
from functools import wraps
from config import jwt_key

def generate_token(user):
    token =  jwt.encode({
            'sub': user.phone_number,
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)},
            jwt_key)
    return token.decode('UTF-8')
    
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, jwt_key)
            user = Users.query.filter_by(phone_number = data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify