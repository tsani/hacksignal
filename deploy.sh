#!/bin/bash

# Deployment script for HackSignal. #
#####################################

# This script will do everything necessary to deploy HackSignal *except things
# relating to the database*. The rationale for this is that databases are
# tricky, and doing this from a script may be unsafe.

set -e

if test -z "$1"
then
    echo "no pidfile path given"
    exit 1
fi

# Create the Python virtualenv if it does not exist.
if ! test -e venv
then
    virtualenv --python=/usr/bin/python2.7 venv
fi

# Enter the virtualenv
source venv/bin/activate || eval 'echo "failed to enter virtualenv" ; exit 1'

# Install/update any dependencies
pip install -r requirements.txt

# This port number needs to match up with the systemd socket file
exec gunicorn -k gevent -n hacksignal -b 127.0.0.1:6543 --pid "$1" app:app
