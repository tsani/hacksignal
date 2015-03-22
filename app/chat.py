from app import app, socketio

from flask.ext.socketio import emit

@socketio.on('my event', namespace='/chat')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')
