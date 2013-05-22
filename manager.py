# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask.ext.script import Manager

from ezlog2 import app
from ezlog2.model.user import Admin
from ezlog2.util import sha224

manager = Manager(app)

@manager.option('-u', '--user', dest='username', default = 'admin')
@manager.option('-p', '--passwrod', dest='password', default= 'changeit')
def add_admin(username, password):
    '''add_admin -u username -p password'''
    if username is None or password is None:
        print "please add corrrect parameters\nadd_admin -u username -p password"
        return

    admin = Admin(email=username, password=sha224(password))
    admin.save()

@manager.command
def delete_admin(username):
    '''delete admin -u username'''
    Admin.delete_admin(username)

@manager.command
def show_admin():
    '''show admins'''
    print [x.email for x in Admin.objects.only('email')]


if __name__ == "__main__":
    manager.run()

