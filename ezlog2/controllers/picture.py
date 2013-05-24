# -*- coding: utf-8 *-*
from flask import Module, url_for, \
    redirect, g, flash, request, current_app,\
    render_template, session,jsonify

from ezlog2 import app
from ezlog2.model import User, Tweet, Comment
from ezlog2.util import sha224





@app.route("/picture/<string:id>")
def get_picture(id):
    pass
    
@app.route("/picture/action/save")
def save_picture():
    pass



    
    
    
    
    
    
    
    
    