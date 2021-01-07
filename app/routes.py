from app import app,db   #从app包中导入Flask程序对象的实例app
import os
from flask import Flask, request, make_response, redirect, abort, render_template,flash,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.forms import LoginForm,RegistrationForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Post
from werkzeug.urls import url_parse
#two routes,无论输入以下哪个URL路由，都会进入def index()函数中

@app.route('/')
@app.route('/index')
@login_required
#one view_function
def index():
   # user = {'username':'lewis'}
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
    return render_template('index.html',title='Home',posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username = login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('invalid username or invalid password!')
            return redirect(url_for('login'))
        login_user(user,login_form.remember_me.data)
       # msg = 'Login required for user {},remember_me={}'.format(login_form.username.data,login_form.remember_me.data)
       # flash(msg)
       # print(msg)
        return redirect(url_for('index'))
        next_page = request.args.get('next')
        if not next_page or  url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html',form=login_form,title='login')
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data,email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('OK,you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=register_form)
