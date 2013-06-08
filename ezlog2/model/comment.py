# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
from datetime import datetime as dt

from flask import render_template

from ezlog2.model import User
from ezlog2.libs.db import db
from ezlog2.util import find_all_at_users

class Comment(db.Document):
    content        = db.StringField(required = True)
    tweet          = db.ReferenceField("Tweet")
    create_date    = db.DateTimeField(default = dt.now)

    commenter      = db.ReferenceField(User, dbref=True)

    @classmethod
    def add(cls,content,tweet,commenter):
        c = Comment(content=content, tweet=tweet, commenter=commenter)
        c.save()
        from message import NotifyMessage
        nicknames   = find_all_at_users(c.content)
        for nickname in nicknames:
            receiver = User.get_user_by_nickname(nickname)
            NotifyMessage.add(c.notify_render(),c.commenter,receiver)
        return c

    def notify_render(self):
        return render_template("include/comment_notify.html",
                                sender=self.commenter,
                                tweet=self.tweet)

    @classmethod
    def get_comments_bytweetid(cls, tweetid, offset =0, limit = 20):
        comment_list = []
        start        = offset*limit
        end          = offset*limit+limit
        comment_list = cls.objects(tweet=tweetid).order_by('-create_date')[start:end]

        return comment_list
