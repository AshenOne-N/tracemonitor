import os
from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory, jsonify, \
    Response
from flask_login import current_user
from tracemonitor import app, db
from initapp import camera
from forms import SignUpForm, LoginForm
from flask_login import login_required, login_user, logout_user
from flask_wtf.csrf import CSRFError
from models import Admin, User, Record
import uuid
import qrcode as qr
import random
import pyzbar.pyzbar as pzb
import cv2


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
        img = qr.make(qrs)
        img.save(os.path.join(store_path, qrs + '.png'))
        return redirect(url_for('result', user_id=usr.id))
    return render_template('signup.html', form=form)


@app.route('/result/<int:user_id>')
def result(user_id):
    user = User.query.get_or_404(user_id)
    filename = user.qr_img + '.png'
    return render_template('result.html', filename=filename)


@app.route('/store/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['STORE_PATH'], filename)


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
    prefix_f = '请出示二维码'
    img = cv2.imread('./imgs/6.jpg', cv2.IMREAD_UNCHANGED)
    if not img is None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = pzb.decode(gray)
        if len(barcodes) > 0:
            barcodedata = barcodes[0].data.decode('utf-8')
            user = User.query.filter_by(qr_img=barcodedata)
            if not user is None:
                record = Record(user=user.id)
                db.session.add(record)
                db.session.commit()
                message = '扫码成功' + user.username + str(user.st_card)
                return jsonify(message=message)
    return jsonify(message=prefix_f)


def gen(camera):
    """Video streaming generator function."""
    prefix = './imgs/'
    while True:
        sss, img = camera.read()
        cv2.imwrite('./imgs/6.jpg', img)
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
