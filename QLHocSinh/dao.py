from QLHocSinh.models import Lop, HocSinh, User
from QLHocSinh import db, app
from flask_login import current_user
from sqlalchemy import func
import hashlib

def get_hocsinh(kw=None, lop_id=None):
    query = HocSinh.query

    if kw:
        query = query.filter(HocSinh.name.contains(kw))

    if lop_id:
        query = query.filter(HocSinh.Lop.__eq__(lop_id))

    return query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()

def add_user(name, username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)
    db.session.add(u)
    db.session.commit()



