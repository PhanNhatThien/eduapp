from _ast import In

from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, backref

from edu import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class Lop(db.Model):

    __tablename__ = 'lop'

    id_lop = Column(Integer, primary_key=True, autoincrement=True)
    ten_lop = Column(String(15), nullable=False, unique=True)
    si_so = Column(Integer)

    hocsinh = relationship('HocSinh', backref='lop', lazy=True)

    def __str__(self):
        return self.ten_lop


class HocSinh(db.Model):
    __tablename__ = 'hocsinh'

    id_hoc_sinh = Column(Integer, primary_key=True, unique=True)
    ten_hoc_sinh = Column(String(50), nullable=False)
    ngay_sinh = Column(DateTime)
    email = Column(String(50), nullable=False, unique=True)
    so_dien_thoai = Column(String(50))
    gioi_tinh = Column(String(50), nullable=False)
    anh = Column(String(100))
    dia_chi = Column(String(100))
    ghi_chu = Column(String(100))

    lop_id = Column(Integer, ForeignKey(Lop.id_lop))


    def __str__(self):
        return self.ten_hoc_sinh

class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2
    TEACHER = 3
    STUDENT = 4

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.STUDENT)

    def __str__(self):
        return self.name

class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    so_tuoi_toi_thieu = Column(Integer)
    so_tuoi_toi_da = Column(Integer)
    si_so_lop = Column(Integer)

class KyHoc(db.Model):
    id_hoc_ky = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(25), default='HK1', nullable=False)
    nam_hoc = Column(String(25), nullable=False)

    diem = relationship('Diem', backref='kyhoc', lazy=True)

    def __str__(self):
        return self.ten

class MonHoc(db.Model):
    __tablename__ = 'monhoc'
    id_mon_hoc = Column(Integer, primary_key=True, autoincrement=True)
    ten_mon_hoc = Column(String(30), nullable=False)

    diem = relationship('Diem', backref='monhoc', lazy=False)

    def __str__(self):
        return self.id_mom_hoc

class Diem(db.Model):
    id_hoc_sinh = Column(Integer, ForeignKey(HocSinh.id_hoc_sinh), primary_key=True)
    id_mon_hoc = Column(Integer, ForeignKey(MonHoc.id_mon_hoc), primary_key=True)
    id_hoc_ky = Column(Integer, ForeignKey(KyHoc.id_hoc_ky), primary_key=True)
    Diem15p_1 = Column(Float, default=0)
    Diem15p_2 = Column(Float, default=0)
    Diem15p_3 = Column(Float, default=0)
    Diem15p_4 = Column(Float, default=0)
    Diem15p_5 = Column(Float, default=0)

    Diem1Tiet_1 = Column(Float, default=0)
    Diem1Tiet_2 = Column(Float, default=0)
    Diem1Tiet_3 = Column(Float, default=0)

    DiemCK = Column(Float, default=0)
    DiemTB = Column(Float, default=0)


if __name__ == '__main__':
    with app.app_context():

        # c1 = Lop(ten_lop='1A', si_so='5')
        # c2 = Lop(ten_lop='2B', si_so='5')
        # c3 = Lop(ten_lop='3C', si_so='5')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        # s1 = HocSinh(ten_hoc_sinh='Trần Văn Phương', ngay_sinh='2001-1-29 00:00:00', email='vanphuong@gmail.com',
        #              so_dien_thoai='0332123762',
        #              gioi_tinh='Nam',
        #              anh='https://res.cloudinary.com/dogosq8z4/image/upload/v1660017463/odvuo7ehpgj00r7hzc6a.png',
        #              dia_chi='Vũng Tàu',
        #              ghi_chu='khônng',
        #              lop_id=1)
        # s2 = HocSinh(ten_hoc_sinh='Phan Nhất Thiện', ngay_sinh='2001-1-1 00:00:00', email='thien@gmail.com',
        #              so_dien_thoai='123',
        #              gioi_tinh='Nam',
        #              anh='https://res.cloudinary.com/dogosq8z4/image/upload/v1660017463/odvuo7ehpgj00r7hzc6a.png',
        #              dia_chi='TPHCM',
        #              ghi_chu='khônng',
        #              lop_id=1)
        #
        #
        # db.session.add_all([s1, s2])
        # db.session.commit()

        # k1 = KyHoc(ten='HK1', nam_hoc='2020')
        # k2 = KyHoc(ten='HK2', nam_hoc='2020')
        # k3 = KyHoc(ten='HK3', nam_hoc='2020')
        #
        # db.session.add(k1)
        # db.session.add(k2)
        # db.session.add(k3)
        # db.session.commit()
        #
        # m1 = MonHoc(ten_mon_hoc='Toán')
        # m2 = MonHoc(ten_mon_hoc='Lý')
        # m3 = MonHoc(ten_mon_hoc='Hóa')
        #
        # db.session.add(m1)
        # db.session.add(m2)
        # db.session.add(m3)
        # db.session.commit()

        db.create_all()




