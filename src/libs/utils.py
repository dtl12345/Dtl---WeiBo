import os
from hashlib import sha256
from functools import wraps

from flask import session
from flask import redirect


def make_password(password):
    hash_value = sha256(password.encode('utf8')).hexdigest()
    salt = os.urandom(32).hex()
    return salt + hash_value


def check_password(password, safe_password):
    hash_value = sha256(password.encode('utf8')).hexdigest()
    return hash_value == safe_password[64:]


def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if 'uid' in session:
            return view_function(*args, **kwargs)
        else:
            return redirect('/user/login')
    return wrapper


def save_avatar(uid, avatar):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'Avatar-%s' %uid
    filepath = os.path.join(project_dir, 'static', 'upload', filename)
    avatar.save(filepath)
    file_url = os.path.join('/static', 'upload', filename)
    return file_url