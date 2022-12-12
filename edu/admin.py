from edu import app
from flask_admin import Admin, BaseView, expose, AdminIndexView
from edu.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect
import utils
from flask import request





class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):

        monhoc = utils.load_mon_hoc()
        hocky = utils.load_ky_hoc()

        return self.render('admin/stats.html', stats=utils.ket_qua(id_mon=request.args.get('id_mon'),
                                                                   id_hoc_ky=request.args.get('id_hoc_ky')),
                                                monhoc=monhoc,
                                                hocky=hocky,
                                                thongke=utils.thong_ke(id_mon=request.args.get('id_mon'),
                                                                       id_hoc_ky=request.args.get('id_hoc_ky')))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.lop_hoc_stats())

admin = Admin(app=app,
              name="Education Administration",
              template_mode="bootstrap4",
              index_view=MyAdminIndex())
admin.add_view(AuthenticatedModelView(Lop,db.session))
admin.add_view(AuthenticatedModelView(HocSinh,db.session))
admin.add_view(AuthenticatedModelView(QuyDinh,db.session))
admin.add_view(AuthenticatedModelView(MonHoc,db.session))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Logout'))