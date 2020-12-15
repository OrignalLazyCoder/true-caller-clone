from app import app
from models import db
from data.GlobalDB import globaldb_test_data
from data.User import User_test_data, admin_test_data
from data.Spam import spam_test_data
from flask_sqlalchemy import SQLAlchemy
from models.Users import Users
from utility.Security import hash_string
from models.GlobalDB import GlobalDB
from models.Spam import Spam
from shared.Constants import user_roles, globaldb_is_user

with app.app_context():
    db.drop_all()
    db.create_all()

db = SQLAlchemy(app)

for i in User_test_data:
    user = Users(i['name'].lower(), i['email'], i['phone_number'], hash_string(i['password']))
    db.session.add(user)

admin = Users(admin_test_data['name'].lower(), admin_test_data['email'], admin_test_data['phone_number'], hash_string(admin_test_data['password']), user_roles['admin'])
db.session.add(admin)
db.session.commit()

for i in User_test_data:
    globaldb = GlobalDB(i['name'].lower(), i['email'], i['phone_number'], isUser = globaldb_is_user['user'], syncedFrom=1)
    db.session.add(globaldb)

db.session.commit()

for i in globaldb_test_data:
    globaldb = GlobalDB(i['name'].lower(), i['email'], i['phone_number'])
    db.session.add(globaldb)

db.session.commit()

for i in spam_test_data:
    spam = Spam(i['reported_by'], i['number'])
    db.session.add(spam)

db.session.commit()


