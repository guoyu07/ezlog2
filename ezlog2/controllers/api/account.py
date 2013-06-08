# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify

from ezlog2 import app
from ezlog2.model import User, Tweet, Comment
from ezlog2.util import sha224

@app.route("/api/account/username", methods=["GET","POST"])
def username_startwith():
    startname       = request.values.get("startwith", "")
    users           = User.get_users_startwith(startname)
    return jsonify(users=[{'nickname':x.nickname, 
                           'id':str(x.id), 
                           'avatar':x.avatar} for x in users])