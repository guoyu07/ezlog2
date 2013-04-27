# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify
import re

from ezlog2.model import User,Tweet, Comment, Follow
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
    new_tweet = render_template('include/show_retweet.html', tweet = t)
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


@user_action.route('/logout')
def logout():
    session.pop('user')
    flash(u"登出成功!","info")
    return redirect('/')