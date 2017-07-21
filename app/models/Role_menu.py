# coding:utf8

from app import db


class Role_menu(db.Model):
    __table__name = "role_menu"
    id = db.Column(db.Integer, primary_key=True)
    fk_company_id = db.Column(db.Integer)
    fk_role_id = db.Column(db.Integer)
    fk_menu_id = db.Column(db.Integer)
    authority = db.Column(db.Integer)
    memo = db.Column(db.String(255))
