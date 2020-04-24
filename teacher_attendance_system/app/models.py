from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime
import requests
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    subjects = db.relationship('Subject', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subjectid = db.Column(db.Integer,nullable=False)
    subjectname=db.Column(db.String(30), nullable=False)
    batchid=db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Subject('{self.subjectid}','{self.subjectname}','{self.user_id}')"

class Student_User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    batchid=db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    subjects = db.relationship('Student_Subject', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"

class Student_Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subjectid = db.Column(db.Integer,nullable=False)
    subjectname=db.Column(db.String(30), nullable=False)
    batchid=db.Column(db.String(20), nullable=False)
    tot_class=db.Column(db.Integer, default=0)
    att_class=db.Column(db.Integer, default=0)
    student_id = db.Column(db.Integer, db.ForeignKey('student__user.id'), nullable=False)

    def __repr__(self):
        return f"Subject('{self.subjectid}','{self.subjectname}','{self.student_id}','{self.tot_class}')"