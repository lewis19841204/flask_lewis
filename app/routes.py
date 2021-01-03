from app import app   #从app包中导入Flask程序对象的实例app
import os
from flask import Flask, request, make_response, redirect, abort, render_template,flash,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.forms import LoginForm
#two routes,无论输入以下哪个URL路由，都会进入def index()函数中

@app.route('/')
@app.route('/index')

#one view_function
def index():
    user = {'username':'lewis'}
    posts = [
            {
                'author':{'username':'wendy'},
                'body': 'this is a sunshine day!'
            },
            {
                'author':{'username':'susan'},
                'body': 'this is a big suprise!'

            }
            ]
    return render_template('index.html',title='Home',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        msg = 'Login required for user {},remember_me={}'.format(login_form.username.data,login_form.remember_me.data)
        flash(msg)
        print(msg)
        return redirect('/index')
    return render_template('login.html',form=login_form,title='login')
