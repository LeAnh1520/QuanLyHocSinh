from flask import render_template, request, redirect, session, Flask
from QLHocSinh import app, dao, admin
from QLHocSinh import login
from flask_login import login_user, logout_user
import cloudinary.uploader


@app.route("/")
def index():
    return render_template("index.html")

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id=user_id)

@app.route('/login')
def my_login():
    return render_template('login.html')

@app.route("/login", methods=['post'])
def my_login_process():
    username = request.form['username']
    password = request.form['password']
    u = dao.auth_user(username, password)
    if u:
        login_user(user=u)

        next_page = request.args.get('next')
        return redirect(next_page if next_page else '/')

    return render_template('login.html')

@app.route("/logout")
def my_logout():
    logout_user()
    return redirect("/login")



if __name__ == '__main__':
    app.run(debug=True)

