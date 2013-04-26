# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
from datetime import datetime as dt

from ezlog2.model import User, Comment
from ezlog2.libs.db import db

class Tweet(db.Document):
    content            = db.StringField(required = True)
    type               = db.StringField(default = "text")
    originalid         = db.StringField(default = "")
    retweet_comment    = db.StringField()
    create_date        = db.DateTimeField(default = dt.now)

    poster             = db.ReferenceField(User, dbref=True)

    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }
    
    def __ini__(self):
        self._comments = None

    def tweet(self):
        self.save()

    def retweetit(self, originalid):
        c = g.db.cursor()
        self.retweet_comment = self.content
        t = Tweet.get_tweet_byid(originalid)
        originalid = t.originalid or originalid
        self.create_date = datetime.datetime.now()
        c.execute("INSERT INTO tweet(content, posterid,originalid, retweet_comment) VALUES \
                (:content, :posterid,:originalid, :retweet_comment)",\
            {'content': t.content, 'posterid':self.posterid,
            'originalid':originalid, 'retweet_comment':self.retweet_comment})
        self.id = c.lastrowid
        self.poster = User.get_user_by_id(self.posterid)
        g.db.commit()

    def is_retweet(self):
        return self.originalid!=""

    @property
    def original_tweet(self):
        return Tweet(id=self.originalid).first()


    #TO-DO: it should be follower
    @classmethod
    def get_tweets_foruser(cls,user, limit = 20, offset = 0):
        start       = offset*limit
        end         = offset*limit+limit
        following_users = user.get_following_users()
        
        return cls.objects(poster__in=[x.id for x in following_users] + [user.id])\
                  .order_by("-create_date")[start:end]

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

    def retweet(self):
        pass
        
    @property
    def retweet_counter(self):
        return 0
    @property
    def comment_counter(self):
        return len(Comment.objects(tweet=self.id))
    @property
    def comments(self):
        self._comments = Comment.get_comments_bytweetid(self.id)
        return self._comments
        



