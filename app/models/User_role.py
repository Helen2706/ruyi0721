# coding:utf8

from app import db


class User_role(db.Model):
    __table__name = "user_role"
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer)
    fk_company_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    memo = db.Column(db.String(255))
