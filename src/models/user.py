from database import Database

__author__ = 'jamie'

COLLECTION = "users"


class User(object):

    @staticmethod
    def register_user(email, password):
        Database.insert(COLLECTION, {"email": email, "password": password})

    @staticmethod
    def find_user(email):
        Database.find_one(COLLECTION, {"email": email})
