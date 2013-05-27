# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify,send_file

from ezlog2 import app
from ezlog2.model import User, Tweet, Comment
from ezlog2.util import sha224
from ezlog2.libs.pic import Picture,MongOperator




@app.route("/picture/<string:id>",methods=["GET"])
def get_picture(id):
    picture = MongOperator.get_pictue_by_id(id)
    return send_file(picture, mimetype='image/jpeg')

@app.route("/picture/action/save", methods=["POST"])
def save_picture():
    file = request.files.get("file", None)
    if file is None:
        return jsonify(rcode=404, msg="file required")

    pic  = Picture(file,operator=MongOperator)
    pic.save()
    return jsonify(url=pic.get_url(),rcode=200)







