from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from hashlib import sha256
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone=db.Column(db.String(11),nullable=False)
    user=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(64),nullable=False)
    def __init__(self,*args,**kwargs):
        telephone=kwargs.get('telephone')
        user=kwargs.get('user')
        password=kwargs.get('password')
        self.telephone=telephone
        self.user=user
        # self.password=generate_password_hash(password)
        gender = sha256()
        gender.update(password.encode('utf8'))
        self.password = gender.hexdigest()
    def check_password(self,password):
        # return check_password_hash(self.password,password)
        gender = sha256()
        gender.update(password.encode('utf8'))
        password = gender.hexdigest()
        return password==self.password
class Question(db.Model):
    __tablename__='question'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    publish_time=db.Column(db.DateTime,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship('User',backref=db.backref('questions'))
class Answer(db.Model):
    __tablename__='answer'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    answer_content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    author=db.relationship('User',backref=db.backref('answers',order_by=create_time.desc()))
    question=db.relationship('Question',backref=db.backref('answers',order_by=create_time.desc()))
