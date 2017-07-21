# coding:utf8

from app.user import user
from flask_login import login_required, login_user, logout_user
from flask import jsonify, redirect, url_for, render_template, request, flash,session
from app.models.User import User
from .validate import generate_verification_image_code
from app import db


import sys
reload(sys)
sys.setdefaultencoding('utf8')


@user.route('/')
@login_required
def index():
    return redirect(url_for('main.home'))


@user.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            if user.verify_password(password):
                login_user(user)
                if user.is_userInfo_completed:
                    return redirect(request.args.get('next') or url_for('user.index'))
                elif user.fk_role==1:
                    return render_template('user/admin_first_login.html')
                elif user.fk_role==11:
                    return render_template('user/user_first_login.html')
            else:
                flash("用户名或密码错误！")
        else:
            flash("用户不存在")
    return render_template('user/login.html')

#登录时检查用户名是否存在
@user.route('/login/validate/username',methods=['POST','GET'])
def loginValidateUsername():
    username = request.form.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify(True)
    return jsonify(False)

#检查用户名密码是否正确
@user.route('/validate/password',methods=['POST','GET'])
def validatepassword():
    username = request.form.get("username")       # 获取用户输入的信息
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):     #若与数据库中用户名密码匹配，返回true
        return jsonify(True)    # 返回json数据true，接收方会自动解析，当返回true时不显示信息
    return jsonify(False)       # 当返回false时显示“用户名或密码错误”

# 用户注册
@user.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        strs = generate_verification_image_code()
        session['code_text'] = strs
        return render_template('user/register.html')
    else:
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        #telephone = request.form.get("telephone")
        #confirmcode = request.form.get("confirmcode")
        user = User(email, username, password)
        userRole = request.form.get("userRole")
        if userRole == 'companyStaff':
            user.fk_role = 11
        else:
            user.fk_role = 1
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email,'确认账户','user/email/email_body',user=user,token=token)
        login_user(user, True)
        return render_template("user/emailInfo.html")




#注册时检查邮箱是否存在
@user.route('/validate/email',methods=['POST','GET'])
def validateemail():
    email = request.form.get('email')
    if User.query.filter_by(email=email).first():
        return jsonify(False)
    return jsonify(True)



#注册时检查用户名是否存在
@user.route('register/validate/username',methods=['POST','GET'])
def registerValidateUsername():
    username = request.form.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify(False)
    return jsonify(True)


#检查验证码是否正确
@user.route('/validate/confirmcode',methods=['POST','GET'])
def validateconfirmcode():
    confirmcode = request.form.get('confirmcode')
    if confirmcode == session['code_text']:
        return jsonify(True)
    return jsonify(False)


#用户协议
@user.route('/register/protocol')
def register_protocol():
    return render_template("user/register_protocol.html")


# 注销用户
@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已注销登录')
    return redirect(url_for('user.login'))
