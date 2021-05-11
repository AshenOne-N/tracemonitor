import os
import random
from faker import Faker
from flask import current_app
from initapp import db
from models import User, Admin, Record
from sqlalchemy.exc import IntegrityError
import uuid
import qrcode as qr

fake = Faker(locale='zh_CN')


def fake_admin():
    admin = Admin()
    db.session.add(admin)
    db.session.commit()


def fake_user(count=5):
    store_path = current_app.config['STORE_PATH']
    for i in range(count):
        qrs = uuid.uuid4().hex
        card = random.randint(100000000000,999999999999)
        usr = User(username=fake.name(),
                   st_card=str(card),
                   phone=fake.phone_number(),
                   qr_img=qrs
                   )
        db.session.add(usr)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        else:
            img = qr.make(qrs)
            img.save(os.path.join(store_path, qrs + '.png'))


def fake_record(count=50):
    for i in range(count):
        record = Record(timestamp=fake.date_time_this_year(),
                        user=User.query.get(random.randint(1,User.query.count()))
                        )
        db.session.add(record)
    db.session.commit()
