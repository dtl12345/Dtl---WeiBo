from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import Blueprint
from sqlalchemy.orm import exc


from libs.utils import make_password
from libs.utils import check_password
from libs.utils import login_required
from libs.utils import save_avatar
from .models import User
from libs.db import db

user_bp = Blueprint('user', __name__, url_prefix='/user',
                    template_folder='./templates', static_folder='./static')


@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        location = request.form.get('location')
        bio = request.form.get('bio')
        birthday = request.form.get('birthday')

        if username == "" or password == '':
            return render_template('register.html', err='昵称和密码不能为空')
        user = User(username=username, password=password, gender=gender, location=location, bio=bio, birthday=birthday, created=datatime.datatime.now())

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', err='昵称已被使用,请重新输入昵称')
        else:
            return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')


        try:
            user = User.query.filter_by(username=username, password=password).one()
        except NoResultFound:
            return render_template('login.html', err='昵称或密码错误')
    
        session['uid'] = user.id
        session['username'] = user.username

        return redirect('/user/info')  
    else:
        return render_template('login.html')


@user_bp.route('/logout')
def logout():
  
    session.pop('uid')
    session.pop('username')

    return redirect('/user/login') 


@user_bp.route('/info')
def info():
    
    if 'uid' in session:
        uid = session['uid']
        user = User.query.get(uid)
        return render_template('info.html', user=user)
    else:
        return redirect('/user/login')
