from flask import Flask

app = Flask(__name__)

print('who used me:',__name__)

from app import routes
