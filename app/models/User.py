# coding:utf8

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    confirmed = db.Column(db.Boolean)
    realname = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    education = db.Column(db.String(255))
    cv = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    fk_role = db.Column(db.Integer)
    checked = db.Column(db.String(255))
    user_image = db.Column(db.String(255))
    fk_company_id = db.Column(db.Integer)
    is_userInfo_completed = db.Column(db.Boolean)


    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_userInfo_completed = 0

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)



#加载用户回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
