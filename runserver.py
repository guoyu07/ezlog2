# -*- coding: utf-8 -*-

from ezlog2 import app


if(__name__ == "__main__"):
    app.debug = app.config["DEBUG_MODE"]
    app.run()
