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


class ModelView(ModelView):
    column_filters = ['nickname', 'email']
    def is_accessible(self):
        return author_admin()



