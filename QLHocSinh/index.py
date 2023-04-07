from flask import render_template, request, redirect, session, Flask, url_for
from flask_login import login_user, login_required, logout_user
from QLHocSinh.admin import *
from QLHocSinh import app, dao, admin, login
import cloudinary.uploader
import utilities

@app.route("/")
def index():
    return render_template("index.html")

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)

# @login.user_loader
# def user_load(id):
#     return utilities.get_user_by_id(id=id)

@app.route('/login')
def my_login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    error_msg = ""
    if current_user.is_authenticated:
        return redirect('/')
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = dao.check_login(username=username, password=password)
            if user:
                login_user(user=user)
                if current_user.user_role == UserRole.QTV:
                    return redirect('/admin')
                next = request.args.get('next', '/')
                return redirect(next)
            else:
                error_msg = "Sai tài khoản hoặc mật khẩu !!!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)

# @app.route("/login", methods=['get', 'post'])
# def my_login():
#     err_msg = ''
#     if request.method.__eq__('POST'):
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         user = utilities.check_login(username=username, password=password)
#         if user:
#             login_user(user=user)
#             return redirect(url_for('index'))
#         else:
#             err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác'
#     return render_template('login.html', err_msg=err_msg)

@app.route("/logout")
def my_logout():
    logout_user()
    return redirect(url_for('my_login'))

@app.route("/add-students")
def add_students():
    return render_template("add-students.html")

@app.route("/setup-class")
def setup_class():
    return render_template("setup-class.html")

@app.route("/arrange-class")
def arrange_class():
    return render_template("arrange-class.html")

if __name__ == '__main__':
    from QLHocSinh.admin import *
    # app.run(debug=True)
    app.run()

