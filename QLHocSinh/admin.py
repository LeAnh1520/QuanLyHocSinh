from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from QLHocSinh import app, db, dao
from QLHocSinh.models import GiaoVien, NhanVien, QuanTriVien, MonHoc, HocSinh, HocKy, UserRole, User, Lop
from flask_login import logout_user, current_user
from flask_admin import BaseView, expose
from flask import redirect, request

#Vào trang admin

class AuthenticatedBaseView(BaseView):
    def __index__(self):
        return current_user.is_authenticated
class AuthenticatedModelView(ModelView):
    page_size = 10
    create_modal = True
    edit_modal = True
    column_display_all_relations = True
    column_labels = {
        'ten': 'Họ',
        'hoten': 'Tên',
        'ngaysinh': 'Ngày sinh',
        'gioitinh': 'Giới tính',
        'diachi': 'Địa chỉ',
        'sdt': 'SĐT',
        'email': 'Email',
        'ngaybatdau': 'Ngày gia nhập',
        'active': 'Active',
        'user': 'Tài khoản',
        'lop': 'Lớp',
        'name': 'Tên người dùng',
        'username': 'Tài khoản',
        'password': 'Mật khẩu',
        'avatar': 'Ảnh đại diện',
        'user_role': 'Chức vụ',
        #'classes': 'Các lớp phụ trách',
        'giaovien': 'Giáo viên',
        #'class_room': 'Lớp',
        'hocsinh': 'Học sinh',
        'nhanvien': 'Nhân viên',
        'mon': 'Môn',
        'hocky': 'Năm',
        #'course': 'Khóa học'
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.QTV



class AdminBaseView(AuthenticatedBaseView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.user_role == UserRole.QTV


class UserView(ModelView):
    can_view_details = True
    column_searchable_list = ['name', 'username']
    column_filters = ['name']
    column_exclude_list = ['avatar']
    column_labels = {
        'name': 'Tên',
        'username': 'Tên đăng nhập',
        'password': 'Mật khẩu',
        'user_role': 'Chức vụ'
    }
class PersonView(ModelView):
    can_view_details = True
    column_searchable_list = ['ten', 'hoten', 'email']
    column_filters = ['ten', 'hoten']
    column_exclude_list = ['avatar', 'chuyenmon']
    column_labels = {
        'ten': 'Tên',
        'hoten': 'Họ',
        'ngaysinh': 'Ngày sinh',
        'gioitinh': 'Giới tính',
        'diachi': 'Địa chỉ',
        'sdt': 'Số điện thoại',
        'ngaybatdau': 'Ngày bắt đầu'
    }

class HocSinhView(ModelView):
    can_view_details = True
    column_searchable_list = ['ten', 'hoten']
    column_filters = ['ten', 'hoten']
    column_exclude_list = ['avatar', 'chuyenmon']
    column_labels = {
        'ten': 'Tên',
        'hoten': 'Họ',
        'ngaysinh': 'Ngày sinh',
        'gioitinh': 'Giới tính',
        'diachi': 'Địa chỉ',
        'sdt': 'Số điện thoại',
        'ngaybatdau': 'Ngày bắt đầu'
    }

class MonHocView(ModelView):
    can_view_details = True
    column_searchable_list = ['ten']
    column_filters = ['ten']
    column_labels = {
        'ten': 'Tên'
    }

class LopView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_searchable_list = ['khoi','ten']
    column_filters = ['khoi','ten']
    column_labels = {
        'khoi': 'Khối',
        'ten': 'Tên lớp',
        'siso': 'Sĩ số'
    }

class LapDanhSachLop(BaseView):
    @expose('/')
    def __index__(self):
        return redirect("/setup-class")

class SapXepLop(BaseView):
    @expose('/')
    def __index__(self):
        return redirect("/arrange-class")

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render("admin/stats.html")

class LogoutView(AuthenticatedBaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

class DiemView(ModelView):
    column_display_pk = True



admin = Admin(app, name='QUẢN TRỊ TRƯỜNG THPT', template_mode='bootstrap4')
admin.add_view(UserView(User, db.session, name='Tài khoản'))
admin.add_view(PersonView(GiaoVien, db.session, name='Giáo viên', category= "Cá nhân"))
admin.add_view(PersonView(NhanVien, db.session, name='Nhân viên', category= "Cá nhân"))
admin.add_view(PersonView(QuanTriVien, db.session, name='Quản trị viên', category= "Cá nhân"))
admin.add_view(HocSinhView(HocSinh, db.session, name="Học sinh"))
admin.add_view(MonHocView(MonHoc, db.session, name="Môn học"))
admin.add_view(LopView(Lop, db.session, name='Danh sách lớp học', category= "Lớp học"))
admin.add_view(LapDanhSachLop(name='Lập danh sách lớp', category= "Lớp học"))
admin.add_view(SapXepLop(name='Điều chỉnh lớp học', category= "Lớp học"))


admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Logout'))

