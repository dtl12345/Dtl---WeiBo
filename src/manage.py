#!/usr/bin/env python

from flask import Flask
from flask import redirect

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from libs.db import db

app = Flask(__name__)
app.secret_key = 'KHIGUFUYHljlahkfuhkaN64654678$%#%$#%#$?><HIUghslkk'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:529529Dtl!@139.224.130.8/WeiBo'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)


manager = Manager(app)



migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


from user.views import user_bp
from article.views import article_bp

app.register_blueprint(user_bp)
app.register_blueprint(article_bp)


@app.route('/')
def home():
    return redirect('/article/show_articles')


if __name__ == "__main__":
    manager.run()

