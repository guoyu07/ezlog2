# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
import datetime

from ezlog2.model import User

class Comment:
    def __init__(self,content,tweetid, userid):
        self.id = None
        self.content = content
        self.userid = userid
        self.tweetid =tweetid
        self.create_date =None

        self.commenter = None

    def save(self):
        c = g.db.cursor()
        self.create_date = datetime.datetime.now()
        c.execute("INSERT INTO comment(content,tweetid,userid, create_date) VALUES (?,?,?,?)",\
                                (self.content,self.tweetid,self.userid,self.create_date))
        self.id = c.lastrowid
        g.db.commit()

    @staticmethod
    def get_comments_bytweetid(tweetid, offset =0, limit = 20):
        c = g.db.cursor()
        c.execute('''
        SELECT * FROM comment WHERE tweetid=:tweetid
        ORDER BY create_date ASC LIMIT :limit OFFSET :offset
        ''',\
        {'tweetid':tweetid,'limit':limit,'offset':limit*offset})
        results = c.fetchall()
        if(results is None):
            return None
        comment_list = []
        for result in results:
            tempcomment = Comment(result['content'], tweetid, None)
            tempcomment.create_date = result['create_date']
            tempuser = User.get_user_by_id(result['userid'])
            tempcomment.commenter = tempuser

            comment_list.append(tempcomment)

        return comment_list
