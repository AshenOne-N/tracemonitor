import os
from datetime import datetime
from flask import current_app
from tracemonitor import app, db
from flask_login import UserMixin


class Administrator(db.Model):
    admin_id = db.column(db.Integer, primary_key=True)
    account = db.column(db.String(30))
    password_hash = db.column(db.String(128))


class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(30))
    card_id = db.column(db.String(20), unique=True, index=True)
    ID_hash = db.column(db.String(128))
    photo_id = db.column(db.String(64))
    records = db.relationship('record',back_populates='user',cascade='all')


class record(db.Model):
    id = db.column(db.Integer, primary_key=True)
    timestamp = db.column(db.DateTime, default=datetime.utcnow(), index=True)
    user_id = db.column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',back_populates='records')
