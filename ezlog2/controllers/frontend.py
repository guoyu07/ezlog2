# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify

from ezlog2 import app
from ezlog2.model import User, Tweet, Comment



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
    email = request.form['email']
    password = request.form['password']
    user = User(email,None,password)
    if(user.is_valid()):
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
    email = request.form['email']
    if(User.is_email_exist(email)):
        flash(u'该Email已经注册','error')
        error = True
    nickname = request.form['nickname']
    if(User.is_nickname_exist(nickname)):
        flash(u'该昵称已经注册','error')
        error = True
    password = request.form['password']
    if(error):
        return redirect(url_for('register'))
    user = User(email, nickname, password)
    user.save()
    flash(u'注册成功','info')
    session['user'] = user
    return redirect(url_for('main'))













