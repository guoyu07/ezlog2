# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from redis import Redis
from flask import request,Response, stream_with_context,session

from ezlog2 import app

redis = Redis()
@app.route("/streams/interesting")
def stream():
    # print "Connect"
    # user = session.get("user",None)
    # print "user",user
    # print "session",session
    print "request.cookies",request.cookies
    # if user is None:
        # return "None"
    def generate():
        pubsub = redis.pubsub()
        pubsub.subscribe("interesting-channel")
        for event in pubsub.listen():
            if event["type"] == "message":
                yield "data: %srnrn % event[data]"
    return Response(stream_with_context(generate()),
                    direct_passthrough=True,
                    mimetype="text/event-stream")

if __name__ == '__main__':
    app.debug = True
    app.run(port=5005,threaded=True)