from libs.db import db


class Article(db.Model):
    '''文章'''
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)

    @property
    def user(self):
        if not hasattr(self, '_user'):
            self._user = User.query.get(self.uid)
        return self._user
