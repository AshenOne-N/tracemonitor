import os
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
app = Flask(__name__)


app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'dev key')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
prefix = 'sqlite:////'
app.config["SQLALCHEMY_DATABASE_URI"]= prefix + os.path.join(basedir, 'data-dev.db')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)
import views