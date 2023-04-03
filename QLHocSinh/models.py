from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date, CheckConstraint, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship,  backref
from QLHocSinh import db, app
from flask_login import UserMixin
from datetime import datetime
from enum import Enum as UserEnum

#Thiết kế bảng trong mySQL
class UserRole(UserEnum):
    QTV = 0
    NV = 1
    GV = 2

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer,primary_key=True, autoincrement=True)

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), nullable=False)
    quantrivien = relationship('QuanTriVien', backref='user', lazy=True)
    giaovien = relationship('GiaoVien', backref='user', lazy=True)
    nhanvien = relationship('NhanVien', backref='user', lazy=True)

class HoSo(BaseModel):
    __abstract__ = True

    ten = Column(String(20), nullable=False)
    hoten = Column(String(20), nullable=False)
    ngaysinh = Column(DateTime, nullable=False)
    gioitinh = Column(Boolean, default=True)
    diachi = Column(String(100))
    sdt = Column(String(15))
    email = Column(String(50))
    ngaybatdau = Column(DateTime, default=datetime.now())
    chuyenmon = Column(Boolean, default=True)

    def __str__(self):
        return self.ten + ' ' + self.hoten

class Lop(BaseModel):
    lop = Column(String(5), nullable=False)
    ten = Column(String(10), nullable=False)
    siso = Column(Integer, default=0)
    hocsinh = relationship('HocSinh', backref='lop', lazy=False)
    # teachers = relationship('Teacher', secondary='course', lazy='subquery',
    #                         backref=backref('classroom', lazy=True))

    def __str__(self):
        return self.grade + self.name

class HocSinh(BaseModel):
    __table_args__ = (
        CheckConstraint('(year(ngaybatdau) - year(ngaysinh)) > 14', name='chk_age1'),
        CheckConstraint('(year(ngaybatdau) - year(ngaysinh)) < 21', name='chk_age2')
    )

    ten = Column(String(20), nullable=False)
    hoten = Column(String(20), nullable=False)
    ngaysinh = Column(Date, nullable=False)
    gioitinh = Column(Boolean, default=True)
    diachi = Column(String(100))
    sdt = Column(String(15))
    email = Column(String(50))
    ngaybatdau = Column(Date, default=datetime.now())
    lop_id = Column(Integer, ForeignKey(Lop.id))

class GiaoVien(HoSo):
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    #classes = relationship('ClassRoom', secondary='course', lazy='subquery',
                           #backref=backref('teacher', lazy=True))

class QuanTriVien(HoSo):
    user_id = Column(Integer, ForeignKey(User.id), unique=True)

class NhanVien(HoSo):
    user_id = Column(Integer, ForeignKey(User.id), unique=True)

class MonHoc(BaseModel):
    ten = Column(String(20), nullable=False)

    def __str__(self):
        return self.ten

class HocKy(BaseModel):
    hocky = Column(String(20), nullable=False)

class Diem15(BaseModel):

    col1 = Column(Float)
    col2 = Column(Float)
    col3 = Column(Float)
    col4 = Column(Float)
    col5 = Column(Float)
    diem = relationship('Diem', backref='diem15', lazy=True)

class Diem45(BaseModel):
    col1 = Column(Float)
    col2 = Column(Float)
    col3 = Column(Float)
    diem = relationship('Diem', backref='diem45', lazy=True)

class Diem(db.Model):
    monhoc_id = Column(Integer, ForeignKey(MonHoc.id), primary_key=True, nullable=False)
    hocsinh_id = Column(Integer, ForeignKey(HocSinh.id), primary_key=True, nullable=False)
    hocky_id = Column(Integer,ForeignKey(HocKy.id), primary_key=True)
    year = Column(Integer, primary_key=True)
    diem15_id = Column(Integer, ForeignKey(Diem15.id), unique=True)
    diem45_id = Column(Integer, ForeignKey(Diem45.id), unique=True)
    DiemThi = Column(Float)
    DiemTBHK1 = Column(Float)
    DiemTBHK2 = Column(Float)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

