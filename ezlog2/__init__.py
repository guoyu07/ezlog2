# -*- coding: utf-8 -*-

import os

import flask as f
from flask import Flask
from flask.ext.admin import Admin
#import flask.ext.assets as fassets

import config.conf as conf
from util import readable_time,linkify,clean

app = Flask(__name__)

app.config.from_object("ezlog2.config.conf")
from ezlog2.blueprints.admin import admin
admin.init_app(app)
admin.base_template='admin/my_master.html'
#assets = fassets.Environment(app)
#assets.versions = 'hash:32'

@app.before_request
def something_before_request():
    pass

import controllers
import blueprints
app.register_module(controllers.useraction.user_action, url_prefix="/useraction")
app.jinja_env.filters['timesince']  = readable_time
app.jinja_env.filters['linkify']    = linkify
app.jinja_env.filters['clean']      = clean