from datetime import datetime
from database import Database

__author__ = 'jamie'

COLLECTION = "aroundtheworld"


class AroundTheWorld(object):

    @staticmethod
    def add_game(name, numberOfDarts, mode):

        if Database.insert(COLLECTION, {"username": name, "numberOfDarts": numberOfDarts, "mode": mode, "date": datetime.now()}):
            return True
        return False

    @staticmethod
    def get_games(name):
        games = Database.find(COLLECTION, {"username": name}, "date")
        return games
