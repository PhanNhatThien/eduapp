from pip._internal import utils

from edu import app, login
from flask import render_template, request, redirect, url_for
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/user-login", methods=['get', 'post'])
def user_signin():

    err_msg =""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg =" Uername hoac password khong dung!!"
    return render_template('login.html', err_msg=err_msg)

@app.route('/admin-login', methods=['post', 'get'])
def signin_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password,
                             role=UserRole.ADMIN)
    if user:
        login_user(user=user)
        return redirect('/admin')
    return redirect('/admin')

@app.route('/employee-login', methods=['post', 'get'])
def signin_employee():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password,
                                 role=UserRole.EMPLOYEE)
        if user:
            login_user(user=user)
            return redirect(url_for('add_student'))
        else:
            err_msg = " Uername hoac password khong dung!!"
    return render_template('login_employee.html', err_msg=err_msg)

@app.route('/teacher-login', methods=['post', 'get'])
def signin_teacher():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password,
                                 role=UserRole.TEACHER)
        if user:
            login_user(user=user)
            return redirect(url_for('bang_diem'))
        else:
            err_msg = " Uername hoac password khong dung!!"
    return render_template('login_teacher.html', err_msg=err_msg)



@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)

@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg =""

    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')

                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name,
                               username=username,
                               password=password,
                               email=email,
                               avatar=avatar_path)
                return redirect(url_for("user_signin"))
            else:
                err_msg = 'Mat khau khong khop !!!'
        except Exception as ex:
            err_msg = 'Dang co loi ' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route("/student/add", methods=["get", "post"])
def add_student():
    err_msg = ""

    lop = utils.get_class()

    tuoi = utils.get_quy_dinh()

    date_now = int((datetime.now()).year)

    if request.method.__eq__('POST'):
        hoten = request.form.get('hoten')
        ngaysinh = request.form.get('ngaysinh')
        sdt = request.form.get('sdt')
        gioitinh = request.form.get('gioitinh')
        diachi = request.form.get('diachi')
        email = request.form.get('email')
        lop = request.form.get('lop', 0)
        anh_path = None

        do_tuoi = int(ngaysinh[0:4])

        try:
            # if 15 <= (date_now - do_tuoi) <= 20:
            if tuoi.so_tuoi_toi_thieu <= (date_now - do_tuoi) <= tuoi.so_tuoi_toi_da:
                anh = request.files.get('anh')

                if anh:
                    res = cloudinary.uploader.upload(anh)
                    anh_path = res['secure_url']
                utils.add_student(hoten=hoten,
                                   ngaysinh=ngaysinh,
                                   email=email,
                                   lop=lop,
                                   gioitinh=gioitinh,
                                   anh=anh_path,
                                  sdt=sdt,
                                  diachi=diachi
                                  )
                return redirect(url_for("add_student"))
            else:
                err_msg = 'học sinh tiếp nhận có độ tuổi từ 15 đến  20 tuổi !!!'
        except Exception as ex:
            err_msg = 'Dang co loi ' + str(ex)

    return render_template('student-add.html',
                           lop=lop,
                           tuoi=tuoi,
                           err_msg=err_msg)

@app.route("/lophoc")
def lop_hoc():
    lop = utils.get_class()

    hocsinh = utils.load_student(lop_id=request.args.get('lop_id'),
                                 kw=request.args.get('keyword'))


    siso = utils.count_student()

    return render_template('lophoc.html',
                           lop=lop,
                           hocsinh=hocsinh,
                           siso=siso)



@app.route("/bangdiem" , methods=["get", "post"])
def bang_diem():
    lop = utils.get_class()
    monhoc = utils.load_mon_hoc()
    ky = utils.load_ky_hoc()

    hocsinh = utils.load_student(lop_id=request.args.get('lop_id'),
                                 kw=request.args.get('keyword'))

    err_msg = ""
    if request.method.__eq__('POST'):
        idmonhoc = request.form.get('monhoc')
        idkyhoc = request.form.get('kyhoc')
        idhocsinh = request.form.get('idhocsinh')
        diem151 = request.form.get('diem151', 0)
        diem152 = request.form.get('diem152', 0)
        diem153 = request.form.get('diem153', 0)
        diem154 = request.form.get('diem154', 0)
        diem155 = request.form.get('diem155', 0)
        diem601 = request.form.get('diem601', 0)
        diem602 = request.form.get('diem602', 0)
        diem603 = request.form.get('diem603', 0)
        diemck = request.form.get('diemck', 0)
        diemtb = request.form.get('diemtb', 0)

        try:
            utils.add_diem(idhs=idhocsinh,
                           idmh=idmonhoc,
                           idhk=idkyhoc,
                           diem151=diem151, diem152=diem152, diem153=diem153, diem154=diem154, diem155=diem155,
                           diem601=diem601, diem602=diem602, diem603=diem603,
                           diemck=diemck,
                           diemtb=diemtb)
            return redirect(url_for("bang_diem"))
        except Exception as ex:
            err_msg = 'Dang co loi ' + str(ex)

    return render_template('nhapdiem.html',
                           lop=lop,
                           hocsinh=hocsinh,
                           monhoc=monhoc,
                           kyhoc=ky)

@app.route("/xuatdiem")
def xuatdiem():

    xuatdiem = utils.xuat_diem(id_mon_hoc=request.args.get('mon_id'))

    monhoc = utils.load_mon_hoc()



    return render_template('xuatdiem.html',
                           xuatdiem=xuatdiem,
                           monhoc=monhoc,
                          )

if __name__ == '__main__':
    from edu.admin import *

    app.run(debug=True)