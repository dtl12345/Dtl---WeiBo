import datetime

from flask import Blueprint
from flask import request
from flask import session
from flask import render_template
from flask import redirect

from .models import Article
from user.models import User
from orm import db


article_bp = Blueprint('article', __name__, url_prefix='/article',
                       static_folder='./static', template_folder='./templates')


@article_bp.route('/show_articles')
def show_articles():
    '''所有文章列表'''
    all_articles = Article.query.all()
    return render_template('show_articles.html', all_articles=all_articles)


@article_bp.route('/read')
def read():
    '''阅读文章'''
    article_id = int(request.args.get('article_id'))

    # 取出需要的数据
    article = Article.query.get(article_id)  # 取出当前文章
    user = User.query.get(article.uid)       # 取出作者信息

    return render_template('read.html', article=article, user=user)


@article_bp.route('/post', methods=('GET', 'POST'))
def post():
    '''发布文章'''
    # 检查用户是否登录
    if 'uid' not in session:
        return redirect('/user/login')

    if request.method == 'POST':
        uid = session['uid']
        title = request.form.get('title')
        content = request.form.get('content')
        created = datetime.datetime.now()
        article = Article(uid=uid, title=title, content=content, created=created)
        db.session.add(article)
        db.session.commit()
        return redirect(f'/article/read?article_id={article.id}')
    else:
        return render_template('post.html')


@article_bp.route('/edit', methods=('GET', 'POST'))
def edit():
    '''修改文章 (只能修改自己的文章)'''
    # 检查用户是否登录
    if 'uid' not in session:
        return redirect('/user/login')

    if request.method == 'POST':
        article_id = int(request.form.get('article_id'))
        title = request.form.get('title')
        content = request.form.get('content')
        Article.query.filter_by(id=article_id).update({'title': title,'content': content})
        db.session.commit()
        return redirect('/article/read?article_id=%s' % article_id)
    else:
        article_id = int(request.args.get('article_id'))
        article = Article.query.get(article_id)
        return render_template('edit.html', article=article)


@article_bp.route('/delete')
def delete():
    '''删除文章 (只能删除自己的文章)'''
    # 检查用户是否登录
    if 'uid' not in session:
        return redirect('/user/login')

    article_id = int(request.args.get('article_id'))
    article = Article.query.get(article_id)

    if article.uid == session['uid']:
        db.session.delete(article)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('error.html', error='您没有权限删除该文章')
