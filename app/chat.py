from app import app, socketio

from flask import session

from flask.ext.socketio import emit, join_room

@socketio.on('chat message', namespace='/chat')
def test_message(message):
    emit('chat message', {
        'sender': message['sender'],
        'data': message['data']
    }, room='__admin__')

    emit('chat message', {
        'sender': message['sender'],
        'data': message['data']
    })

@socketio.on('auth', namespace='/chat')
def socket_auth(req):
    join_room(req['username'])
    emit('server message', {
        'sender': 'Server',
        'data': 'You&apos;re logged in as ' + req['username']
    })

@socketio.on('admin message', namespace='/chat')
def admin_message(req):
    if 'password' not in req:
        emit('error message', {
            'message': 'no password given'
        })
        return None

    if req['password'] != app.config['ADMIN_MESSAGE_PASSWORD']:
        emit('error message', {
            'message': 'invalid password'
        })
        return None

    if 'destination' not in req:
        emit('error message', {
            'message': 'no destination given'
        })
        return None

    try:
        emit('admin message', {
            'sender': 'Operator', # TODO operator name
            'data': req['data'],
        }, room=req['destination'])
    except Exception as e:
        emit('error message', {
            'data': str(e)
        })
    else:
        emit('admin message', {
            'sender': 'Operator', # TODO operator name
            'data': req['data'],
        })

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('server message', {
        'sender': 'Server',
        'data': 'Connected'
    })

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')
