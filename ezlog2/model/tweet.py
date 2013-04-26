# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
import datetime

from ezlog2.model import User, Comment
from ezlog2.libs.db import db

class Tweet(db.Document):
    content            = db.StringField(required = True)
    type               = db.StringField(default = "text")
    original_id        = db.StringField(default = "")
    retweet_comment    = db.StringField()
    create_date        = db.DateTimeField()

    poster             = db.ReferenceField(User, dbref=True)
    #self.original_tweet =None
    
    meta = {
        'allow_inheritance': False,
        'index_types': False,
    }

    def tweet(self):
        c = g.db.cursor()
        self.create_date = datetime.datetime.now()
        c.execute("INSERT INTO tweet(content, posterid) VALUES \
         (:content, :posterid)",\
            {'content': self.content, 'posterid':self.posterid})
        self.id = c.lastrowid
        self.poster = User.get_user_by_id(self.posterid)
        g.db.commit()

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
        return self.originalid !=0



    #TO-DO: it should be follower
    @classmethod
    def get_tweets_foruser(cls,userid, limit = 20, offset = 0):
        start       = offset*limit
        end         = offset*limit+limit
        user        = User.get_user_by_id(userid)
        return cls.objects(poster=user).order_by("-create_date")[start:end]

    @classmethod
    def get_newest_tweets(cls,limit = 20, offset =0):
        start       = offset*limit
        end         = offset*limit+limit
        return cls.objects().order_by("-create_date")[start:end]


    @staticmethod
    def get_tweet_byid(id):
        tweet = cls.objects(id=id).first()
        return tweet

    def comment_on(self, commenter, content):
        pass

    def retweet(self):
        pass



