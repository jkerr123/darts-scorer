import os
from flask import Flask, session, jsonify, request, render_template, redirect, url_for, make_response, send_file, \
    Response
from flask_socketio import SocketIO

from database import Database
from _sha256 import sha256
from user import User

app = Flask(__name__)

__author__ = 'jamie'

MONGODB_URI = 'mongodb://heroku_plq17kjt:au06mdnk5ll4tq8dudvfccu89d@ds041934.mongolab.com:41934/heroku_plq17kjt'
app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



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


@app.before_first_request
def init_app():
    setup_database()

if __name__ == "__main__":
    socketio.run(app, debug=True)
