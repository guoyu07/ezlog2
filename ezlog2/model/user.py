# -*- coding: utf-8 *-*

import string,random
import hashlib
from datetime import datetime as dt

from flask import g,session,jsonify

from ezlog2.libs.db import db

class Validator(object):

    @classmethod
    def is_valid(cls,email,password):
        user = cls.objects(email=email,password=password).first()
        return user is not None

    @classmethod
    def validate_user(cls, email, password):
        return cls.objects(email=email,password=password).first()

class Admin(db.Document, Validator):
    email       = db.StringField(required = True)
    password    = db.StringField(required = True)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['email'], 'unique': True},
        ]
    }

class User(db.Document):
    email       = db.StringField(required = True)
    nickname    = db.StringField(required = True)
    avatar      = db.StringField()#probably change it
    password    = db.StringField(required = True)
    create_date = db.DateTimeField(default = dt.now)


    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['email'], 'unique': True},
            {'fields': ['nickname'], 'unique': True},
        ]
    }

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
    def is_email_exist(cls,email):
        user = cls.objects(email=email).first()
        return user is not None

    @classmethod
    def is_nickname_exist(cls,nickname):
        user = cls.objects(nickname=nickname).first()
        return user is not None

    @staticmethod
    def change_password(original_pw, changed_pw):
        pass

    def is_following(self, followeduserid):
        #print "the fo: ", type(followeduserid)
        if(followeduserid is None):
            return False
        result = Follow.objects(follower=self.id, followed_user=followeduserid).first()
        return result is not None

    def get_followers(self):
        pass
    
    def get_following_users(self):
        following_users = Follow.objects(follower=self)
        return following_users
        

    def read_message(self, notify_message_id):
        pass

    def get_unread_message(self):
        pass


class Follow(db.Document):
    follower             = db.ReferenceField(User)
    followed_user        = db.ReferenceField(User)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['follower', 'followed_user'], 'unique': True},
        ]
    }

    @classmethod
    def toggle_follow(cls,followerid, followeduserid):
        result = cls.objects(follower=followerid,followed_user=followeduserid).first()
        if result:
            result.delete()
        else:
            cls(follower=followerid,followed_user=followeduserid).save()
























