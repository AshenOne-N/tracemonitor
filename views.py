from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user
from tracemonitor import app
from forms import SignUpForm,LoginForm
from flask_wtf.csrf import CSRFError

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/signup')
def sign_up():
    form = SignUpForm()
    return render_template('signup.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
