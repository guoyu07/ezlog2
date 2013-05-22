# coding:utf-8
from flask import Blueprint, g,session,redirect,url_for,flash
from flask.ext.admin import Admin, BaseView,AdminIndexView, expose
from flask.ext.admin.contrib.mongoengine import ModelView

def author_admin():
    return "admin" in session

class AuthBase():
    def is_accessible(self):
        return False

class MyAdminView(AdminIndexView,AuthBase):
    @expose('/')
    def index(self):
        return self.render('/admin/index.html')

    @expose('/logout')
    def logout(self):
        if author_admin():
            session.pop("admin")
            flash(u"管理员登出成功")
        return redirect(url_for('main'))
        
    def is_accessible(self):
        return True

class MyModelView(ModelView):
    can_delete = False

    def is_accessible(self):
        return author_admin()

class UserModelView(MyModelView):
    column_list = ('email', 'nickname','avatar', 'nickname',
                   'create_date', 'addr','birthday', 'gender',
                   'blog', 'slogan','university', 'theme',)
    column_filters = ['nickname', 'email']





