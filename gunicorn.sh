#!/bin/bash

exec gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker \
    -n mchacks-mentorship -b 127.0.0.1:6543 app:app
