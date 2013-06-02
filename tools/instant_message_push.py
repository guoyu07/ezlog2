# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from redis import Redis
from flask import request,Response, stream_with_context,session
import gevent

from ezlog2 import app

redis = Redis()

@app.route("/notify_user/<userid>")
def stream(userid):
    def generate():
        pubsub = redis.pubsub()
        pubsub.subscribe("notify-%s"%userid)
        for event in pubsub.listen():
            gevent.sleep(0.5)
            if event["type"] == "message":
                yield "data: %s\r\n\r\n" % event["data"]
    return Response(stream_with_context(generate()),
                    direct_passthrough=True,
                    mimetype="text/event-stream")

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from gevent import monkey; monkey.patch_all()
    
    # app.debug = True
    # app.run(port=5005,threaded=True)
    http_server = WSGIServer(('127.0.0.1', 5005), app)
    http_server.serve_forever()

