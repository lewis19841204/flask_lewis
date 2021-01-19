from flask import Flask,request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel,lazy_gettext as _l
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL, DOCUMENTS, AUDIO, TEXT
import os,re

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
#print(app.config['SECRET_KEY'])
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')

mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

#app.config['UPLOADED_PHOTO_DEST'] = os.path.dirname(os.path.abspath(__file__)) + '/static/music' 
#app.config['UPLOADED_PHOTO_ALLOW'] = AUDIO
#audios = UploadSet('AUDIO')
#configure_uploads(app, audios)
app.config['UPLOADED_AUDIO_DEST'] = '/root/blog/app/static/music'
app.config['UPLOADED_AUDIO_ALLOW'] = AUDIO
def dest(name):
    return '{}/{}'.format(UPLOAD_AUDIO_DEST, name)
#app.config['UPLOAD_PHOTO_URL'] = 'http://localhost:5000/'
#audios = UploadSet('AUDIO')
#configure_uploads(app, audios)


print('who used me:',__name__)

from app import routes,models,forms

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

