import os
from datetime import datetime
from flask import current_app
from initapp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        self.set_password()
        self.account = 'admin'

    def set_password(self, password='123456'):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    st_card = db.Column(db.String(20), index=True)
    phone = db.Column(db.String(20))
    qr_img = db.Column(db.String(40))
    records = db.relationship('Record', back_populates='user', cascade='all')




class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='records')
