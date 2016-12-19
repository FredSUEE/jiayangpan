from src import db
import datetime

from flask_login import UserMixin

from .post import Post


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    login_method = db.Column(db.Enum('signup', 'google', 'facebook'), default='signup')
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.email)
