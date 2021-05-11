from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user
from tracemonitor import app
from forms import SignUpForm, LoginForm
from flask_login import login_required, login_user, logout_user
from flask_wtf.csrf import CSRFError
from models import Admin, User, Record


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/signup')
def sign_up():
    form = SignUpForm()

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.pswd.data
        admin = Admin.query.first()
        if admin:
            if username == admin.account and admin.validate_password(password):
                login_user(admin, True)
                flash('Welcome !!')
                return redirect('auth')
        else:
            flash('No account!', 'error')
    return render_template('login.html', form=form)


@app.route('/auth')
@login_required
def auth():
    records = Record.query.order_by(Record.timestamp.desc()).all()
    return render_template('auth.html', records=records)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    form = LoginForm()
    flash('Logout success!', 'info')
    return redirect(url_for('login'))
