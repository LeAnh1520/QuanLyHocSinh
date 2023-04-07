from QLHocSinh.models import User
import hashlib

def check_login(username, password):
    if username and password:
        # password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip().lower()),
                                 User.password.__eq__(password)).first()

def get_user_by_id(id):
    return User.query.get(id)