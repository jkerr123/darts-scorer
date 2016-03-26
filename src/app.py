from functools import wraps
from hashlib import sha256
import os
import uuid
from flask import Flask, session, jsonify, request, render_template, redirect, url_for, make_response, send_file, \
    Response, current_app, flash
from flask_login import LoginManager
from flask_socketio import SocketIO, emit, join_room
from flask_sslify import SSLify
from werkzeug.exceptions import abort

from src.models.database import Database
from src.models.user import User
from src.models.aroundtheworld import AroundTheWorld
from src.models.dartsat import DartsAt
from src.models.bobs27 import Bobs27

app = Flask(__name__)

__author__ = 'jamie'

#MONGODB_URI = "mongodb://heroku_plq17kjt:au06mdnk5ll4tq8dudvfccu89d@ds041934.mongolab.com:41934/heroku_plq17kjt"
MONGODB_URI = os.environ.get('MONGOLAB_URI')


app.secret_key = os.urandom(24)

socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)

match = None

connected_users = list()
opponent = None


def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        return redirect(request.url.replace("http://", "https://"))

    return decorated_view


def loggedin(function):
    @wraps(function)
    def wrapper():
        if 'name' in session:
            function()
        else:
            abort(401)
    return wrapper


def setup_database():
    Database.initialize(MONGODB_URI)


@app.route('/')
def home_page():

    if 'email' in session:
        return render_template("index.html", message="You are logged in as " + session['name'])
    return render_template("index.html")


@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route('/login')
def login_page():
    return render_template("login.html")


@app.route('/player-lobby')
@loggedin
def player_lobby():
    return render_template("player-lobby.html")


@app.route('/games')
@loggedin
def games_list():
    return render_template("games.html")


@app.route('/around-the-board')
@loggedin
def around_the_board_page():
    return render_template("around-the-board.html")


@app.route('/100-darts-at')
@loggedin
def darts_at_page():
    return render_template("100-darts-at.html")


@app.route('/bobs-27')
@loggedin
def bobs_27_page():
    return render_template("bobs-27.html")


@app.route('/profile')
@loggedin
def profile_page():
    return render_template("profile.html", aroundTheBoard=around_the_board_stats(),
                           dartsAt=darts_at_stats())


def darts_at_stats():
    player = session['name']
    games = DartsAt.get_games(player)
    return games


def around_the_board_stats():
    player = session['name']
    games = AroundTheWorld.get_games(player)
    return games

@app.route("/update/100-darts-at", methods=["POST"])
def update_darts_at():
    data = request.get_json()
    player = session['name']
    dartsThrown = data['dartsThrown']
    score = data['score']
    points = data['points']
    number = data['number']

    if DartsAt.add_game(player, dartsThrown, score, points, number):
        return jsonify({"message": "Done"}), 200
    else:
        return jsonify({"error": "The data could not be saved"}), 201


@app.route("/update/bobs-27", methods=["POST"])
def update_bobs_27():
    data = request.get_json()
    player = session['name']
    score = data['score']
    if Bobs27.add_game(player, score):
        return jsonify({"message": "Done"}), 200
    else:
        return jsonify({"error": "The data could not be saved"}), 201


@app.route("/update/around-the-board", methods=["POST"])
def update_around_the_board():
    data = request.get_json()
    player = session['name']
    numberOfDarts = data['numberOfDarts']
    mode = data['mode']

    if AroundTheWorld.add_game(player, numberOfDarts, mode):
        return jsonify({"message": "Done"}), 200
    else:
        return jsonify({"error": "The data could not be saved"}), 201


@app.route('/auth/register', methods=["POST"])
def register_user():
    name = request.form['username']
    password = sha256(request.form['password'].encode('utf-8')).hexdigest()
    email = request.form['email']
    if User.register_user(name, password, email):
        session['name'] = name
        return redirect(url_for('home_page'))
    else:
        flash("This user already exists")
        return redirect(url_for('register_page'))


@app.route('/auth/login', methods=["POST"])
def login_user():
    user_name = request.form['username']
    user_password = request.form['password']

    if User.check_login(user_name, user_password):
        session['name'] = user_name
        return redirect(url_for('home_page'))
    else:
        flash("Your username or password was incorrect")
        return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))


@socketio.on('joined', namespace='/chat')
def joined():
    user = session['name']
    join_room(user)
    connected_users.append(user)
    emit('status', {'msg': user + ' has entered the room.', 'user': user, 'userlist': connected_users}, broadcast=True)


@socketio.on('message', namespace='/chat')
def message_received(message):
    user = session['name']
    emit('message received', {'message': user + ': ' + message['msg']}, broadcast=True)


@socketio.on('playerleft', namespace='/chat')
def disconnected():
    user = session['name']
    connected_users.remove(user)
    emit('status', {'msg': user + ' has left the room.', 'user': user, 'userlist': connected_users}, broadcast=True)


@socketio.on('challenge_player', namespace='/chat')
def challenge_player(player):
    user = session['name']
    room = player['player']
    newroom = user + room
    join_room(newroom)
    emit('challenged', {'msg': user + ' has challenged you to 501, accept?', 'player': user, 'newroom': newroom})


@socketio.on('matchaccepted', namespace='/chat')
def player_accepted(data):
    join_room(data['room'])
    matchid = str(uuid.uuid1())
    url = '/match/' + matchid
    emit('beginmatch', {'url': url})


@socketio.on('setupmatch', namespace='/chat')
def setup_match(data):
    join_room(data['room'])
    matchid = str(uuid.uuid1())
    url = '/match/' + matchid
    emit('beginmatch', {'url': url})


@app.route('/player-challenged', methods=['POST'])
def match_accepted():
    json = request.get_json()

    session['opponent'] = json['player']
    room = json['newroom']

    return jsonify({'room': room})




@app.route('/match/<uuid:match_id>', methods=["GET", "POST"])
def start_match(match_id):
    test= 12
    myData = {'name': session['name'],
              'score': 501,
              'dartaverage': 0,
              'doublepercentage': 0
              }

    theirData = {'name': session['opponent'],
              'score': 501,
              'dartaverage': 0,
              'doublepercentage': 0
              }

    matchData = {'id': match_id,
                'legs': 5,
                 'sets': 1
                }
    return render_template("match.html", myData=myData, theirData=theirData, matchData=matchData)


@app.before_first_request
def init_app():
    setup_database()


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
