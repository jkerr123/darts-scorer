from flask import session
from flask_socketio import emit, join_room, socketio

__author__ = 'jamie'


@socketio.on('player joined',  namespace='/lobby')
def player_connect():
    user = session['email']
    room = session['room']
    join_room(room)
    emit('player connected', {'player': user}, room=room)


@socketio.on('message', namespace='/lobby')
def message_received(message):
    room = session['room']
    emit('message received', {'message': session.get('name') + ':' + message['message']}, room=room)


