from orm import db


class Article(db.Model):
    '''文章'''
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    title = db.Column(db.String(32), nullable=False, index=True)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False)
