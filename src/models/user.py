from database import Database

__author__ = 'jamie'

COLLECTION = "users"


class User(object):

    @staticmethod
    def register_user(email, password):
        if Database.insert(COLLECTION, {"email": email, "password": password}):
            return True

        return False

    @staticmethod
    def find_user(email):
        Database.find_one(COLLECTION, {"email": email})
