# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify,render_template
import sqlite3
import hashlib
from datetime import datetime as dt

from ezlog2.model import User, Comment
from ezlog2.libs.db import db
from ezlog2.util import find_all_at_users,notify_user

class Tweet(db.Document):
    content            = db.StringField(required = True)
    type               = db.StringField(default = "text")
    originalid         = db.StringField(default = "")
    retweetid          = db.StringField(default = "")
    retweet_comment    = db.StringField()
    create_date        = db.DateTimeField(default = dt.now)
    extra_pic          = db.StringField(default = "")

    poster             = db.ReferenceField(User, dbref=True)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }

    def __ini__(self):
        self._comments = None

    def tweet(self):
        from message import NotifyMessage
        nicknames   = find_all_at_users(self.content)
        self.save()
        for nickname in nicknames:
            receiver = User.get_user_by_nickname(nickname)
            NotifyMessage.add(self.notify_render(),self.poster,receiver)

    def notify_render(self):
        return render_template("include/tweet_notify.html",sender=self.poster,tweet=self)

    @classmethod
    def retweetit(cls, originalid, comment, poster):
        t   = cls.get_tweet_byid(originalid)
        ret = cls(content       = t.content,
                originalid      = t.originalid or originalid,
                retweetid       = originalid,
                retweet_comment = comment,
                poster          = poster).save()
        return ret

    def is_retweet(self):
        return self.originalid!=""

    @property
    def original_tweet(self):
        if not self.originalid:
            return None
        return Tweet.objects(id=self.originalid).first()

    @property
    def retweet_tweet(self):
        return Tweet.objects(id=self.retweetid).first()

    @classmethod
    def get_tweets_foruser(cls,user, limit=15, offset=0):
        start           = offset*limit
        end             = offset*limit+limit
        following_users = user.get_following_users()
        tweets = cls.objects(poster__in=[x.id for x in following_users]+[user.id])\
                  .order_by("-create_date")[start:end]
        return tweets

    @classmethod
    def get_users_tweets(cls, user, limit=15, offset=0):
        start       = offset*limit
        end         = offset*limit+limit
        tweets      = cls.objects(poster=user)\
                        .order_by("-create_date")[start:end]
        return tweets


    @classmethod
    def get_newest_tweets(cls,limit = 20, offset =0):
        start       = offset*limit
        end         = offset*limit+limit
        return cls.objects().order_by("-create_date")[start:end]


    @classmethod
    def get_tweet_byid(cls, id):
        tweet = cls.objects(id=id).first()
        return tweet

    def comment_on(self, commenter, content):
        pass


    @property
    def retweet_counter(self):
        return len(Tweet.objects(retweetid=str(self.id)))
    @property
    def comment_counter(self):
        return len(Comment.objects(tweet=self.id))
    @property
    def comments(self):
        self._comments = Comment.get_comments_bytweetid(self.id)
        return self._comments




