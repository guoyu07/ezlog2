# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify
import re

from ezlog2.model import User,Tweet, Comment, Follow
from ezlog2.util import random_int,sha224
user_action = Module(__name__)


@user_action.before_request
def require_login():
    if 'user' not in session:
        if request.method == 'PUT':
            return jsonify(result ='login')
        flash(u"你需要先登入!","error")
        return redirect('/login')



@user_action.context_processor
def inject_user():
    user = session['user']
    return dict(user = user)

@user_action.route('/tweet', methods=['POST'])
def tweet():
    content = request.form['content']
    posterid = session['user'].id
    t = Tweet(content=content,poster=session['user'])
    t.tweet()
    new_tweet = render_template('include/show_tweet.html', tweet = t)
    return jsonify(result="done", newtweet = new_tweet)

@user_action.route('/retweet', methods=['POST'])
def retweet():
    comment         = request.form['comment']
    originalid      = request.form['originalid']
    poster          = session['user']
    t               = Tweet.retweetit(originalid,comment,poster)
    new_tweet = render_template('include/show_tweet.html', tweet = t, floor=random_int())
    return jsonify(result="done", newtweet = new_tweet)

@user_action.route('/comment', methods=['POST'])
def comment():
    tweetid = request.form['tweetid']
    content = request.form['content']
    c = Comment(content=content, tweet=Tweet.get_tweet_byid(tweetid), commenter=session['user'])
    c.save()
    new_comment = render_template('include/show_comment.html', comment = c)
    return jsonify(result="done", newcomment = new_comment)

@user_action.route('/toggle_follow', methods=['POST'])
def toggle_follow():
    followeduserid = request.form['followeduserid']
    Follow.toggle_follow(session['user'], User.get_user_by_id(followeduserid))
    return jsonify(result="done")


@user_action.route('/setting', methods=["GET"])
def setting_view():
    return render_template("setting.html")


@user_action.route('/basic_setting', methods=["POST"])
def basic_setting():
    original_password       = request.form.get("original_password", "")
    user = session['user']
    error = False
    if user.password != sha224(original_password):
        flash(u"用户ID与密码不匹配",'error')
        return redirect(url_for("setting_view"))

    email = request.form.get("email", None) or None
    if email is None:
        flash(u'请输入Email地址','error')
        error = True
    if(user.email!=email and User.is_email_exist(email)):
        flash(u'该Email已经注册','error')
        error = True

    nickname = request.form.get('nickname',None) or None
    if nickname is None:
        flash(u'请输入你的昵称','error')
        error = True
    if(user.nickname!=nickname and User.is_nickname_exist(nickname)):
        flash(u'该昵称已经注册','error')
        error = True

    if error:
        return redirect(url_for("setting_view"))

    new_pwd         = request.form.get("new_password")
    user.email      = email
    user.nickname   = nickname
    if new_pwd:
        user.password   = sha224(new_pwd)
    user.save()
    flash(u"修改成功",'info')
    session['user'] = user
    return redirect(url_for("setting_view"))

@user_action.route('/user_info_setting', methods=["POST"])
def user_info_setting():
    addr            = request.form.get("addr", "")
    birthday        = request.form.get("birthday", "")
    gender          = request.form.get("gender", "")
    blog            = request.form.get("blog", "")
    slogan          = request.form.get("slogan", "")
    university      = request.form.get("university", "")

    user            = session['user']

    user.addr       = addr
    user.birthday   = birthday
    user.gender     = gender
    user.blog       = blog
    user.slogan     = slogan
    user.university = university

    user.save()
    flash(u"修改成功",'info')
    session['user'] = user
    return redirect(url_for("setting_view"))

@user_action.route('/page_setting', methods=["POST"])
def page_setting():
    user            = session['user']
    user.theme      = request.form.get("theme", user.theme)

    user.save()
    flash(u"修改成功",'info')
    return redirect(url_for("setting_view"))

@user_action.route('/logout')
def logout():
    session.pop('user')
    flash(u"登出成功!","info")
    return redirect('/')















