import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
class Users(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    phone_number = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    passhash = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    token = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.phone_number)   

class Posts(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    content = db.Column(db.String(255))
    likes = db.Column(db.Integer, default=0)
    posted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.id)   

class Comments(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    post_id = db.Column(db.String(64), db.ForeignKey('posts.id'))
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    content = db.Column(db.String(255))
    likes = db.Column(db.Integer, default=0)
    posted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.id)  

class Likes(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    post_id = db.Column(db.String(64), db.ForeignKey('posts.id'), nullable=True)
    comment_id = db.Column(db.String(64), db.ForeignKey('comments.id'), nullable=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    posted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Like {}>'.format(self.id)