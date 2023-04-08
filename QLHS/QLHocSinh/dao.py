from QLHocSinh.models import Lop, HocSinh, User, MonHoc, Diem, Diem15, Diem45, GiaoVien, KhoaHoc
from QLHocSinh import db, app
from datetime import datetime

from flask_login import current_user
from sqlalchemy import func
import hashlib

# def get_hocsinh(kw=None, lop_id=None):
#     query = HocSinh.query
#
#     if kw:
#         query = query.filter(HocSinh.name.contains(kw))
#
#     if lop_id:
#         query = query.filter(HocSinh.Lop.__eq__(lop_id))
#
#     return query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def auth_user(username, password):
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()
def check_login(username, password):
    if username and password:
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def add_student(first_name, last_name, sex, bday, address, phone, email):
    if sex == 'male':
        sex = True
    else:
        sex = False
    # if config.min_age <= (datetime.now() - parser.parse(bday)).days / 365 <= config.max_age:

    student = HocSinh(ten=first_name,
                    hoten=last_name,
                    gioitinh=sex,
                    ngaysinh=bday,
                    diachi=address,
                    sdt=phone,
                    email=email)

    db.session.add(student)
    db.session.commit()
    # else:
    #     return "Tuổi không hợp lệ"

def get_classes():
    return db.session.query(Lop).all()

def get_course_info(course_id):
    return db.session.query(Lop.khoi, Lop.ten, MonHoc.ten, KhoaHoc.year)\
            .join(Lop, Lop.id.__eq__(KhoaHoc.lop_id))\
            .join(MonHoc, MonHoc.id.__eq__(KhoaHoc.monhoc_id)).filter(KhoaHoc.id.__eq__(course_id)).first()


def get_teacher_id(user_id):
    return db.session.query(GiaoVien.id).filter(GiaoVien.user_id.__eq__(user_id))

def get_classes_of_teacher(user_id):
    teacher_id = get_teacher_id(user_id=user_id)

    return db.session.query(MonHoc.ten, Lop.khoi + Lop.ten, KhoaHoc.id)\
             .join(KhoaHoc, KhoaHoc.monhoc_id.__eq__(MonHoc.id))\
             .join(Lop, Lop.id.__eq__(KhoaHoc.lop_id))\
             .filter(KhoaHoc.giaovien_id.__eq__(teacher_id)).all()

def check_teacher_access(user_id, course_id=None, student_id=None, subject_id=None):
    teacher_id = get_teacher_id(user_id=user_id).first()[0]

    if course_id:
        course = KhoaHoc.query.get(course_id)
        print("teacher_id")
        print(course.teacher_id)
        if teacher_id == course.teacher_id:
            return True

    if student_id and subject_id:
        class_id = HocSinh.query.get(student_id).lop_id
        course = db.session.query(KhoaHoc)\
                   .join(HocSinh, HocSinh.lop_id.__eq__(KhoaHoc.lop_id))\
                   .filter(KhoaHoc.giaovien_id.__eq__(teacher_id),
                           KhoaHoc.monhoc_id.__eq__(subject_id),
                           KhoaHoc.lop_id.__eq__(class_id)).first()
        if teacher_id == course.teacher_id:
            return True

    return False

def create_all_mark_records(course_id=None):
    course = KhoaHoc.query.get(course_id)
    students_already_have = db.session.query(Diem.hocsinh_id).filter(Diem.monhoc_id.__eq__(course.subject_id),
                                                                     Diem.year.__eq__(course.year)).distinct()
    students_have_no_record = db.session.query(HocSinh.id)\
                                .filter(HocSinh.lop_id.__eq__(course.class_id),
                                        HocSinh.id.not_in(students_already_have))

    for s in students_have_no_record:
        diem15_1 = Diem15()
        diem15_2 = Diem15()
        diem45_1 = Diem45()
        diem45_2 = Diem45()

        db.session.add(diem15_1)
        db.session.add(diem15_2)
        db.session.add(diem45_1)
        db.session.add(diem45_2)

        mark1 = Diem(monhoc_id=KhoaHoc.monhoc_id,
                     hocsinh_id=s[0],
                     hocki=1,
                     year=course.year,
                     mark15=mark15_1,
                     mark45=mark45_1)
        db.session.add(mark1)

        mark2 = Mark(subject_id=course.subject_id,
                     student_id=s[0],
                     semester=2,
                     year=course.year,
                     mark15=mark15_2,
                     mark45=mark45_2)
        db.session.add(mark2)

    db.session.commit()

