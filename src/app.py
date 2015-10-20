from flask import Flask, render_template
import pymongo


app = Flask(__name__)

__author__ = 'jamie'


@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
