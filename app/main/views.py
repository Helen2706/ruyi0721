# coding:utf8

from . import main
from app.models.Menu import Menu
from flask import render_template
from flask_login import current_user
from app.models.Role_menu import Role_menu
from app.models.User_role import User_role

@main.route('/')
# 对不同角色的用户显示不同的菜单
def home():
    # menu_list存储menu_id集合，menus2为对应的二级Menu类列表
    menu_list = set()
    menus2 = []

    # 根据当前用户的ID查找该用户的角色（用户与角色是一对多的关系）
    userid = current_user.get_id()
    user_roles = User_role.query.filter_by(fk_user_id=userid).all()

    # 对每一个角色查找所有的菜单id
    for user_role in user_roles:
        user_roleid = user_role.role_id
        # role_menus是当前角色的所有角色-菜单对应表中的记录
        role_menus = Role_menu.query.filter_by(fk_role_id=user_roleid).all()
        for role_menu in role_menus:
            menu_id = role_menu.fk_menu_id
            menu_list.add(menu_id)
    # 获得该用户所有菜单id列表
    menu_list = list(menu_list)
    menu_list.sort()
    for menu_list_id in menu_list:
        menus = Menu.query.filter_by(id=menu_list_id).first()
        menus2.append(menus)
    menus1 = Menu.query.filter_by(rank=1).all()
    return render_template('main.html', menus1=menus1, menus2=menus2)
