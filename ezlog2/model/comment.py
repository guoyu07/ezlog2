# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
from datetime import datetime as dt

from ezlog2.model import User
from ezlog2.libs.db import db

class Comment(db.Document):
    content        = db.StringField(required = True)
    tweet          = db.ReferenceField("Tweet")
    create_date    = db.DateTimeField(default = dt.now)

    commenter      = db.ReferenceField(User, dbref=True)



    @classmethod
    def get_comments_bytweetid(cls, tweetid, offset =0, limit = 20):
        comment_list = []
        start        = offset*limit
        end          = offset*limit+limit
        comment_list = cls.objects(tweet=tweetid)[start:end]

        return comment_list
