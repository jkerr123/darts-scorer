from flask import Flask, session, jsonify, request, render_template, redirect, url_for, make_response, send_file, \
    Response
from database import Database

app = Flask(__name__)

__author__ = 'jamie'

MONGODB_URI = 'mongodb://heroku_plq17kjt:au06mdnk5ll4tq8dudvfccu89d@ds041934.mongolab.com:41934/heroku_plq17kjt'


def setup_database():
    Database.initialize(MONGODB_URI)


@app.route('/')
def home_page():
    user = Database.find_one("users", {"username": "jamie"})
    return render_template("index.html", message=user['username'])


@app.before_first_request
def init_app():
    setup_database()

if __name__ == "__main__":
    app.run()
