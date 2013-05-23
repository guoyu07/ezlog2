# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
from datetime import datetime as dt

from ezlog2.model import User
from ezlog2.libs.db import db


class NotifyMessage(db.Document):
    content            = db.StringField(required = True)
    sender             = db.ReferenceField(User)
    receiver           = db.ReferenceField(User)
    create_date        = db.DateTimeField(default=dt.now)
    has_read           = db.BooleanField(default=False)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }

    @classmethod
    def add(cls,content,sender,receiver):
        nm      = cls(content=content,sender=sender,receiver=receiver).save()
        return nm

    @classmethod
    def get_notify_message_by_id(cls,id):
        if id is None:
            return None
        return cls.objects(id=id).first()

    @classmethod
    def get_user_notify_counter(cls,user):
        return len(cls.objects(receiver=user,has_read=False))

    @classmethod
    def get_notify_message_for_user(cls,user):
        return cls.objects(receiver=user,has_read=False)
    
    def read(self,user):
        if user != self.receiver:
            return False
        self.has_read = True
        self.save()
        return True


#only two person followed each other, they can send private message
class PrivateMessage(db.Document):
    content            = db.StringField(required = True)
    sender             = db.ReferenceField(User)
    receiver           = db.ReferenceField(User)
    create_date        = db.DateTimeField(default=dt.now)
    has_read           = db.BooleanField(default=False)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }

    @classmethod
    def add(cls,content,sender,receiver):
        pass

    @classmethod
    def get_private_message_for_user(cls,user):
        pass










