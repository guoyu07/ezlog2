# -*- coding: utf-8 -*-

import os
import logging

from fabric.api import local

_warn = logging.warn
CURRENT_PATH = os.path.join(os.getcwd(),os.path.dirname(__file__))

def cleaning():
    'write the python script to delete unnecesary files'
    pass

def update_req():
    """Updating requirements for pip"""
    # check whether in virtualenv
    if not os.environ.get("VIRTUAL_ENV"):
        _warn("You are not in an Virtualenv, please activate it first")
        return
    local("pip freeze > %s/pip_requirements.txt" % CURRENT_PATH)

def test():
    """Run nose test"""
    local("nosetests --nocapture")