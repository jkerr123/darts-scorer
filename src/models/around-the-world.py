from database import Database

__author__ = 'jamie'

COLLECTION = "users"


class AroundTheWorld(object):

    @staticmethod
    def add_game(email, numberOfDarts, mode):
        if Database.insert(COLLECTION, {"email": email, "numberOfDarts": numberOfDarts, "mode": mode}):
            return True

        return False
