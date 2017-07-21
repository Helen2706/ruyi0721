# coding:utf8

import os



class Config:
    SECRET_KEY = os.urandom(128)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/ruyi20170622'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = '18763823073@163.com'  # 邮件的用户名和密码可以在系统的环境变量中进行添加
    MAIL_PASSWORD = '13467065634,lhl'
    MAIL_DEBUG = True
    MAIL_SUBJECT_PREFIX = "如艺影视大数据"
    UPLOAD_FOLDER_EDITOR = os.path.abspath('app/static/avatar')
    UPLOAD_FOLDER_PROJECT=os.path.abspath('app/static/poster')
    UPLOAD_FOLDER_USER = os.path.abspath('app/static/useravatar')
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']



config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
