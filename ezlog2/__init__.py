﻿# -*- coding: utf-8 -*-

import os

import flask as f
from flask import Flask
#import flask.ext.assets as fassets

import config.conf as conf
from util import readable_time

app = Flask(__name__)

app.config.from_object("ezlog2.config.conf")

#assets = fassets.Environment(app)
#assets.versions = 'hash:32'

@app.before_request
def something_before_request():
    pass

import controllers
app.register_module(controllers.useraction.user_action, url_prefix="/useraction")
app.jinja_env.filters['timesince'] = readable_time