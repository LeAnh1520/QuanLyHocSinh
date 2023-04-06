from flask import render_template, request, redirect, session, Flask
from QLHocSinh import app, dao, admin
from QLHocSinh import login
from flask_login import login_user, login_required, logout_user
import cloudinary.uploader
from QLHocSinh.admin import *

@app.route("/")
def index():
    return render_template("index.html")

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)

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


@app.route("/logout")
def my_logout():
    logout_user()
    return redirect('/login')

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
    app.run(debug=True)

