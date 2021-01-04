from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
print(app.config['SECRET_KEY'])



print('who used me:',__name__)

from app import routes
