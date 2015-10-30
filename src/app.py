from flask import Flask, session, jsonify, request, render_template, redirect, url_for, make_response, send_file, \
    Response
from database import Database
from _sha256 import sha256
from user import User

app = Flask(__name__)

__author__ = 'jamie'

MONGODB_URI = 'mongodb://heroku_plq17kjt:au06mdnk5ll4tq8dudvfccu89d@ds041934.mongolab.com:41934/heroku_plq17kjt'


def setup_database():
    Database.initialize(MONGODB_URI)


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route('/auth/register', methods=["POST"])
def register_user():
    email = request.form.get['email']
    password = sha256(request.form.get['password'].encode('utf-8')).hexdigest()
    if User.register_user(email, password):
        session['email'] = email
        return redirect(url_for('home_page', message="You have been registered"))
    else:
        return redirect(url_for('register_page', message="User exists"))


@app.before_first_request
def init_app():
    setup_database()

if __name__ == "__main__":
    app.run()
