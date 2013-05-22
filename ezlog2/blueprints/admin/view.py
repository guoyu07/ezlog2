# coding:utf-8
from flask import Blueprint, g
from flask.ext.admin import Admin, BaseView,AdminIndexView, expose
from flask.ext.admin.contrib.mongoengine import ModelView

def author_admin():
    return True

class AuthBase():
    def is_accessible(self):
        return False

class MyAdminView(AdminIndexView,AuthBase):
    @expose('/')
    def index(self):
        return self.render('/admin/index.html')

    def is_accessible(self):
        return author_admin()

class MyModelView(ModelView):
    pass

class UserModelView(ModelView):
    column_list = ('email', 'nickname','avatar', 'nickname','create_date', 'addr','birthday', 'gender','blog', 'slogan','university', 'theme',)
    column_filters = ['nickname', 'email']

    def is_accessible(self):
        return author_admin()



