# -*- coding: utf-8 *-*

import string,random
import hashlib
import datetime

from flask import g,session,jsonify

from ezlog2.libs.db import db

class Admin(db.Document):
    email       = db.StringField(required = True)
    password    = db.StringField(required = True)

    @classmethod
    def is_valid(self):
        admin = cls.objects(email=email,password=password).first()
        return admin is not None

    @classmethod
    def validate_admin(cls, email, password):
        return cls.objects(email=email,password=password).first()

class User():
    self.email       = db.StringField(required = True)
    self.nickname    = db.StringField(required = True)
    self.avatar      = db.StringField()#probably change it
    self.password    = db.StringField(required = True)
    self.create_date = db.DateTimeField()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.objects(id=id).first()

    @classmethod
    def change_avatar_by_id(id,avatar):
        pass

    @staticmethod
    def get_user_startswith(word):
        pass

    @classmethod
    def is_valid(cls,email,password):
        user = cls.objects(email=email,password=password).first()
        return user is not None

    @classmethod
    def is_email_exist(cls,email):
        pass

    @classmethod
    def is_nickname_exist(cls,nickname):
        pass

    @staticmethod
    def change_password(original_pw, changed_pw):
        pass

    def is_following(self, followeduserid):
        #print "the fo: ", type(followeduserid)
        if(followeduserid is None):
            return False
        c = g.db.cursor()
        c.execute("SELECT * FROM follow WHERE followerid=:followerid AND followeduserid=:followeduserid",\
                                {'followerid':self.id,'followeduserid':followeduserid})
        result = c.fetchone()
        return result is not None


    def read_message(self, notify_message_id):
        pass

    def get_unread_message(self):
        pass


class Follow:
    def __init__(self):
        pass

    @staticmethod
    def toggle_follow(followerid, followeduserid):
        c = g.db.cursor()
        c.execute("SELECT * FROM follow WHERE followerid=:followerid AND followeduserid=:followeduserid",\
                                {'followerid':followerid,'followeduserid':followeduserid})
        result = c.fetchone()
        if result:
            c.execute("DELETE FROM follow WHERE followerid=:followerid AND followeduserid=:followeduserid",\
                                {'followerid':followerid,'followeduserid':followeduserid})
        else:
            c.execute("INSERT INTO follow(followerid,followeduserid ) VALUES (:followerid,:followeduserid)",\
                                {'followerid':followerid,'followeduserid':followeduserid})
        g.db.commit()
























