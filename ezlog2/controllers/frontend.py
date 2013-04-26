# -*- coding: utf-8 -*-

from flask import render_template

from ezlog2 import app

@app.route('/')
def main():
    return render_template("main.html")