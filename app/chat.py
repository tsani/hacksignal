from app import app, socketio

from flask import session

from flask.ext.socketio import emit, join_room

def admin_authenticate(inner):
    """ Wrap a SocketIO endpoint requiring the socket to have administrative
        primileges.
    """
    def authenticate_and_call(req):
        """ Two checks are performed on the socket: either it provides a
            password in the request or its session has administrative
            privileges.
        """
        password = 'password' in req and \
                req['password'] == app.config['ADMIN_MESSAGE_PASSWORD']
        is_admin = 'password' in session and \
                session['password'] == app.config['ADMIN_MESSAGE_PASSWORD']

        if password or is_admin:
            inner(req)
        else:
            emit('error message', {
                'message': 'authentication required'
            })
            return None

    return authenticate_and_call

@socketio.on('chat message', namespace='/chat')
def chat_message(message):
    print 'dispatching chat message'
    emit('chat message', {
        # The username is established in the session upon authenticating
        'sender': session['username'],
        'data': message['data']
    }, room='__admin__')

    emit('chat message', {
        'sender': session['username'],
        'data': message['data']
    })

@socketio.on('auth', namespace='/chat')
def socket_auth(req):
    session['username'] = req['username']
    join_room(req['username'])
    emit('server message', {
        'sender': 'Server',
        'data': 'You\'re logged in as ' + req['username']
    })

@socketio.on('admin auth', namespace='/chat')
@admin_authenticate
def admin_auth(req):
    join_room('__admin__')
    session['password'] = app.config['ADMIN_MESSAGE_PASSWORD']
    emit('server message', {
        'sender': 'Server',
        'data': 'Authenticated administrator.'
    })

@socketio.on('admin message', namespace='/chat')
@admin_authenticate
def admin_message(req):
    if 'destination' not in req:
        emit('error message', {
            'message': 'no destination given'
        })
        return None

    try:
        # Dispatch the message to the destination
        emit('admin message', {
            'sender': 'Operator', # TODO operator name
            'data': req['data'],
        }, room=req['destination'])
        print 'dispatched message to', req['destination']
    except Exception as e:
        emit('error message', {
            'data': str(e)
        })
    else:
        # Echo the message back to the admins
        emit('admin message', {
            'sender': 'Operator', # TODO operator name
            'data': req['data'],
            'destination': req['destination'],
        }, room='__admin__')

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('server message', {
        'sender': 'Server',
        'data': 'Connected'
    })

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    pass
