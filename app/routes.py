from app import app,db   #从app包中导入Flask程序对象的实例app
import os
from flask import Flask, request, make_response, redirect, abort, render_template,flash,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.forms import LoginForm,RegistrationForm,EditProfileForm,ResetPasswordRequestForm,ResetPasswordForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Post
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_email,send_password_reset_email
from pygame import mixer
from time import sleep
#two routes,无论输入以下哪个URL路由，都会进入def index()函数中
#file = 'loving_you_truely.mp3'

@app.route('/')
@app.route('/index')
@login_required
#one view_function
def index():
    #mixer.init()
    # mixer.music.load(r'./loving_you_truely.mp3')
    #mixer.music.play()
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
   # sleep(7200)
   # mixer.music.stop()

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


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
                {'author':user,'body':'Test post 111'},
                {'author':user,'body':'Test post 222'}
            ] 
    return render_template('user.html',user=user,posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title='Edit profile',form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user',username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user',username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user',username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user',username=username))

@app.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reset_password_request_form = ResetPasswordRequestForm()
    if reset_password_request_form.validate_on_submit():
        user = User.query.filter_by(email=reset_password_request_form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',tilte='Reset Password',form=reset_password_request_form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
#    pass
    if current_user.is_authenticated:
       return redirect(url_for('index'))
    user = User.verify_reset_password_token(token) #verify_reset_password_token()这个方法是静态方法，直接用类名就可以调用
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html',form=form)
