from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from QLHocSinh import app, db
from QLHocSinh.models import GiaoVien, NhanVien, QuanTriVien, MonHoc, HocSinh, HocKy, Diem, Diem15, Diem45, UserRole, User
from flask_login import logout_user, current_user
from flask_admin import BaseView

#Vào trang admin
class AuthenticatedView(BaseView):
    def is_accessible(self):
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

class MonHocView(ModelView):
    pass

admin = Admin(app, name='QUẢN TRỊ TRƯỜNG THPT', template_mode='bootstrap4')
admin.add_view(ModelView(GiaoVien, db.session, name='Giáo viên'))
admin.add_view(ModelView(MonHoc, db.session, name='Môn học'))
admin.add_view(ModelView(User, db.session, name='Người dùng'))


