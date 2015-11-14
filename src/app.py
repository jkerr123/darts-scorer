from functools import wraps
from hashlib import sha256
import os
from flask import Flask, session, jsonify, request, render_template, redirect, url_for, make_response, send_file, \
    Response, current_app
from flask_socketio import SocketIO, emit, join_room
from flask_sslify import SSLify

from src.models.database import Database
from src.models.user import User

app = Flask(__name__)

__author__ = 'jamie'

MONGODB_URI = 'mongodb://heroku_plq17kjt:au06mdnk5ll4tq8dudvfccu89d@ds041934.mongolab.com:41934/heroku_plq17kjt'
app.secret_key = os.urandom(24)

socketio = SocketIO(app)

connected_users = list()

def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):

                return redirect(request.url.replace("http://", "https://"))


    return decorated_view



def setup_database():
    Database.initialize(MONGODB_URI)


@app.route('/')
def home_page():
    if 'email' in session:
        return render_template("index.html", message="You are logged in as " + session['email'])
    return render_template("index.html")


@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route('/player-lobby')
def player_lobby():
    return render_template("player-lobby.html")


@app.route('/auth/register', methods=["POST"])
def register_user():
    email = request.form['email']
    password = sha256(request.form['password'].encode('utf-8')).hexdigest()
    if User.register_user(email, password):
        session['email'] = email
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for('register_page'))


@socketio.on('joined', namespace='/chat')
def joined():
    user = session['email']
    join_room(user)
    connected_users.append(user)
    emit('status', {'msg': user + ' has entered the room.', 'user': user, 'userlist': connected_users}, broadcast=True)


@socketio.on('message', namespace='/chat')
def message_received(message):
    user = session['email']
    emit('message received', {'message': user + ': ' + message['msg']}, broadcast=True)


@socketio.on('playerleft', namespace='/chat')
def disconnected():
    user = session['email']
    connected_users.remove(user)
    emit('status', {'msg': user + ' has left the room.', 'user': user, 'userlist': connected_users}, broadcast=True)


@socketio.on('challenge_player', namespace='/chat')
def challenge_player(player):
    user = session['email']
    room = player['player']
    emit('challenged', {'msg': user + ' has challenged you to 501, accept?', 'user': user}, room=room)


@app.before_first_request
def init_app():
    setup_database()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
