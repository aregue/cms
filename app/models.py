from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import sqlalchemy

# Database and login system 
# -------------------------

class User(UserMixin, db.Model):
    __tablename__="users"
    
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def get_id(self):
        return self.username
    
        
class Post(db.Model):
    __tablename__="posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(80))
    content = db.Column(db.Text())
    draft_title =  db.Column(db.String(80))
    draft_content = db.Column(db.Text())
    url = db.Column(db.String(80))
    published = db.Column(db.Boolean())
    pinned = db.Column(db.Boolean())
    date_published = db.Column(db.Date)
    date_updated = db.Column(db.Date)
    files = db.relationship('Upload', backref='post', lazy='dynamic')
    
    
class Upload(db.Model):
    __tablename__="uploads"
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    filename =  db.Column(db.String(80))


class Site(db.Model):
    __tablename__="site"
    
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(80))
    value =  db.Column(db.Text())
    
    
    
