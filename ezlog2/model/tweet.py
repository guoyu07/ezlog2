# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
import datetime

from ezlog.model import User, Comment

class Tweet:
    def __init__(self, content, posterid):
        self.id = None
        self.content = content
        self.posterid = posterid
        self.type = 'text'
        self.originalid = 0
        self.retweet_comment = None
        self.create_date = None
        self.retweet_counter = 0
        self.comment_counter = 0

        self.poster = None
        self.original_tweet =None
        self.comments = []

    def init(self,result):
        self.id = result['id']
        self.content = result['content']
        self.posterid = result['posterid']
        self.type = result['type']
        self.originalid = result['originalid']
        self.retweet_comment = result['retweet_comment']
        self.create_date = result['create_date']
        self.retweet_counter = result['retweet_counter']
        self.comment_counter = result['comment_counter']

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



    @staticmethod
    def get_tweets_foruser(userid, limit = 20, offset = 0):
        c = g.db.cursor()
        c.execute('''
           SELECT * from tweet WHERE posterid IN
           (SELECT followeduserid from follow
           WHERE followerid=:id) or posterid=:id
           ORDER BY create_date DESC
           LIMIT :limit OFFSET :offset
           ''', {'id':userid, 'limit':limit, 'offset':offset * limit})
        results = c.fetchall()
        tweet_list = []
        for result in results:
            t = Tweet(None, None)
            t.init(result)
            t.poster = User.get_user_by_id(t.posterid)
            t.comments = Comment.get_comments_bytweetid(t.id)
            if(t.is_retweet()):
                t.original_tweet = Tweet.get_tweet_byid(t.originalid)
            tweet_list.append(t)
        return tweet_list

    @staticmethod
    def get_newest_tweets(limit = 20, offset =0):
        c = g.db.cursor()
        c.execute('''
           SELECT * from tweet
           ORDER BY create_date DESC
           LIMIT :limit OFFSET :offset
           ''', {'limit':limit, 'offset':offset * limit})
        results = filter(lambda x:x['content']!=None,c.fetchall())
        
        tweet_list = []
        for result in results:
            t = Tweet(None, None)
            t.init(result)
            t.poster = User.get_user_by_id(t.posterid)
            t.comments = Comment.get_comments_bytweetid(t.id)
            tweet_list.append(t)
        return tweet_list


    @staticmethod
    def get_tweet_byid(id):
        c = g.db.cursor()
        c.execute('''
           SELECT * from tweet
           WHERE id=:id
           ''', {'id':id})
        result = c.fetchone()
        t = Tweet(None, None)
        t.init(result)
        t.poster = User.get_user_by_id(t.posterid)
        t.comments = Comment.get_comments_bytweetid(t.id)
        return t

    def comment_on(self, commenter, content):
        pass

    def retweet(self):
        pass



