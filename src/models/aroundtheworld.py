from datetime import datetime
from bson import UUIDLegacy
from database import Database

__author__ = 'jamie'

COLLECTION = "aroundtheworld"


class AroundTheWorld(object):

    @staticmethod
    def add_game(_id, name, numberOfDarts, numberOfDartsAtEachNumber):

        if Database.insert(COLLECTION, {"_id": _id, "username": name, "numberOfDarts": numberOfDarts, "numberOfDartsAtEachNumber":
                                        numberOfDartsAtEachNumber, "date": datetime.now()}):
            return True
        return False

    @staticmethod
    def get_games(name):
        games = Database.find(COLLECTION, {"username": name}, "date")
        return games

    @staticmethod
    def get_by_id(game_id):
        game = Database.find_one(COLLECTION, {"_id": UUIDLegacy(game_id)})
        return game
