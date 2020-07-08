import datetime

from flask import Blueprint
from flask import request
from flask import session
from flask import render_template
from flask import redirect

from .models import Article
from user.models import User
from libs.db import db
from libs.utils import login_required


article_bp = Blueprint('article', __name__, url_prefix='/article', template_folder='./templates')


@article_bp.route('/post', methods=('GET', 'POST'))
@login_required
def post():
    if request.method == 'POST':
        uid = session['uid']
        content = request.form.get('content')
        now = datetime.datetime.now()

        if not content:
            return render_template('post.html', err='微博不能为空')
        article = Article(uid=uid, content=content, created=now, updated=now)
        db.session.add(article)
        db.session.commit()
        return redirect('/article/read?wid=%s' %article.id)

    else:
        return render_template('post.html')

@article_bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    if request.method == 'POST':
        wid = int(request.form.get('wid'))
        content = request.form.get('content')
        now = datetime.datetime.now()

        if not content:
            return render_template('post.html', err='微博不能为空')
        
        Article.query.filter_by(id=wid).update({
            'content':content,
            'updated':now,
        })
        db.session.commit()
        return redirect('/article/read?wid=%s' %wid)

    else:
        wid = int(request.args.get('wid'))
        article = Article.query.get(wid)
        return render_template('edit.html', article=article)


@article_bp.route('/read')
def read():
    wid = int(request.args.get('wid'))
    article = Article.query.get(wid)
    return render_template('read.html', article=article)