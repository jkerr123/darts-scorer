from hashlib import sha256
from database import Database

__author__ = 'jamie'

COLLECTION = "users"


class User(object):

    @staticmethod
    def register_user(username, password, email):
        user = User.find_user(username)
        if user is not None:
            return False
        if Database.insert(COLLECTION, {"username": username, "password": password, "email": email}):
            return True

        return False

    @staticmethod
    def find_user(username):
        return Database.find_one(COLLECTION, {"username": username})


    @staticmethod
    def check_login(username, password):
        # This method checks a login/password combo is correct
        user = User.find_user(username)
        if user is not None:
            password_encode = password.encode('utf-8')
            if user['password'] == sha256(password_encode).hexdigest():
                return True
        return False
