from functools import wraps
from hashlib import sha256
import os
import uuid
from flask import Flask, session, jsonify, request, render_template, redirect, url_for, make_response, flash
from flask_login import LoginManager
from flask_socketio import SocketIO, emit, join_room
from flask_uuid import FlaskUUID
from werkzeug.exceptions import abort

from src.models.database import Database
from src.models.user import User
from src.models.aroundtheworld import AroundTheWorld
from src.models.dartsat import DartsAt
from src.models.bobs27 import Bobs27

app = Flask(__name__)
FlaskUUID(app)
__author__ = 'jamie'

MONGODB_URI = os.environ.get('MONGO_URL')


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
            return make_response(function())
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


@app.route('/bobs-27-summary', methods=['GET'])
@loggedin
def bobs_27_summary():
    game_id = request.args.get('game_id')
    game = Bobs27.get_by_id(uuid.UUID(game_id))
    return render_template('bobs-27-summary.html', game=game)

@app.route('/darts-at-summary', methods=['GET'])
@loggedin
def darts_at_summary():
    game_id = request.args.get('game_id')
    game = DartsAt.get_by_id(uuid.UUID(game_id))
    return render_template('bobs-27-summary.html', game=game)


@app.route('/around-the-board-summary', methods=['GET'])
@loggedin
def around_the_board_summary():
    game_id = request.args.get('game_id')
    game = AroundTheWorld.get_by_id(uuid.UUID(game_id))
    dartsThrownAtDict = game['numberOfDartsAtEachNumber']
    dartsThrownAt = []
    dartsThrownAtLabels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12', '13', '14', '15', '16',
                           '17', '18', '19', '20', 'Bull']

    # can't loop through because keys are unordered strings. Auto ordering does not work.
    dartsThrownAt.append(dartsThrownAtDict['1'])
    dartsThrownAt.append(dartsThrownAtDict['2'])
    dartsThrownAt.append(dartsThrownAtDict['3'])
    dartsThrownAt.append(dartsThrownAtDict['4'])
    dartsThrownAt.append(dartsThrownAtDict['5'])
    dartsThrownAt.append(dartsThrownAtDict['6'])
    dartsThrownAt.append(dartsThrownAtDict['7'])
    dartsThrownAt.append(dartsThrownAtDict['8'])
    dartsThrownAt.append(dartsThrownAtDict['9'])
    dartsThrownAt.append(dartsThrownAtDict['10'])
    dartsThrownAt.append(dartsThrownAtDict['11'])
    dartsThrownAt.append(dartsThrownAtDict['12'])
    dartsThrownAt.append(dartsThrownAtDict['13'])
    dartsThrownAt.append(dartsThrownAtDict['14'])
    dartsThrownAt.append(dartsThrownAtDict['15'])
    dartsThrownAt.append(dartsThrownAtDict['16'])
    dartsThrownAt.append(dartsThrownAtDict['17'])
    dartsThrownAt.append(dartsThrownAtDict['18'])
    dartsThrownAt.append(dartsThrownAtDict['19'])
    dartsThrownAt.append(dartsThrownAtDict['20'])
    dartsThrownAt.append(dartsThrownAtDict['Bull'])

    return render_template("around-the-board-summary.html", game=game, dartsThrownAt=dartsThrownAt, dartsThrownAtLabels
                           =dartsThrownAtLabels)


@app.route("/update/100-darts-at", methods=["POST"])
def update_darts_at():
    _id = uuid.uuid4()
    data = request.get_json()
    player = session['name']
    dartsThrown = data['dartsThrown']
    score = data['score']
    points = data['points']
    number = data['number']

    if DartsAt.add_game(_id, player, dartsThrown, score, points, number):
        return jsonify({"message": "Done"}), 200
    else:
        return jsonify({"error": "The data could not be saved"}), 201


@app.route("/update/bobs-27", methods=["POST"])
def update_bobs_27():
    _id = uuid.uuid4()
    data = request.get_json()
    player = session['name']
    score = data['score']
    if Bobs27.add_game(_id, player, score):
        return jsonify({"message": "Done"}), 200
    else:
        return jsonify({"error": "The data could not be saved"}), 201


@app.route("/update/around-the-board", methods=["POST"])
def update_around_the_board():
    _id = uuid.uuid4()
    data = request.get_json()
    player = session['name']
    numberOfDarts = data['numberOfDarts']
    dartsAtEachNumber = data['dartsAtEachNumber']

    if AroundTheWorld.add_game(_id, player, numberOfDarts, dartsAtEachNumber):
        return jsonify({"message": "Game Saved!", "id": _id}), 200
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

@app.route('/leaderboards')
def leaderboards():
    around_the_board_leader = AroundTheWorld.get_leaderboard(10)
    darts_at_leader = DartsAt.get_leaderboard(10)
    bobs_27_leader = Bobs27.get_leaderboard(10)
    return render_template('leaderboards.html', around_the_board=around_the_board_leader,
                           darts_at=darts_at_leader, bobs27=bobs_27_leader)



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
