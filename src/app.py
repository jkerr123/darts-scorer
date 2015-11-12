from functools import wraps
from hashlib import sha256
import os
from flask import Flask, session, jsonify, request, render_template, redirect, url_for, make_response, send_file, \
    Response, current_app
from flask_socketio import SocketIO, emit

from src.models.database import Database
from src.models.user import User

app = Flask(__name__)

__author__ = 'jamie'

MONGODB_URI = 'mongodb://heroku_plq17kjt:au06mdnk5ll4tq8dudvfccu89d@ds041934.mongolab.com:41934/heroku_plq17kjt'
app.secret_key = os.urandom(24)
socketio = SocketIO(app)


def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))

        return fn(*args, **kwargs)

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
    session['room'] = "player-lobby"
    return render_template("player-lobby.html", room=session['room'])


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
@ssl_required
def joined():
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    user = session['email']
    emit('status', {'msg': user + ' has entered the room.', 'user': user}, broadcast=True)


@socketio.on('message', namespace='/chat')
@ssl_required
def message_received(message):
    user = session['email']
    emit('message received', {'message': user + ': ' + message['msg']}, broadcast=True)



@app.before_first_request
def init_app():
    setup_database()

if __name__ == "__main__":
    socketio.run(app)
