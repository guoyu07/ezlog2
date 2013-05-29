# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify
import re

from ezlog2 import app
from ezlog2.model import User,Tweet, Comment, Follow
from ezlog2.model.message import NotifyMessage,PrivateMessage
from ezlog2.util import random_int,sha224,clean
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
    user = session.get('user',None)
    return dict(user = user)

@user_action.route('/tweet', methods=['POST'])
def tweet():
    content = request.form['content']
    content = clean(content)
    posterid = session['user'].id
    t = Tweet(content=content,poster=session['user'])
    t.tweet()
    new_tweet = render_template('include/show_tweet.html', tweet = t)
    return jsonify(result="done", newtweet = new_tweet)

@user_action.route('/retweet', methods=['POST'])
def retweet():
    comment         = request.form['comment']
    comment         = clean(comment)
    originalid      = request.form['originalid']
    poster          = session['user']
    t               = Tweet.retweetit(originalid,comment,poster)
    new_tweet = render_template('include/show_tweet.html', tweet = t, floor=random_int())
    return jsonify(result="done", newtweet = new_tweet)

@user_action.route('/comment', methods=['POST'])
def comment():
    tweetid = request.form['tweetid']
    content = request.form['content']
    content = clean(content)
    c = Comment.add(content, Tweet.get_tweet_byid(tweetid), session['user'])
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


@user_action.route("/personal_center",methods=["GET"])
@app.route("/personal_center/<string:userid>",methods=["GET"])
def personal_center(userid=None):
    theuser = None
    if userid is None:
        theuser = session['user']
    else:
        theuser = User.get_user_by_id(userid)

    page        = request.args.get("page", 1, type=int)
    tweets      = Tweet.get_users_tweets(theuser,offset=page-1,limit=15)

    return render_template("personal_center.html",
                            theuser=theuser,
                            tweets=tweets,
                            more_url = url_for("personal_center",page=page+1,userid=userid)
                            )

@user_action.route("/followers", methods=["GET"])
def show_user_followers():
    userid          = request.args.get("userid",None)
    user            = User.get_user_by_id(userid)
    followers       = Follow.get_followers_by_user(user)

    return render_template("show_followers.html",
                           followers=followers,
                           theuser=user)

@user_action.route("/followed_users", methods=["GET"])
def show_user_followed_users():
    userid          = request.args.get("userid",None)
    user            = User.get_user_by_id(userid)
    followed_users  = Follow.get_followed_users_by_user(user)

    return render_template("show_followed_users.html",
                           followed_users=followed_users,
                           theuser=user)


@user_action.route("/message_center",methods=["GET"])
def message_center():
    return render_template("message_center.html")


@user_action.route("/private_message", methods=["POST"])
def private_message_sender():
    receiverid          = request.form.get("receiverid", None)
    content             = request.form.get("content",None)
    result              = session["user"].send_private_message(receiverid,content)
    if result is None:
        return jsonify(rcode=404)
    return jsonify(rcode=200)
    
@user_action.route("/read_private_message",methods=["POST"])
def read_private_message():
    pmid        = request.form.get("pmid",None)
    pm          = PrivateMessage.get_private_message_by_id(pmid)
    if pm is None:
        return jsonify(rcode=404)
    result = pm.read(session['user'])
    if not result:
        return jsonify(rcode=404)
    return jsonify(rcode=200)

@user_action.route("/delete_private_message",methods=["POST"])
def delete_private_message():
    pmid        = request.form.get("pmid",None)
    pm          = PrivateMessage.get_private_message_by_id(pmid)
    if pm is None:
        return jsonify(rcode=404)
    pm.delete()
    return jsonify(rcode=200)

@user_action.route("/read_notify_message",methods=["POST"])
def read_notify_message():
    messageid   = request.form.get("messageid",None)
    nm          = NotifyMessage.get_notify_message_by_id(messageid)
    if nm is None:
        return jsonify(rcode=404)
    result = nm.read(session['user'])
    if not result:
        return jsonify(rcode=404)
    return jsonify(rcode=200)

@user_action.route('/logout')
def logout():
    session.pop('user')
    flash(u"登出成功!","info")
    return redirect('/')
