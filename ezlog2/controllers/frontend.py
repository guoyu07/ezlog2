# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify

from ezlog2 import app
from ezlog2.model import User, Tweet, Comment
from ezlog2.util import sha224


@app.context_processor
def inject_user():
    user = session.get('user',None)
    return dict(user = user)

@app.route("/")
def main():
    if('user' not in session):
        return redirect(url_for('login'))
    tweets = Tweet.get_tweets_foruser(session['user'].id)
    return render_template('main.html', tweets = tweets)

@app.route("/newest")
def newest():
    tweets = Tweet.get_newest_tweets()
    return render_template('newest.html', tweets = tweets)

@app.route("/login", methods = ['GET' ,'POST'])
def login():
    if(request.method == "GET"):
        return render_template('login.html')
    email = request.form.get('email',"")
    password = sha224(request.get('password',""))
    if(User.is_valid(email, password)):
        session['user'] = user
        flash(u'登入成功','info')
        return redirect(url_for('main'))
    else:
        flash(u'登入失败, 请重试','error')
        return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    if(request.method == 'GET'):
        return render_template('register.html')

    error = False

    email = request.form.get('email',None) or None
    if email is None:
        flash(u'请输入Email地址','error')
        error = True
    if(User.is_email_exist(email)):
        flash(u'该Email已经注册','error')
        error = True

    nickname = request.form.get('nickname',None) or None
    if nickname is None:
        flash(u'请输入你的昵称','error')
        error = True
    if(User.is_nickname_exist(nickname)):
        flash(u'该昵称已经注册','error')
        error = True

    password = request.form.get('password',None) or None
    if password is None:
        flash(u'请输入你的密码','error')
        error = True

    if(error):
        return redirect(url_for('register'))
    user = User(email=email,nickname=nickname, password=password)
    user.save()
    flash(u'注册成功','info')
    session['user'] = user
    return redirect(url_for('main'))













