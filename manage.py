# coding:utf8

from flask_script import Manager, Server
from app import create_app
from flask import redirect, url_for

myApp = create_app('default')
manager = Manager(myApp)
manager.add_command('runserver', Server('127.0.0.1', 5000))

@myApp.route('/')
def index():
    return redirect(url_for('user.index'))

# 路由重定向，全部交给geteditor处理
@myApp.route('/<projectId>/')
def select_project(projectId):
    if not str(projectId).startswith('No'):
        return ''
    return redirect(url_for('editor.getEditor', projectId=projectId))

if __name__ == '__main__':
    manager.run(default_command='runserver')