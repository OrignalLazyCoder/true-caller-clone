db = {
    'database': 'postgres',
    'user_name' : "postgres",
    'password'  : "toor",
    'db_name' : "truecaller",
    'host': "localhost",
    "port": "5432"
}

jwt_key = "secretkeywillbefetchedfromconfig"


#Change your connection string w.r.t to your database
SQLALCHEMY_DATABASE_URI = "{database}://{user_name}:{password}@{host}:{port}/{db_name}".format(database = db['database'],user_name = db['user_name'], password = db['password'], host = db['host'], port = db['port'], db_name = db['db_name'])
SQLALCHEMY_TRACK_MODIFICATIONS = False
