# coding:utf8

from app import db


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    fk_company_ID = db.Column(db.Integer, nullable=False)
    fk_user_ID = db.Column(db.Integer, nullable=False)
    company_project_ID = db.Column(db.Integer, nullable=False)
    project_name = db.Column(db.String(255), nullable=False)
    episode_count = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    issued = db.Column(db.Boolean, nullable=False)
    investment = db.Column(db.Float)
    label = db.Column(db.Text)
    memo = db.Column(db.Text)
    project_poster = db.Column(db.String(255))
    abstract = db.Column(db.Text)

    def __repr__(self):
        return '<Project %r>' % self.project_name
