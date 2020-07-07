from datetime import datetime
from app import db
from flask_login import UserMixin

class User_(UserMixin):
    pass

users = [
    {'username':'admin','password':'123'}
]

def query_user(user_id):
    for user in users:
        if user_id == user['username']:
            return user



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),index=True, unique=True)
    email = db.Column(db.String(120),index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    def __repr__(self):
        return '<Username:{}>'.format(self.username)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40),index=True, unique=True)
    posts = db.relationship('Post',backref='category',lazy='dynamic')

    def __repr__(self):
        return '<Category:{}>'.format(self.name)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140),index=True)
    body = db.Column(db.TEXT)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db .Column(db.Integer,db.ForeignKey('user.id'))
    cover = db.Column(db.String(200),default=None)
    category_id = db .Column(db.Integer,db.ForeignKey('category.id'))
    is_en = db.Column(db.Boolean,default=False)
    
    def __repr__(self):
        return '<Post:{}>'.format(self.title)