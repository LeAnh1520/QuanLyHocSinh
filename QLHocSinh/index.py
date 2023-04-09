from flask import render_template, request, redirect, session, Flask
from QLHocSinh import app, dao, admin
from QLHocSinh import login
from flask_login import login_user, login_required, logout_user
import cloudinary.uploader
from QLHocSinh.admin import *

@app.route("/")
def index():
    return render_template("dashboard.html")

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

# @app.route('/add-students', methods=['GET', 'POST'])
@app.route('/add-students')
@login_required
def add_students():
    if current_user.user_role == UserRole.NV:
        if request.args.get('err_msg'):
            return render_template("add-students.html", err_msg=request.args.get('err_msg'))

    return render_template("add-students.html")

@app.route('/add-students', methods=['GET', 'POST'])
@login_required
def out_student():
    if current_user.user_role == UserRole.QTV:
        if request.method.__eq__('POST'):
            first_name = request.form.get('ten')
            last_name = request.form.get('hoten')
            sex = request.form.get('gioitinh')
            bday = request.form.get('ngaysinh')
            address = request.form.get('diachi')
            phone = request.form.get('sdt')
            email = request.form.get('email')

        dao.add_student(first_name=first_name,
                                    last_name=last_name,
                                    sex=sex,
                                    bday=bday,
                                    address=address,
                                    phone=phone,
                                    email=email)
        info_student = {
                'ten': first_name,
                'hoten': last_name,
                'gioitinh': 'Nam' if sex == 'male' else 'Nữ',
                'ngaysinh': 'Ngày ' + bday.split('-')[2] + ' Tháng ' + bday.split('-')[1] + ' Năm ' + bday.split('-')[0],
                'diachi': address,
                'sdt': phone,
                'email': email
            }
        return render_template("out-student.html", info_student=info_student)
    else:
        return redirect("/")

@app.route("/setup-class")
def setup_class():
    return render_template("setup-class.html")

@app.route("/arrange-class")
def arrange_class():
    return render_template("arrange-class.html")

# @app.route("/students-marks")
# @login_required
# def students_marks():
#     course_id = request.args.get('course_id')
#     keyword = request.args.get('keyword')
#     classes = dao.get_classes_of_teacher(current_user.id)
#     if keyword:
#         filtered_classes = []
#         for c in classes:
#             for i in c:
#                 if keyword.lower() in str(i).lower():
#                     if c not in filtered_classes:
#                         filtered_classes.append(c)
#
#         return render_template("students-marks.html", classes=filtered_classes)
#
#     if course_id:
#         if dao.check_teacher_access(user_id=current_user.id, course_id=course_id):
#             course = dao.get_course_info(course_id)
#             dao.create_all_mark_records(course_id=course_id) # Tao bang diem khi vao nhap diem
#             marks = utilities.get_mark_by_course_id(course_id=course_id)
#
#             return render_template("students-marks.html",
#                                    marks=marks,
#                                    course=course,
#                                    classes=classes)
#         else:
#             return redirect("/")
#     else:
#         return render_template("students-marks.html", classes=classes)


if __name__ == '__main__':
    app.run(debug=True)

