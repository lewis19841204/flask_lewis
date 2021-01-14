from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
#print(app.config['SECRET_KEY'])
login.login_view = 'login'

mail = Mail(app)
bootstrap = Bootstrap(app)

print('who used me:',__name__)

from app import routes,models,forms
