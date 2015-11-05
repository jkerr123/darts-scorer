from flask import session
from flask_socketio import SocketIO
from flask_socketio import join_room, emit
import socketio

__author__ = 'jamie'


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('messager', namespace='/chat')
def message_received(message):
    room = session['room']
    emit('message received', {'message': session.get('name') + ':' + message['msg']}, room=room)



