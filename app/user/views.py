# coding:utf8

from app.user import user
from flask_login import login_required, login_user, logout_user,current_user
from flask import jsonify, redirect, url_for, render_template, request, flash,session
from app.models.User import User
from app.models.company import Company
from .validate import generate_verification_image_code
from app import db


import sys
reload(sys)
sys.setdefaultencoding('utf8')


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
                    return redirect(request.args.get('next') or url_for('main.home'))
                elif user.fk_role==6:
                    return render_template('user/admin_info_complete.html')
                elif user.fk_role==11:
                    return render_template('user/user_info_complete.html')
                elif user.checked == 0:
                    return render_template('user/wait_company_check.html')
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
        return render_template('user/register.html',strs=strs)
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
            user.fk_role = 6
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email,'确认账户','user/email/email_body',user=user,token=token)
        login_user(user, True)
        return redirect(url_for('main.home'))

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

#当用户首次完善个人信息提交时的处理函数
@user.route('/user_info_complete',methods=['POST','GET'])
@login_required
def user_info_complete():
    if request.method == 'POST':
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        fk_role = request.form.get("fk_role")
        fk_company_id = request.form.get("fk_company_id")
        current_user.user_info_complete(gender,phone,fk_role,fk_company_id)
        db.session.add(current_user)
        db.session.commit()
        return render_template('user/wait_company_check.html')
    else:
        return redirect(url_for('main.home'))

#当公司管理员首次完善公司信息提交时的处理函数
@user.route('/admin_info_complete',methods=['POST','GET'])
@login_required
def admin_info_complete():
    if request.method == 'POST':
        company_name = request.form.get("company_name")
        owner = request.form.get("owner")
        address = request.form.get("address")
        tel = request.form.get("tel")
        email = request.form.get("email")
        contacts = request.form.get("contacts")
        contact_phone = request.form.get("contact_phone")
        company = Company(company_name,owner,contacts,contact_phone,email,address,tel)
        current_user.is_userInfo_completed = 1
        current_user.fk_company_id = company.id
        db.session.add(company)
        db.session.add(current_user)
        db.session.commit()
        return render_template('user/wait_company_check.html')
    else:
        return redirect(url_for('main.home'))