from QLHocSinh.models import Lop, HocSinh, User, MonHoc, Diem, Diem15, Diem45
from QLHocSinh import db, app
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


def get_classes():
    return db.session.query(Lop).all()

# Cho: lay bang diem cua cac hoc sinh trong 1 lop theo hoc ky, nam, mon
# def get_students_mark(class_id=None, semester=None, year=None, subject_id=None):
#     marks = db.session.query(MonHoc, HocSinh, Diem.semester, Diem.year, Diem15, Diem45, Diem.DiemThi, Diem.DiemTBHK1)\
#                                 .join(Diem, Diem.monhoc_id.__eq__(MonHoc.id))\
#                                 .join(HocSinh, HocSinh.id.__eq__(Diem.hocsinh_id))\
#                                 .join(Diem15, Diem15.id.__eq__(Diem.diem15_id), isouter=True)\
#                                 .join(Diem45, Diem45.id.__eq__(Diem.diem45_id), isouter=True)
#
#     if class_id:
#         marks = marks.filter(HocSinh.lop_id.__eq__(class_id))
#     if semester:
#         marks = marks.filter(Diem.hocky_id.__eq__(semester))
#     if year:
#         marks = marks.filter(Diem.year.__eq__(year))
#     if subject_id:
#         marks = marks.filter(Diem.monhoc_id.__eq__(subject_id))
#
#     return marks
#
# # Cho: tinh trung binh bo qua None.
# def average_ignore_none(numbers):
#     total = []
#     for n in numbers:
#         if n:
#             total.append(n)
#     if len(total) == 0:
#         return 0
#     avg = sum(total) / len(total)
#     return avg
#
# def cal_avg_mark(subject_id, semester, year):
#     marks = get_students_mark(subject_id=subject_id, semester=semester, year=year)
#
#     for s in marks:
#         if s.Diem15:
#             mark15 = average_ignore_none([s.Diem15.col1, s.Diem15.col2, s.Diem15.col3, s.Diem15.col4, s.Diem15.col5])
#         else:
#             mark15 = 0
#         if s.Diem45:
#             mark45 = average_ignore_none([s.Diem45.col1, s.Diem45.col2, s.Diem45.col3])
#         else:
#             mark45 = 0
#         if s.DiemThi:
#             avg = (mark15 + mark45 * 2 + s.DiemThi * 3) / 6
#         else:
#             avg = (mark15 + mark45 * 2) / 6
#         db.session.query(Diem).filter(Diem.monhoc_id.__eq__(subject_id),
#                                                Diem.hocsinh_id.__eq__(s.Student.id),
#                                                Diem.hocky_id.__eq__(semester),
#                                                Diem.year.__eq__(year)).update({Diem.avg: avg},
#                                                                               synchronize_session=False)
#     db.session.commit()
#
# def total_qualified_by_class(class_id, semester, year, subject_id):
#     cal_avg_mark(subject_id=subject_id, semester=semester, year=year)
#     count = db.session.query(func.count(Diem.avg)).\
#         join(HocSinh, HocSinh.id.__eq__(Diem.student_id)).\
#         join(Lop, Lop.id.__eq__(HocSinh.class_id)).\
#         filter(Lop.id.__eq__(class_id),
#                Diem.monhoc_id.__eq__(subject_id),
#                Diem.hocky_id.__eq__(semester),
#                Diem.year.__eq__(year),
#                Diem.DiemTBHK1.__ge__(5)).first()
#     return count[0]
#
# def get_stats(semester=None, year=None, subject_name=None):
#     classes = get_classes()
#     stats = []
#     subject_id = db.session.query(MonHoc.id).filter(MonHoc.ten.__eq__(subject_name)).first()
#
#     for c in classes:
#         total_qualified = total_qualified_by_class(c.id, semester=semester,
#                                                    year=year, subject_id=(subject_id[0] if subject_id else 0))
#         total = c.total if c.total else 0
#         stats.append({
#             'class_id': c.id,
#             'class_name': c.lop + c.ten,
#             'total': total,
#             'total_qualified': total_qualified,
#             'ratio': "{0:.2f}".format((float(total_qualified) / total * 100) if total != 0 else 0)
#         })
#
#     return stats



