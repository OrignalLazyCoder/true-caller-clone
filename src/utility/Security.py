import hashlib

def hash_string(string):
    return str(hashlib.sha512(string.encode('utf-8')).hexdigest())