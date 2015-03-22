#!/usr/bin/env python

from app import app, socketio

from gevent import monkey

monkey.patch_all()

if __name__ == "__main__":
    app.debug = True
    socketio.run(app, port=6542, host="0.0.0.0")
