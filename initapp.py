import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import cv2

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'auth'
camera  =  cv2.VideoCapture(0)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'dev key')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    prefix = 'sqlite:////'
    app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(basedir, 'data-dev.db')
    app.config["STORE_PATH"] = os.path.join(basedir, 'store')
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    user = Admin.query.get(int(user_id))
    return user