from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from QLHocSinh import app, db
from QLHocSinh.models import GiaoVien, MonHoc

admin = Admin(app, name='QUẢN TRỊ TRƯỜNG THPT', template_mode='bootstrap4')
admin.add_view(ModelView(GiaoVien, db.session))
admin.add_view(ModelView(MonHoc, db.session))
