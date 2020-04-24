import os
from flask import Flask
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY']='bcf89ccf37493530152e15de30778064'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:''@localhost/attendance_system"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes