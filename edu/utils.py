from edu import app, db
from edu.models import *
import hashlib
from sqlalchemy import func
from sqlalchemy import or_

from edu.models import HocSinh


def get_class():
    return Lop.query.all()


def get_quy_dinh():
    return QuyDinh.query.get(1)

def check_login(username, password, role=UserRole.STUDENT):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)



def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()

def load_student(lop_id=None, kw=None):

    query = HocSinh.query.filter()
    if lop_id:
        query = query.filter(HocSinh.lop_id.__eq__(lop_id))

    if kw:
        query = query.filter(HocSinh.ten_hoc_sinh.contains(kw))

    return query.all()

def count_student():
    q = db.session.query(Lop.ten_lop, func.count(HocSinh.id_hoc_sinh))\
        .join(HocSinh, HocSinh.lop_id == Lop.id_lop, isouter=True) \
        .group_by(Lop.id_lop)

    return q.all()

def add_student(hoten, email, gioitinh, lop, **kwargs):
    hocsinh = HocSinh(ten_hoc_sinh=hoten.strip(),
                      email=email.strip(),
                      gioi_tinh=gioitinh.strip(),
                      lop_id=int(lop),
                      ngay_sinh=kwargs.get('ngaysinh'),
                      so_dien_thoai=kwargs.get('sdt'),
                      anh=kwargs.get('anh'),
                      dia_chi=kwargs.get('diachi'),
                      ghi_chu=kwargs.get('ghichu'))

    db.session.add(hocsinh)
    db.session.commit()




def load_mon_hoc():
    return MonHoc.query.all()

def load_ky_hoc():
    return KyHoc.query.all()

def load_hoc_sinh_lop1():
    query = HocSinh.query.filter(HocSinh.lop_id.__eq__(1))

    return query

def add_diem(idhs, idmh, idhk,**kwargs):
    diem = Diem(id_hoc_sinh= int(idhs),
                id_mon_hoc = int(idmh),
                id_hoc_ky = int(idhk),
                Diem15p_1=kwargs.get('diem151'), Diem15p_2=kwargs.get('diem152'), Diem15p_3=kwargs.get('diem153'), Diem15p_4=kwargs.get('diem154'), Diem15p_5=kwargs.get('diem155'),
                Diem1Tiet_1=kwargs.get('diem601'), Diem1Tiet_2=kwargs.get('diem602'), Diem1Tiet_3=kwargs.get('diem603'),
                DiemCK=kwargs.get('diemck'), DiemTB=kwargs.get('diemtb'))

    db.session.add(diem)
    db.session.commit()


def xuat_diem(id_mon_hoc=None):
    q = db.session.query(HocSinh.ten_hoc_sinh, Lop.ten_lop, KyHoc.ten, Diem.DiemTB)\
        .join(Diem, HocSinh.id_hoc_sinh.__eq__(Diem.id_hoc_sinh))\
        .join(Lop, Lop.id_lop.__eq__(HocSinh.lop_id))\
        .join(KyHoc, KyHoc.id_hoc_ky.__eq__(Diem.id_hoc_ky)) \
        # .all()

    if id_mon_hoc:
        q = q.filter(Diem.id_mon_hoc.__eq__(id_mon_hoc))\
            # .all()


    return q.all()



def ket_qua(id_mon=None, id_hoc_ky=None):
    q = db.session.query(HocSinh.ten_hoc_sinh, Lop.ten_lop, MonHoc.ten_mon_hoc, Diem.DiemTB) \
        .join(Lop, Lop.id_lop.__eq__(HocSinh.lop_id)) \
        .join(Diem, HocSinh.id_hoc_sinh.__eq__(Diem.id_hoc_sinh)) \
        .filter(Diem.id_mon_hoc.__eq__(MonHoc.id_mon_hoc))

    if id_mon and id_hoc_ky :
        q = q.filter(Diem.id_mon_hoc.__eq__(id_mon), Diem.id_hoc_ky.__eq__(id_hoc_ky))\

    return q.all()

def thong_ke(id_mon=None, id_hoc_ky=None):
    q = db.session.query(Lop.ten_lop, Lop.si_so, func.count(HocSinh.id_hoc_sinh), (func.count(HocSinh.id_hoc_sinh)/Lop.si_so)) \
        .join(HocSinh, Lop.id_lop.__eq__(HocSinh.lop_id)) \
        .join(Diem, HocSinh.id_hoc_sinh.__eq__(Diem.id_hoc_sinh)) \
        .join(MonHoc, Diem.id_mon_hoc.__eq__(MonHoc.id_mon_hoc))\
        .filter(Diem.DiemTB >= 5)\
        .group_by(Lop.ten_lop)

    if id_mon and id_hoc_ky :
        q = q.filter(Diem.id_mon_hoc.__eq__(id_mon), Diem.id_hoc_ky.__eq__(id_hoc_ky))\

    return q.all()


def lop_hoc_stats():
    return db.session.query(Lop.id_lop, Lop.ten_lop, func.count(HocSinh.id_hoc_sinh))\
                .join(HocSinh, Lop.id_lop.__eq__(HocSinh.lop_id), isouter=True)\
                .group_by(Lop.id_lop).all()

