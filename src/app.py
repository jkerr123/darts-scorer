from flask import Flask, render_template
import pymongo
from src.models.database import Database

app = Flask(__name__)

__author__ = 'jamie'


@app.before_first_request
def init_app():
    Database
    return render_template("index.html", message="test")

if __name__ == "__main__":
    app.run()
