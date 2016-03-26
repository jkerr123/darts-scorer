from datetime import datetime
from database import Database

__author__ = 'jamie'

COLLECTION = "bobs27"


class Bobs27(object):

    @staticmethod
    def add_game(name, score,):

        if Database.insert(COLLECTION, {"username": name,  "score": score, "date": datetime.now()}):
            return True
        return False

    @staticmethod
    def get_games(name):
        games = Database.find(COLLECTION, {"username": name}, "date")
        return games
