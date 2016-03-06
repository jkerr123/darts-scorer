from datetime import datetime
from database import Database

__author__ = 'jamie'

COLLECTION = "aroundtheworld"


class AroundTheWorld(object):

    @staticmethod
    def add_game(email, numberOfDarts, mode):

        if Database.insert(COLLECTION, {"name": email, "numberOfDarts": numberOfDarts, "mode": mode, "date": datetime.now()}):
            return True
        return False

    @staticmethod
    def get_games(email):
        games = Database.find(COLLECTION, {"name": email}, "date")
        return games
