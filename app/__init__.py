# coding:utf8


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
# 设置LoginManager的保护级别和登录视图
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message = ""


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(blueprint=main_blueprint, url_prefix='/main')
    from .user import user as user_blueprint
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    # from .editor import editor as editor_blueprint
    # app.register_blueprint(blueprint=editor_blueprint, url_prefix='/<projectId>/editor')
    # from .analysis import analysis as analysis_blueprint
    # app.register_blueprint(blueprint=analysis_blueprint, url_prefix='/<projectId>/analysis')
    # from .outline import outline as outline_blueprint
    # app.register_blueprint(blueprint=outline_blueprint, url_prefix='/<projectId>/outline')
    # from .scene import scene as scene_blueprint
    # app.register_blueprint(blueprint=scene_blueprint, url_prefix='/<projectId>/scene')
    # from .plan import plan as plan_blueprint
    # app.register_blueprint(blueprint=plan_blueprint, url_prefix='/<projectId>/plan')
    # from .actor import actor as actor_blueprint
    # app.register_blueprint(blueprint=actor_blueprint, url_prefix='/actor')
    # from .plots import plots as plots_blueprint
    # app.register_blueprint(blueprint=plots_blueprint, url_prefix='/<projectId>/plots')
    # from .drama import drama as drama_blueprint
    # app.register_blueprint(blueprint=drama_blueprint, url_prefix='/<projectId>/drama')
    # from .team import team as team_blueprint
    # app.register_blueprint(blueprint=team_blueprint, url_prefix='/team')

    return app
