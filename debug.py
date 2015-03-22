#!/usr/bin/env python

from app import app

if __name__ == "__main__":
    socketio.run(port=6542, host="0.0.0.0")
