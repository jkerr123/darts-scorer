from datetime import datetime
from database import Database

__author__ = 'jamie'

COLLECTION = "dartsAt"


class DartsAt(object):

    @staticmethod
    def add_game(name, numberOfDarts, score, points, number):

        if Database.insert(COLLECTION, {"username": name, "numberOfDarts": numberOfDarts, "score": score,
                                        "points": points, "number": number, "date": datetime.now()}):
            return True
        return False

    @staticmethod
    def get_games(name):
        games = Database.find(COLLECTION, {"username": name}, "date")
        return games
