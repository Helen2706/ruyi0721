# coding:utf8

from app import db


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    owner = db.Column(db.String(255))
    contacts = db.Column(db.String(255))
    contact_phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    tel = db.Column(db.String(255))
    logo = db.Column(db.String(255))

    def __init__(self,company_name,owner,contacts,contact_phone,email,address,tel):
        self.company_name = company_name
        self.owner = owner
        self.contacts = contacts
        self.contact_phone = contact_phone
        self.email = email
        self.address = address
        self.tel = tel

class CompanyUser(db.Model):
    __tablename__ = "company_project_user"
    id = db.Column(db.Integer(),primary_key=True)
    company_ID = db.Column(db.Integer())
    project_ID = db.Column(db.Integer())
    user_ID = db.Column(db.Integer())