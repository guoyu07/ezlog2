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

    @classmethod
    def delete_admin(cls,email):
        cls.objects(email=email).first().delete()

    def to_dict(self):
        return {"id":str(self.id),
                "nickname":self.email
        }

class User(db.Document, Validator):
    email       = db.StringField(required = True)
    nickname    = db.StringField(required = True)
    avatar      = db.StringField()#probably change it
    password    = db.StringField(required = True)
    create_date = db.DateTimeField(default = dt.now)

    #here is extra info which is not required, user can setting it later
    addr        = db.StringField()
    birthday    = db.StringField()
    gender      = db.StringField()
    blog        = db.StringField()
    slogan      = db.StringField()
    university  = db.StringField()

    #page setting
    #layout      = db.StringField(default="right")
    theme       = db.StringField(default="default")



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
        if id is None:
            return None
        return cls.objects(id=id).first()

    @classmethod
    def change_avatar_by_id(id,avatar):
        pass

    @classmethod
    def get_user_by_nickname(cls,nickname):
        return cls.objects(nickname=nickname).first()

    @classmethod
    def get_users_startwith(cls,word, limit=5):
        return cls.objects(nickname__istartswith=word)[:limit]

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
        follower_users = [x.follower for x in Follow.objects(followed_user=self)]
        return following_users

    def get_following_users(self):
        following_users = [x.followed_user for x in Follow.objects(follower=self)]
        return following_users

    #check whether this user can send private message to others
    def can_send_pm_to_user(self, userid):
        pass


    #private message
    def read_message(self, notify_message_id):
        pass

    #private message
    def get_unread_message(self):
        pass

    def get_notify_messages(self):
        from message import NotifyMessage
        return NotifyMessage.get_notify_message_for_user(self)
    @property
    def notify_counter(self):
        from message import NotifyMessage
        return NotifyMessage.get_user_notify_counter(self)

    @property
    def private_counter(self):
        #TO-DO
        return 0
    @property
    def following_counter(self):
        return len(Follow.objects(follower=self))

    @property
    def follower_counter(self):
        return len(Follow.objects(followed_user=self))

    @property
    def tweet_counter(self):
        from tweet import Tweet
        return len(Tweet.objects(poster=self))



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

    @classmethod
    def get_followers_by_user(cls,user):
        return [x.follower for x in cls.objects(followed_user=user).only("follower")]


    @classmethod
    def get_followed_users_by_user(cls,user):
        return [x.followed_user for x in cls.objects(follower=user).only("followed_user")]




















