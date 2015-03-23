from app import app, socketio

from flask import session

from flask.ext.socketio import emit

@socketio.on('my event', namespace='/chat')
def test_message(message):
    if 'username' not in session:
        emit('server message', {
            'data': 'Not logged in!'
        })
    else:
        emit('chat message', {
            'data': message['data']
        })

@socketio.on('auth', namespace='/chat')
def socket_auth(req):
    session['username'] = req['username']
    emit('server message', {
        'data': 'Logged in as: ' + session['username']
    })

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('chat message', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')
