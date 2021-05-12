import os
from flask import render_template, flash, redirect, url_for, request, current_app,send_from_directory,jsonify
from flask_login import current_user
from tracemonitor import app, db
from forms import SignUpForm, LoginForm
from flask_login import login_required, login_user, logout_user
from flask_wtf.csrf import CSRFError
from models import Admin, User, Record
import uuid
import qrcode as qr
import random

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/signup')
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        store_path = current_app.config['STORE_PATH']
        username = form.name.data
        card = form.stcard.data
        phone = form.phone.data
        qrs = uuid.uuid4().hex
        usr = User(username=username,
                   st_card=card,
                   phone=phone,
                   qr_img=qrs
                   )
        db.session.add(usr)
        db.session.commit()
        db.session.rollback()
        img = qr.make(qrs)
        img.save(os.path.join(store_path, qrs + '.png'))
        return redirect(url_for('result', user_id=usr.id))
    return render_template('signup.html', form=form)


@app.route('/result/<int:user_id>')
def result(user_id):
    user = User.query.get_or_404(user_id)
    filename = user.qr_img + '.png'
    return  render_template('result.html', filename=filename)

@app.route('/store/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['STORE_PATH'],filename)

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

@app.route('/update-info')
def update_info():
    prefix_s = '扫描成功！'
    prefix_f = '扫描失败！'
    num = random.randint(1,User.query.count() * 2)
    if num > User.query.count():
        return jsonify(message=prefix_f)
    else:
        user = User.query.get(num)
        username = user.username
        stcard = user.st_card
        message = prefix_s + username + stcard
        return jsonify(message=message)