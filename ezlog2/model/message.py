# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
from datetime import datetime as dt

from ezlog2.model import User
from ezlog2.libs.db import db


class NotifyMessage(db.Document):
    sender             = db.ReferenceField(User)
    receiver           = db.ReferenceField(User)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }


#only two person followed each other, they can send private message
class PrivateMessage(db.Document):
    content            = db.StringField(required = True)
    sender             = db.ReferenceField(User)
    receiver           = db.ReferenceField(User)
    create_date        = db.DateTimeField(default = dt.now)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }

    @classmethod
    def add(cls,content,sender,receiver)
        pass

    @classmethod
    def get_private_message_for_user(cls,user):
        pass








