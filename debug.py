#!/usr/bin/env python

from app import app

from flask.ext.socketio import SocketIO

socketio = SocketIO(app)

if __name__ == "__main__":
    app.debug = True
    socketio.run(app, port=6542, host="0.0.0.0")
