from app import app

from flask.ext.socketio import emit

@app.socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@app.socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@app.socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
