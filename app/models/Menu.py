# coding:utf8

from app import db


class Menu(db.Model):
    __table__name = "menu"
    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(255))
    menu2_name = db.Column(db.String(255))
    menu_url = db.Column(db.String(255))
    rank = db.Column(db.Integer)
    memo = db.Column(db.String(255))
