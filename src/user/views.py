from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import Blueprint
from sqlalchemy.orm import exc

from .models import User
from orm import db

user_bp = Blueprint('user', __name__, url_prefix='/user',
                    template_folder='./templates', static_folder='./static')


@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    '''注册功能'''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        city = request.form.get('city')
        bio = request.form.get('bio')
        birthday = request.form.get('birthday')
        user = User(username=username, password=password, gender=gender,
                    city=city, bio=bio, birthday=birthday)

        db.session.add(user)
        db.session.commit()

        return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    '''登录'''
    if request.method == 'POST':
        # 取出参数
        username = request.form.get('username')
        password = request.form.get('password')

        # 取出用户数据, 并检查 (无法取到时需要提示用户密码错误)
        try:
            user = User.query.filter_by(username=username, password=password).one()
        except exc.NoResultFound:
            return render_template('login.html', err='用户名密码错误')

        # 将登录状态记录到 session
        session['uid'] = user.id
        session['username'] = user.username

        return redirect('/user/info')  # 返回用户信息页
    else:
        return render_template('login.html')


@user_bp.route('/logout')
def logout():
    '''退出'''
    # 删除用户信息
    session.pop('uid')
    session.pop('username')

    return redirect('/user/login')  # 跳回首页


@user_bp.route('/info')
def info():
    '''用户信息'''
    if 'uid' in session:
        uid = session['uid']
        user = User.query.get(uid)
        return render_template('info.html', user=user)
    else:
        return redirect('/user/login')
