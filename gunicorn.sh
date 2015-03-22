#!/bin/bash

exec gunicorn -k gevent -w 2 -n mchacks-mentorship -b 127.0.0.1:6543 app:app
