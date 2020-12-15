email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

messages = {
    'bad_request': '',
    'not_found' : ''
}

user_roles = {
    'admin' : 1,
    'user' : 0
}

globaldb_is_user = {
    'synced' : 0,
    'user' : 1
}

error_messages = {
    'user_not_found' : 'not user found',
    'invalid_credentials' : 'invalid credentials',
    'bad_request' : 'bad request',
    'param_missing': 'required parameters are missing',
    'unauthorized_access' : 'unauthorized access',
    'completed': 'completed',
    'something_went_wrong': 'something went wrong. Please check the logs',
    'too_short': 'search string is too short',
    'cannot_report': 'cannot report more than once',
    'user_exist': 'user already exist'
}