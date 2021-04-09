
import os
import json
with open('/etc/config.json') as config_file:
        config = json.load(config_file)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

app.config['SECRET_KEY'] = config.get('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # login is the function name of our route
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = config.get('EMAIL_PASS')
mail = Mail(app)

from uccworks import routes

from uccworks.handlers import errors
app.register_blueprint(errors)
