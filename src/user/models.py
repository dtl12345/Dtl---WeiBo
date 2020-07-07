import enum

from orm import db


class Gender(enum.Enum):
    '''性别的枚举类'''
    male = 1
    female = 2
    unknow = 3


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password = db.Column(db.String(20))
    gender = db.Column(db.Enum(Gender), default='unknow')
    city = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.Date, default='1990-01-01')
    bio = db.Column(db.Text)
