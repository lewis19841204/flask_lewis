from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy  #从包中导入类
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)  #定义数据库对象
migrate = Migrate(app,db)  #定义迁移引擎对象

#print(app.config['SECRET_KEY'])



print('who used me:',__name__)

from app import routes,models  
