import logging
from flask import Flask, render_template
import pymongo
import sys

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

__author__ = 'jamie'


@app.route("/")
def run():
    return render_template("index.html", message="test")

if __name__ == "__main__":
    app.run()
