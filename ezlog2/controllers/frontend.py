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
        return redirect(url_for('newest'))
    page    = request.args.get("page", 1, type=int)
    tweets  = Tweet.get_tweets_foruser(session['user'],offset=page-1,limit=15)
    return render_template('main.html',
                            tweets = tweets,
                            more_url = url_for("main",page=page+1))


@app.route("/tweet/<string:tweetid>",methods=['GET'])
def show_single_tweet(tweetid):
    tweet      = Tweet.get_tweet_byid(tweetid)
    tweet.open = True
    is_retweet = request.args.get("retweet",None)
    return render_template("single_tweet.html",
                            tweet=tweet,
                            is_retweet=is_retweet,
                            )

@app.route("/newest")
def newest():

    page    = request.args.get("page", 1, type=int)
    tweets  = Tweet.get_newest_tweets(offset=page-1,limit=15)
    return render_template('newest.html',
                            tweets = tweets,
                            more_url = url_for("newest",page=page+1))

@app.route("/user/nickname/<string:nickname>",methods=["GET"])
def show_user_by_nickname(nickname):
    userid      = User.get_user_by_nickname(nickname).id
    return redirect(url_for("personal_center",userid=userid))

@app.route("/login", methods = ['GET' ,'POST'])
def login():
    if(request.method == "GET"):
        return render_template('login.html')
    email = request.form.get('email',"")
    password = sha224(request.form.get('password',""))
    user     = User.validate_user(email, password)
    if(user is not None):
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
    user = User(email=email,nickname=nickname, password=sha224(password))
    user.save()
    flash(u'注册成功','info')
    session['user'] = user
    return redirect(url_for('main'))


@app.route("/_admin", methods = ['POST'])
def admin_login():
    from ezlog2.model.user import Admin
    email       = request.form.get("username",None)
    password    = request.form.get("password",None)
    admin       = Admin.validate_user(email,sha224(password))
    if admin is None:
        flash(u'Login failed','error')
        return redirect(url_for('admin.index'))

    session['admin'] = admin.to_dict()
    flash(u'login successfully','info')
    return redirect(url_for('admin.index'))










