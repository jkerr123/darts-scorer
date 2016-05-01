from datetime import datetime
from bson.binary import UUIDLegacy
from database import Database

__author__ = 'jamie'

COLLECTION = "dartsAt"


class DartsAt(object):

    @staticmethod
    def add_game(_id, name, numberOfDarts, score, points, number, miss, single, double, treble):

        if Database.insert(COLLECTION, {"_id": _id, "username": name, "numberOfDarts": numberOfDarts, "score": score,
                                        "points": points, "number": number, "date": datetime.now(),
                                        "miss": miss, "single": single, "double": double, "treble": treble}):
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

    @staticmethod
    def get_leaderboard(numResults = None):
        if numResults:
            results = Database.find(COLLECTION, {}, "points", -1, numResults)
        else:
            results = Database.find(COLLECTION, {}, "points", -1)

        return results
