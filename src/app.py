from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from models.Users import Users
from models.Spam import Spam 
from models.GlobalDB import GlobalDB
from views.UsersView import user_api as user_blueprint
from views.SpamView import spam_api as spam_blueprint
from views.AdminView import admin_api as admin_blueprint
from services.DataAnalyzer import update_spam_likelihood
from apscheduler.scheduler import Scheduler
import atexit

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = "advhbfsoivhbwefovihwevoijwenviojwenv"

app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(spam_blueprint, url_prefix='/api/v1/spams') 
app.register_blueprint(admin_blueprint, url_prefix='/api/v1/admin')

cron = Scheduler(daemon=True)

@cron.interval_schedule(hours=24)
def job_function():
    update_spam_likelihood()

db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)