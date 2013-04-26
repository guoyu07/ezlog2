# -*- coding: utf-8 *-*
import string,random
from flask import g,session,jsonify
import sqlite3
import hashlib
import datetime

class Admin:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def is_valid(self):
        c = g.db.cursor()
        c.execute("SELECT * FROM user WHERE email=:email AND password=:password",\
                                {'email':self.email,'password':self.password})
        tempuser = c.fetchone()
        if(not tempuser):
            return False
        return True

    def reset_password(self):
        c = g.db.cursor()
        c.execute("UPDATE user SET password=:password WHERE email=:email ",\
                                {'email':self.email,'password':self.password})
        g.db.commit()

class User:
    def __init__(self,email,nickname,password):
        self.id = None
        self.email = email
        self.nickname = nickname
        self.avatar = None
        self.password = not password or hashlib.sha224(password).hexdigest()
        self.create_date = None
        self.follower_counter = 0
        self.following_counter = 0
        self.tweet_counter = 0 #add later
        self.notify_message_counter = 0
        self.unreaded_counter = 0


    def init(self, result):
        self.nickname = result['nickname']
        self.create_date = result['create_date']
        self.follower_counter = result['follower_counter']
        self.following_counter = result['following_counter']
        self.tweet_counter = result['tweet_counter']
        self.notify_message_counter = result['notify_message_counter']
        self.unreaded_counter = result['unreaded_counter']
        self.id = result['id']

    @staticmethod
    def get_user_by_id(id):
        c = g.db.cursor()
        c.execute("SELECT * FROM user WHERE id=:id",\
                                {'id':id})
        result = c.fetchone()
        if(result is None):
            return None
        tempuser = User(result['email'],result['nickname'],None)
        tempuser.init(result)
        return tempuser


    @staticmethod
    def change_avatar_by_id(id,avatar):
        c = g.db.cursor()
        c.execute("UPDATE user SET avatar = :avatar WHERE id=:id",\
                                {'id':id,'avatar':avatar})
        g.db.commit()

    @staticmethod
    def get_user_startswith(word):
        c = g.db.cursor()
        c.execute("SELECT id,nickname FROM user \
                    WHERE nickname LIKE :word LIMIT 5",{'word':'%'+word+'%'})
        results = c.fetchall()
        lst = []
        for result in results:
            d = {}
            d['nickname'] = result['nickname']
            d['id'] = result['id']
            lst.append(d)
        return jsonify(users = lst)

    def update_email_nickname(self):
        c = g.db.cursor()
        c.execute("UPDATE user SET email=:email, nickname=:nickname WHERE id=:id",\
            {'email':self.email,'nickname':self.nickname,'id':self.id})
        g.db.commit()

    def is_valid(self):
        c = g.db.cursor()
        c.execute("SELECT * FROM user WHERE email=:email AND password=:password",\
                                {'email':self.email,'password':self.password})
        tempuser = c.fetchone()
        if(not tempuser):
            return False
        self.init(tempuser)
        return True

    @staticmethod
    def is_email_exist(email):
        c = g.db.cursor()
        c.execute("SELECT nickname FROM user WHERE email=:email",\
                                {'email':email})
        if(not c.fetchone()):
            return False
        return True

    @staticmethod
    def is_nickname_exist(nickname):
        c = g.db.cursor()
        c.execute("SELECT nickname FROM user WHERE nickname=:nickname",\
                                {'nickname':nickname})
        if(not c.fetchone()):
            return False
        return True

    def is_exist(self):
        c = g.db.cursor()
        c.execute("SELECT nickname FROM user WHERE email=:email or nickname=:nickname",\
                                {'email':self.email,'nickname':self.nickname})
        if(not c.fetchone()):
            return False
        return True

    def save(self):
        c = g.db.cursor()
        self.create_date = datetime.datetime.now()
        c.execute("INSERT INTO user(nickname,email,password,create_date) VALUES (?,?,?,?)",\
                                (self.nickname,self.email,self.password,self.create_date))
        self.id = c.lastrowid
        g.db.commit()

    @staticmethod
    def change_password(original_pw, changed_pw):
        c = g.db.cursor()
        userid = session['user'].id
        original_pw = hashlib.sha224(original_pw).hexdigest()
        changed_pw = hashlib.sha224(changed_pw).hexdigest()
        c.execute("SELECT 1 FROM user WHERE id=:userid AND password=:password",\
            {'userid':userid,'password':original_pw})
        if(c.fetchone() is None):
            return None
        c.execute("UPDATE user SET password=:password WHERE id=:userid",\
            {'userid':userid,'password':changed_pw})
        g.db.commit()
        return True

    @staticmethod
    def password_generate(size=8, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    @staticmethod
    def reset_password_for(email):
        c = g.db.cursor()
        c.execute("SELECT nickname FROM user WHERE email=:email",\
                                {'email':email})
        if(not c.fetchone()):
            return None
        password = User.password_generate()
        md5pw = hashlib.sha224(password).hexdigest()
        c.execute("UPDATE user SET password =:password WHERE email=:email",\
                                {'email':email,'password':md5pw})
        g.db.commit()
        return password
        
    def is_following(self, followeduserid):
        print "the fo: ", type(followeduserid)
        if(followeduserid is None):
            return False
        c = g.db.cursor()
        c.execute("SELECT * FROM follow WHERE followerid=:followerid AND followeduserid=:followeduserid",\
                                {'followerid':self.id,'followeduserid':followeduserid})
        result = c.fetchone()
        return result is not None


    def read_message(self, notify_message_id):
        pass

    def get_unread_message(self):
        pass


class Follow:
    def __init__(self):
        pass

    @staticmethod
    def toggle_follow(followerid, followeduserid):
        c = g.db.cursor()
        c.execute("SELECT * FROM follow WHERE followerid=:followerid AND followeduserid=:followeduserid",\
                                {'followerid':followerid,'followeduserid':followeduserid})
        result = c.fetchone()
        if result:
            c.execute("DELETE FROM follow WHERE followerid=:followerid AND followeduserid=:followeduserid",\
                                {'followerid':followerid,'followeduserid':followeduserid})
        else:
            c.execute("INSERT INTO follow(followerid,followeduserid ) VALUES (:followerid,:followeduserid)",\
                                {'followerid':followerid,'followeduserid':followeduserid})
        g.db.commit()
    























