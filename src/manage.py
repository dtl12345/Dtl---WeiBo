#!/usr/bin/env python

from flask import Flask
from flask import redirect

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from orm import db

app = Flask(__name__)
app.secret_key = 'awe345ty7890polkmnbgy89okjbvFT^&*IJBVcder56ytfdWQAsdft'

# DATABASE_URI 格式: mysql://用户名:密码@主机地址:端口/数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:529529Dtl!@139.224.130.8/WeiBo'

# 每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 初始化 db 对象
db.init_app(app)

# 初始化 manager
manager = Manager(app)


# 初始化 migrate 迁移工具
migrate = Migrate(app, db)
# 为 manager 添加迁移命令
manager.add_command('db', MigrateCommand)


# 注册蓝图
from user.views import user_bp
from article.views import article_bp

app.register_blueprint(user_bp)
app.register_blueprint(article_bp)


@app.route('/')
def home():
    return redirect('/article/show_articles')


if __name__ == "__main__":
    manager.run()
